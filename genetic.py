from typing import Dict, List

def approach_level(hctest:Dict,hcbranch:Dict,goal_branch: str)->int:
    '''
    Returns:
        int: the branch depth of the first branch that was not covered.
    '''
    assert goal_branch in hcbranch.keys(), "goal branch does not exist in this program"
    for branch in hcbranch.keys():
        if branch not in goal_branch:
            continue
        if branch == goal_branch:
            return 0, None
        if branch not in hctest.keys() or not hctest[branch]:
            return len(goal_branch.split("."))-len(branch.split(".")), branch

def fitness(hctest:Dict,hcbranch:Dict, inputs: Dict[str,int])->float:
    approach_level, blocked_branch = approach_level(hctest,hcbranch)
    if approach_level == 0:
        return
    branch_distance = -abs(blocked_branch.branch_distance(inputs))
    return approach_level+(1-1.001**(branch_distance))

