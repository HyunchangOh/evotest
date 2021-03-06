from typing import Dict

class Branch:
    def __init__(self, depth:str, left_phrase: str, right_phrase: str=0, comparator:str="!="):
        self.depth = depth
        self.left = left_phrase
        self.right = right_phrase[:-1]
        self.comparator = comparator
    
    def branch_distance(self,inputs:Dict[str,int]):
        code = ""
        for key,value in inputs.items():
            if key in ["hcbranch","branch","hcbranch","hcdistance","answer","coverage_report","new_inputs","all_variables","function","generations","prev_seeds","store_format","input_no"]:
                continue
            new_line = f"{key}={value}\n"
            code+=new_line
        code += f"global hcpassed\n"
        code += f"global hcdistance\n"
        code += f"hcpassed=({self.left}{self.comparator}{self.right})\n"
        code += f"hcdistance = ({self.left})-({self.right})\n"

        exec(code)
        return hcpassed, hcdistance


    def get_branch(depth:str,line:str):
        #if (x+y)*3>3:
        core = "".join(line.split()[1:])
        comparators = ["==",">=","<=", "!=", "<", ">"]
        for comparator in comparators:
            if comparator in core:
                cores = core.split(comparator)
                left = cores[0]
                right = cores[1]
                return Branch(depth,left,right,comparator)
        return Branch(depth,left)

    def __str__(self):
        return f"{self.depth}: {self.left} {self.comparator} {self.right}"