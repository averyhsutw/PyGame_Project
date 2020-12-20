import random
import copy


maxeval ={}

check_last_step = {(1, 3): 3}
step = {(2, 3): 2}
child_step  = (4,5)


def dic_min (dict1,dict2):
    new_dict_min = {**dict1,**dict2}
    max_pos = max(new_dict_min,key = new_dict_min.get)

    for i in new_dict_min:
        if i == max_pos:
            new_dict_min.pop(max_pos)
            return new_dict_min

def dic_max (dict1,dict2):
    if dict1 is None:
        return dict2
    else:
        new_dict_max = {**dict1,**dict2}
        min_pos = min(new_dict_max,key = new_dict_max.get)

        for i in new_dict_max:
            if i == min_pos:
                new_dict_max.pop(min_pos)
                return new_dict_max


  
print(dic_min(check_last_step,step))



