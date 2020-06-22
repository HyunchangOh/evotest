class Branch:
    def __init__(self, depth:str, left_phrase: str, right_phrase: str=0, comparator:str="!="):
        self.depth = depth
        self.left = left_phrase
        self.right = right_phrase
        self.comparator = comparator
    
    def branch_distance(self,inputs:Dict[str,int]):
        code = ""
        for key,value in inputs.items():
            new_line = f"{key}={value}\n"
            code+=new_line
        code += f"(hcpassed=({self.left}{self.comparator}{self.right})\n"
        code += f"(hcdistance = {self.left})-({self.right})"
        exec(code)
        return hcpassed, hcdistance

    def get_branch(depth:str,line:str)->Branch:
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