from typing import Dict, List, Callable, Tuple
import random, sys

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

def fitness(hctest:Dict,hcbranch:Dict, inputs: Dict[str,int], goal_branch:str)->float:
    approach_level, blocked_branch = approach_level(hctest,hcbranch,goal_branch)
    if approach_level == 0:
        return
    branch_distance = -abs(blocked_branch.branch_distance(inputs))
    return approach_level+(1-1.001**(branch_distance))

def get_seed(input_no:int)->List[int]:
    seed = []
    for a in range(input_no):
        seed.append(biased_random())
    return tuple(seed)

def biased_random()->int:
    '''
    Returns:
        int: random integer that is likely to be close to zero.
    '''
    mx = sys.maxsize
    rn = 1-random.random()*2
    return int(rn**21*mx)



def evolve(coverage_report:Dict[Tuple[int],Dict[str,bool]],hcbranch:Dict)->List[Tuple[int]]:
    keys = []
    for input_set, hctest in coverage_report.items():
        # f = fitness(hctest,hcbranch,input_set,goal_branch)
        new_input = []
        for j in input_set:
            new_input.append(j//10000)
        keys.append(tuple(new_input))
    return keys

