import pickle

f = open("report.pkl","rb")
answer = pickle.load(f)
for function in answer.keys():
    print(f"\n==== Function: {function} ====")
    ans = answer[function]
    for key in ans.keys():
        new_set = [dict(t) for t in {tuple(d.items()) for d in ans[key]}]
        if len(new_set)>5:
            print(f"{key}: {len(new_set)} Set of Inputs")
        elif len(new_set)>0:
            print(f"{key}: {new_set}")
        else:
            print(f"{key}: -")
