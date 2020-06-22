from branch import Branch
from genetic import *

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

def answer_pretty_print(ans):
    for key in ans.keys():
        new_set = set(ans[key])
        if new_set:
            print(f"{key}: {new_set}")
        else:
            print(f"{key}: -")

def insert_oracles(filename):
    f = open(filename,'r')
    g= open("target.py",'w')
    g.write("hctest={}\n")

    #initialise
    if_counter = 0
    while_counter = 0
    branch_counts = [1]
    hcbranch = dict()

    for line in f:
        indent = get_indent(line.rstrip())
        
        if indent >= len(branch_counts):
            branch_counts.append(0)
        if line.lstrip().startswith("def"):
            function_name= line.lstrip().replace("def "," ").split("(")[0].strip()
            g.write(no_print_liner(line))

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
            hcbranch[br]= Branch.get_branch(br,line)

            g.write(no_print_liner(line))
            g.write((indent+1)*4*" ")
            g.write(f"hctest['{br}']=True\n")

        else:
            g.write(no_print_liner(line))

    # g.write(function_name+inputs+"\n")
    g.close()
    return hcbranch

def get_functions(filename):
    all_functions = dict()
    f = open(filename,"r")
    for line in f:
        if line.lstrip().startswith("def"):
            function_name = line.split()[1].split("(")[0]
            input_number = len(line.split("(")[1].split(")")[0].split(","))
            all_functions[function_name] = input_number
    return all_functions

def randinput_applier(generations:int,function:Callable,input_no:int,hcbranch:Dict)->Dict[str,List[Tuple[int]]]:
    answer = {}
    prev_seeds = get_seed(input_no)

    for branch in hcbranch.keys():
        answer[branch+"T"] = []
        answer[branch+"F"] = []

    for j in range(generations):
        globals()[function](*prev_seeds)
        
        for branch in hcbranch.keys():
            if branch in hctest.keys():
                if hctest[branch]:
                    answer[branch+"T"].append(prev_seeds)
                else:
                    answer[branch+"F"].append(prev_seeds)
        coverage_report = dict()
        coverage_report[prev_seeds] = hctest
        

    for j in range(generations):
        new_inputs = evolve(coverage_report,hcbranch)
        coverage_report = dict()
        for a in new_inputs:
            globals()[function](*a)
            print(a)
            for branch in hcbranch.keys():
                if branch in hctest.keys():
                    if hctest[branch]:
                        answer[branch+"T"].append(a)
                    else:
                        answer[branch+"F"].append(a)
            coverage_report[a] = hctest
        print(f"\n================ Generation {j} ================")
        answer_pretty_print(answer)
    return answer

print(biased_random())
filename = "inputs/sample1.py"
hcbranch = insert_oracles(filename)
print(hcbranch)
functions = get_functions(filename)
from target import *

for function in functions.keys():
    randinput_applier(3,function, functions[function],hcbranch)

