import pygame
import copy
from agent.base_agent import BaseAgent

class F_BaseAgent(BaseAgent):
    def find_valid_step(self, m, c):    
        self.c = c

        exist_pos = []
        valid_list = []

        for i in m:
            if m[i] == self.c: #noted color change
                exist_pos.append((i%8, i//8))
        #print(exist_pos)
        for p in exist_pos:
        #print(p)
            valid_list.append(self.find_pos(p,m,self.c))
        #print(merge_pos_rewards(valid_list))
        return self.merge_pos_rewards(valid_list)
    

    def find_pos(self,t,m,c):
        pos_reward = {}
       
        move = [[1,1],[1,0],[0,1],[-1,-1],[0,-1],[-1,0],[-1,1],[1,-1]]
        for i in move:
            ate = 0
            #edible = False
            #tasty = False
            pos = [t[0]+i[0], t[1]+i[1]]
            if not self.valid_move(pos) or m[pos[0]+pos[1]*8] != -c: #noted color change
                continue
            else:
                ate+=1
                pos = [pos[0]+i[0], pos[1]+i[1]]
                while self.valid_move(pos):
                    if m[pos[0]+pos[1]*8] == -c:
                        ate+=1
                        pos = [pos[0]+i[0], pos[1]+i[1]]
                    elif m[pos[0]+pos[1]*8] == c:
                        break
                    else:
                        ate+=1
                        pos_t = tuple(pos)
                        if pos_reward  == {} or pos_t not in pos_reward:
                            pos_reward.update({pos_t : ate})
                        elif pos_t in pos_reward:
                            pos_reward[pos_t] += ate-1
                        break
        return pos_reward


    def valid_move(self,l):# part of find_valid_step

            if l[0]<0 or l[0]>7 or l[1]<0 or l[1]>7:
                return False
            else: return True

    def merge_pos_rewards(self,rs):# part of find_valid_step
        merged_result = {}
        for r in rs:
            for k in r:
                if k not in merged_result:
                    merged_result.update({k:r[k]})
                else:
                    merged_result[k] += r[k]
        return merged_result


    def get_avmove_pos(self,pos_step):
        return list(pos_step.keys())

    def get_avmove_reward(self,pos_step):
        return list(pos_step.values())

    def change_obs_value(self,obs_copy,position,value_of_change):
        position = position[0]+(position[1]-1)*8    #(x,y) to 0-63
        obs_copy[position] = value_of_change
        return obs_copy

    def unchange_obs_value(self,obs_copy,position,value_of_change):
        position = position[0]+(position[1]-1)*8    #(x,y) to 0-63
        obs_copy[position] = value_of_change
        return obs_copy
    
    def my_max(self,dic):   #return the largest value and it's position of a dict 
        
        if len(dic) == 0 :
            return {(None,None):0}
        else:
            seq = []
            val = max(dic.values())
            for i in dic:
                if dic[i] == val:
                    seq = list(i)
                    break 
            seq = [(seq[0],seq[1])]
            return dict.fromkeys(seq,val)

    def return_func(self,pos,dict2):    
        
        for i in dict2:
            if pos == i :
                seq = list(i)
                break 
        seq = [(seq[0],seq[1])]
        return dict.fromkeys(seq,dict2[i])
    
    def dic_max (self,dict1,dict2): #compare two dict and return the one with larger value
        
        if dict1 is None:
            return dict2
        elif dict2 is None:
            return dict1
        else:
            new_dict = {**dict1,**dict2}
            min_pos = min(new_dict,key = new_dict.get)
            for i in new_dict:
                if i == min_pos:
                    new_dict.pop(min_pos)
                    return new_dict

    def dic_min (self,dict1,dict2): #compare two dict and return the one with smaller value
        
        if dict1 is None:
            return dict2
        elif dict2 is None:
            return dict1
        else:
            new_dict = {**dict1,**dict2}
            max_pos = max(new_dict,key = new_dict.get)
            for i in new_dict:
                if i == max_pos:
                    new_dict.pop(max_pos)
                    return new_dict

    def check(self,target,dict1):   #check if target.key matched dict1.key

        if len(target.keys() & dict1.keys()) != 0:
            return True 
        else:
            return False      
    
# main algorithm
    def minimax(self,obs,isblack_player,depth = 3):
        
        pos_step_with_reward = self.find_valid_step(obs,self.c)
        
        pos_step = self.get_avmove_pos(pos_step_with_reward)
        
        if depth == 0 :
            depth0_out = self.my_max(pos_step_with_reward)
            
            return depth0_out

        elif  isblack_player:
            maxeval = {(None,None):-1000} 
            self.c = -1 #make sure the color is right 

            for child_step in pos_step:

                obs = self.change_obs_value(obs,child_step,1)#change the obs in order to calculate the situation of the next move 

                cur_eval = self.minimax(obs,False,depth - 1 )
                if cur_eval != {(None,None):0}:

                    maxeval = self.dic_max(maxeval,cur_eval) #maxeval is the most reward of the next move

                obs = self.unchange_obs_value(obs,child_step,0)#make sure to change it back
            
            #return the step that lead to maxeval
            for child_step in pos_step_with_reward:  

                obs = self.change_obs_value(obs,child_step,1)
                check_last_step = self.find_valid_step(obs,self.c) 
                last_step = self.check(maxeval,check_last_step)

                if last_step is not None:
                    obs = self.unchange_obs_value(obs,child_step,0)
                    return self.return_func(child_step,pos_step_with_reward)
                else:
                    pass
                obs = self.unchange_obs_value(obs,child_step,0)
            
        # same as above , but it determine white's move 
        # detalis plz google minimax , I can't explain ┐(´д`)┌
        else:  
            
            mineval = {(None,None):1000}
            self.c = 1
            for child_step in pos_step:

                obs = self.change_obs_value(obs,child_step,-1)
                min_cur_eval = self.minimax(obs,True,depth - 1)
                if min_cur_eval != {(None,None):0}:
                    mineval = self.dic_min(mineval,min_cur_eval)
                obs = self.unchange_obs_value(obs,child_step,0)

            for child_step in pos_step_with_reward:
                self.c = 1

                obs = self.change_obs_value(obs,child_step,-1)
                check_last_step_min = self.find_valid_step(obs,self.c) 
                last_step_min = self.check(mineval,check_last_step_min)

                if last_step_min is not None:
                    obs = self.unchange_obs_value(obs,child_step,0)
                    return self.return_func(child_step,pos_step_with_reward)
                else:
                    obs = self.unchange_obs_value(obs,child_step,0)

class MyAgent(F_BaseAgent):
    def step(self,reward,obs):
        self.c = -1
        
        cur_pos_with_rw = self.find_valid_step(obs,-1)
        
        #corner firsttt
        corner_corner = [(0,0),(0,7),(7,0),(7,7)]
        for i in corner_corner:
            if i in cur_pos_with_rw:
                pos = (90+i[0]*60, 90+i[1]*60)
                return pos, pygame.USEREVENT

        obs_copy = copy.deepcopy(obs)
        #main algorithm (minimax)
        #return a dict with position and it's reward eg.{(x,y):reward}
        vlaue_of_minimax  = self.minimax(obs_copy,True,depth=3)

        for a in vlaue_of_minimax:
            pos = a
        pos = (90+pos[0]*60, 90+pos[1]*60)

        return pos, pygame.USEREVENT