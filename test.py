import random
import copy


def change_obs_value(obs_copy,position,changed_value):
    obs_copy[position] = changed_value
    return obs_copy

a = [1,2,3,4]
print(max(a))
obs_copy =  {(1, 1): 1, (1, 3): 5, (0, 4): 2}     

print(change_obs_value(obs_copy,(1,1),3))