steps = []

def save(parameter,index,*args):
    if index == "Null":
        steps.append(parameter+"\n")
        global new_action
        new_action = args[0]
    else:
        if args[0] == "del":
            new_action = args[0]        
        else:
            steps.insert(index, parameter+"\n")
            new_action = args[0]

def return_action_name():
    return new_action
