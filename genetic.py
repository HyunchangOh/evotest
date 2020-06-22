from typing import Dict, List

def approach_level(hctest:Dict,hcbranch:Dict)->int:
    '''
    Returns:
        int: the branch depth of the first branch that was not covered.
    '''
    for branch in hcbranch.keys():
        if branch not in hctest.keys() or not hctest[branch]:
            return len(branch.split(".")), branch
    return 0,None

def fitness(hctest:Dict,hcbranch:Dict, inputs: Dict[str,int])->float:
    approach_level, blocked_branch = approach_level(hctest,hcbranch)
    branch_distance = -abs(blocked_branch.branch_distance(inputs))
    return approach_level+(1-1.001**(branch_distance))

