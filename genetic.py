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
            return len(goal_branch.split("."))-len(branch.split(".")), hcbranch[branch]

def fitness(hctest:Dict,hcbranch:Dict, inputs: Dict[str,int], goal_branch:str, all_variables)->float:
    al, blocked_branch = approach_level(hctest,hcbranch,goal_branch)
    if al == 0:
        return 10
    branch_distance = -abs(blocked_branch.branch_distance(all_variables)[1])
    return al+(1-1.001**(branch_distance))

def get_seed(inputs:List[str])->List[int]:
    seed = dict()
    for val in inputs:
        seed[val.strip()] = biased_random()
    return seed

def biased_random()->int:
    '''
    Returns:
        int: random integer that is likely to be close to zero.
    '''
    mx = sys.maxsize
    rn = 1-random.random()*2
    return int(rn**21*mx)



def evolve(coverage_report:Dict[Tuple[int],Dict[str,bool]],hcbranch:Dict,inputs:Dict[str,int],all_variables)->List[Tuple[int]]:
    goals = []
    for key in hcbranch.keys():
        for i in range(len(key.split("."))**2):
            goals.append(key)
    
    deck = []

    for input_set, hctest in coverage_report.items(): 
        input_dict = dict()
        for i in range(len(list(inputs.keys()))):
            input_dict[list(inputs.keys())[i]] = input_set[i]

        f = fitness(hctest,hcbranch,input_dict,random.choice(goals),all_variables)
        deck += [input_set]*100*int(f)

    new_inputs = []
    for i in range(3):
        mom = random.choice(deck)
        dad = random.choice(deck)
        new_inputs.append(crossover(mom,dad,inputs))

    return new_inputs

def crossover(mom:Tuple[int],dad:Tuple[int],inputs:Dict[str,int])->Tuple[int]:
    assert len(mom) == len(dad), "mom and dad are not of the same species"
    child = {}
    count =0
    for key in inputs.keys():
        '''
            choose a random gene from mom or dad. Then mutate.
            the random multiplication is to change the order of magnitude.
            the random addition is to explore smaller-scale local search space.
        '''
        child[key]=random.choice([mom[count],dad[count]])*random.randrange(1,101,1)//100+random.randrange(-10,10,1)
        count+=1
    return child
