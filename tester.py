from branch import Branch
from genetic import *
import pickle

class InfiniteLoopException(Exception):
    pass

def initialise_pickle():
    f = open("report.pkl","wb")
    a = dict()
    pickle.dump(a,f)
    f.close()

initialise_pickle()

def get_indent(line:str)->int:
    indent = 0
    space_counter = 0
    for char in line:
        if char == "\t":
            indent+=1
        elif char==" ":
            space_counter +=1
        else:
            break
    return indent + space_counter//4

def no_print_liner(line:str)->str:
    if line.lstrip().startswith("print("):
        return line.replace("print(","")[:-2]+"\n"
    return line

def branch_reducer(blist,indent):
    ans = ""
    count = 0
    for i in blist:
        ans+= str(i)
        ans+= "."
        if count == indent:
            break
        count+=1
    return ans[:-1]

def answer_pretty_print(ans,function):
    # print("ans was ",ans)
    f = open("report.pkl","rb")
    report = pickle.load(f)
    f.close()
    f = open("report.pkl","wb")
    report[function] = ans
    pickle.dump(report,f)
    f.close()
    for key in ans.keys():
        new_set = [dict(t) for t in {tuple(d.items()) for d in ans[key]}]
        if len(new_set)>5:
            print(f"{key}: {len(new_set)} Set of Inputs")
        elif len(new_set)>0:
            print(f"{key}: {new_set}")
        else:
            print(f"{key}: -")

def insert_oracles(filename,while_limit):
    f = open(filename,'r')
    g= open("target.py",'w')
    g.write("hctest={}\n")
    g.write("hclocals={}\n")
    g.write("class InfiniteLoopException(Exception):\n    pass\n")

    #initialise
    if_counter = 0
    while_counter = 0
    branch_counts = [1]
    hcbranch = dict()
    first_function_met = False
    for line in f:
        indent = get_indent(line.rstrip())
        
        if indent >= len(branch_counts):
            branch_counts.append(0)
        if line.lstrip().startswith("def"):
            function_name= line.lstrip().replace("def "," ").split("(")[0].strip()

            if first_function_met:
                g.write("\n    hclocals['0'] = locals()\n")
            g.write(no_print_liner(line))
            g.write("\n    global hclocals\n")

            first_function_met = True

        elif line.lstrip().startswith('if'):
            branch_counts[indent] +=1
            for i in range(indent+1,len(branch_counts),1):
                branch_counts[i] = 0
            br = branch_reducer(branch_counts,indent)

            g.write((indent)*4*" ")
            g.write(f"hctest['{br}']=False\n")
            g.write(no_print_liner(line))

            hcbranch[br]= Branch.get_branch(br,line)
            g.write((indent+1)*4*" ")
            g.write(f"hctest['{br}']=True\n")

        elif line.lstrip().startswith('while'):
            g.write((indent)*4*" ")
            branch_counts[indent] = branch_counts[indent]+1
            br = branch_reducer(branch_counts,indent)
            g.write(f"hctest['{br}']=False\n")
            g.write((indent)*4*" ")
            g.write(f"hclooper =0\n")
            
            hcbranch[br]= Branch.get_branch(br,line)

            g.write(no_print_liner(line))
            g.write((indent+1)*4*" ")
            g.write(f"hctest['{br}']=True\n")
            g.write((indent+1)*4*" ")
            g.write("hclooper+=1\n")
            g.write((indent+1)*4*" ")
            g.write(f"if hclooper>{while_limit}: raise InfiniteLoopException\n")
            g.write((indent+1)*4*" ")
            g.write(f"if hclooper>{while_limit}: return\n")

        elif line.lstrip().startswith("return"):
            g.write((indent)*4*" ")
            g.write("hclocals['0'] =locals()\n")
            g.write(line)

        elif line.lstrip().startswith("for"):
            g.write((indent)*4*" ")
            branch_counts[indent] = branch_counts[indent]+1
            br = branch_reducer(branch_counts,indent)
            g.write(f"hctest['{br}']=False\n")
            g.write((indent)*4*" ")
            g.write(f"hclooper =0\n")
            
            condition = line.split("in")[1].strip()[:-1].replace("range","").replace("(","").replace(")","")
            print(condition)
            hcbranch[br]= Branch.get_branch(br,f"if {condition}>0:")

            g.write(no_print_liner(line))
            print(line)
            g.write((indent+1)*4*" ")
            g.write(f"hctest['{br}']=True\n")
            g.write((indent+1)*4*" ")
            g.write("hclooper+=1\n")
            g.write((indent+1)*4*" ")
            g.write(f"if hclooper>{while_limit}: raise InfiniteLoopException\n")
            g.write((indent+1)*4*" ")
            g.write(f"if hclooper>{while_limit}: return\n")
        else:
            g.write(no_print_liner(line))
    if first_function_met:
        # g.write("\n    global hclocals\n")
        g.write("\n    hclocals['0'] = locals()\n")

    # g.write(function_name+inputs+"\n")
    g.close()
    return hcbranch

def get_functions(filename):
    all_functions = dict()
    f = open(filename,"r")
    for line in f:
        if line.lstrip().startswith("def"):
            function_name = line.split()[1].split("(")[0]
            input_number = line.split("(")[1].split(")")[0].split(",") #change this to remove : and -> annotations
            all_functions[function_name] = input_number
    return all_functions


def randinput_applier(generations:int,function:Callable,input_no:int,hcbranch:Dict,while_limit:int)->Dict[str,List[Tuple[int]]]:
    answer = {}
    prev_seeds = get_seed(input_no)
    store_format = prev_seeds.copy()
    passed = False
    global hclocals
    # print("store format: ",store_format)
    for branch in hcbranch.keys():
        answer[branch+"T"] = []
        answer[branch+"F"] = []
    answer["Infinite Loop"] = []
    answer["Error"] = []

    for j in range(generations):
        while not passed:
            try:
                print("trying: ",prev_seeds)
                globals()[function](*list(prev_seeds.values()))
            except InfiniteLoopException:
                answer["Infinite Loop"].append(prev_seeds)
                prev_seeds = get_seed(input_no)
                continue
            except:
                answer["Error"].append(prev_seeds)
                prev_seeds = get_seed(input_no)

            passed =True
        all_variables = hclocals['0']
        for branch in hcbranch.keys():
            if branch in hctest.keys():
                if hctest[branch]:
                    answer[branch+"T"].append(prev_seeds)
                else:
                    answer[branch+"F"].append(prev_seeds)
        coverage_report = dict()
        coverage_report[tuple(prev_seeds.values())] = hctest
        

    for j in range(generations):
        # print(store_format)
        new_inputs = evolve(coverage_report,hcbranch,store_format,all_variables)
        coverage_report = dict()
        for a in new_inputs:
            # print("new inputs are: ",new_inputs)
            globals()[function](*tuple(a.values()))
            all_variables = hclocals['0']
            # print(a)
            for branch in hcbranch.keys():
                if branch in hctest.keys():
                    if hctest[branch]:
                        answer[branch+"T"].append(a)
                    else:
                        answer[branch+"F"].append(a)
            coverage_report[tuple(a.values())] = hctest
        print(f"\n================ Generation {j} for Function {function} ================")
        answer_pretty_print(answer,function)
    return answer


while_limit = 100
generations = 1
filename = "inputs/sample6.py"



# print(biased_random())
hcbranch = insert_oracles(filename,while_limit)
# print(hcbranch)
functions = get_functions(filename)
from target import *

for function in functions.keys():
    randinput_applier(generations,function, functions[function],hcbranch,while_limit)

