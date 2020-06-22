from typing import Dict, List

def approach_level(hctest:Dict,hcbranch:List)->int:
    '''
    Returns:
        int: the branch depth of the first branch that was not covered.
    '''
    for branch in hcbranch.keys():
        if branch not in hctest.keys() or not hctest[branch]:
            return len(branch.split(".")), branch
    return 0

def fitness(hctest:Dict,hcbranch:List, inputs: Dict[str,int])->float:
    approach_level = approach_level(hctest,hcbranch)
    branch_distance = Branch.get_branch

