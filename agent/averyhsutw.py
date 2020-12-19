import random
import pygame
import copy
from agent.base_agent import BaseAgent

class MyBaseAgent(BaseAgent):
    def color_num(self, color):
        if self.color == 'black':
                c = -1
        else: c = 1
        return c
    def enemy_2index_pos(self, obs):
        pos = []
        c = self.color_num(self.color)
        for i in obs:
            if obs[i] == -c: pos.append((i%8, i//8))
        return pos    
    
    def get_2index_pos(self, obs): # return tuples representing current positions.
        pos = []
        c = self.color_num(self.color)
        for i in obs:
            if obs[i] == c: pos.append((i%8, i//8))
        return pos
    
    def valid_move(self, pos):  # To avoid moving out of the frame.
        if pos[0]<0 or pos[0]>7 or pos[1]<0 or pos[1]>7:
            return False
        else: return True
        
    def find_pos(self, t, m): 
        # input: 'a tuple' in the exist_pos list
        # return the dict: pos_reward
        c = self.color_num(self.color)
        pos_reward = {}
        #in pos_reword:
        #   key: available positions to move to
        #   value: score the agent can gain(positive) or lose(negative)
        def avoid_enemy_helper(pos, i):
            white_in_back = False
            white_in_front = False
            blank_in_front = False
            blank_in_back = False
            b_pos = [t[0]-i[0],t[1]-i[1]]
            f_pos = [pos[0]+i[0],pos[1]+i[1]]
            f_count = 0
            b_count = 0
            while self.valid_move(b_pos):
                if m[b_pos[0]+b_pos[1]*8] == -c:
                    white_in_back = True
                    break
                elif m[b_pos[0]+b_pos[1]*8] == 0:
                    blank_in_back = True
                    break
                else:
                    b_count += 1
                    b_pos = [b_pos[0]-i[0],b_pos[1]-i[1]]
                    continue
            while self.valid_move(f_pos):
                if m[f_pos[0]+f_pos[1]*8] == -c:
                    white_in_front = True
                    break
                elif m[f_pos[0]+f_pos[1]*8] == 0:
                    blank_in_front = True
                    break
                else:
                    f_count += 1
                    f_pos = [f_pos[0]+i[0],f_pos[1]+i[1]]
                    continue
            if (white_in_front and blank_in_back) or (white_in_back and blank_in_front):
                return False, b_count+f_count+2
            else:
                return True, 0
        move = [[1,1],[1,0],[0,1],[-1,-1],[0,-1],[-1,0],[-1,1],[1,-1]]
        for i in move:
            ate = 0
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
                    elif m[pos[0]+pos[1]*8] == c: break                        
                    else:
                        ate+=1
                        pos_t = tuple(pos)
                        aeh, loss = avoid_enemy_helper(pos, i)
                        if pos_reward  == {} or pos_t not in pos_reward:
                            if aeh:
                                pos_reward.update({pos_t : ate})
                            else:
                                pos_reward.update({pos_t : -loss})
                        elif pos_t in pos_reward:
                            if aeh:
                                pos_reward[pos_t] += ate-1
                            else:
                                pos_reward[pos_t] -= loss
                        break                                        
        return pos_reward
    def find_valid_step(self, obs):
        #retrun a dict
        #key: all the pos can move to
        #value: score that the agent will gain or lose
        exist_pos = self.get_2index_pos(obs)
        valid_list = []
        #risk_list = []
        def merge_pos_rewards(rs):
            merged_result = {}
            for r in rs:
                for k in r:
                    if k not in merged_result:
                        merged_result.update({k:r[k]})
                    else:
                        merged_result[k] += r[k]
            return merged_result
        for p in exist_pos:
            rew = self.find_pos(p, obs)
            valid_list.append(rew)            
        return merge_pos_rewards(valid_list)

    def get_available_action(self, obs): # return the positions agent can move to.
        available_pos = []
        pos_dict = self.find_valid_step(obs)
        for i in pos_dict:
            available_pos.append(i)
        return available_pos

class MyRandomAgent(MyBaseAgent): # a faster RandomAgent
    def step(self, reward, obs):
        available_actions = self.get_available_action(obs)
        x, y = random.choice(available_actions)
        return (self.col_offset + x * self.block_len, self.row_offset + y * self.block_len), pygame.USEREVENT

class MyAgent(MyBaseAgent):
    def step(self, reward, obs):
        # feature added: get corners first!
        cur_pos = self.get_2index_pos(obs)
        cur_enemy_pos = self.enemy_2index_pos(obs)
        pos_step = self.find_valid_step(obs)
        corner = [(0,0), (7,7), (7,0), (0,7)]
        better_pos = [(2,0), (5,0), (0,2), (7,2), (0,5), (7,5), (2,7), (5,7)]
        selected_position = (None, None)
        
        def avoid_cpos(pos_st):
            c_pos = [(1,0), (6,0), (0,1), (7,1), (0,6), (7,6), (1,7), (6,7)]
            n_pos = copy.deepcopy(pos_step)
            for i in c_pos:
                if i in pos_st:
                    n_pos.pop(i)
            if n_pos=={}: return pos_st
            else: return n_pos
        if len(cur_pos)+len(cur_enemy_pos)<30:
            pos_ano = avoid_cpos(pos_step)
            pos_step = copy.deepcopy(pos_ano)

        for i in corner:
            if i in pos_step:
                selected_position = (90+i[0]*60, 90+i[1]*60)
                return selected_position, pygame.USEREVENT
        if len(cur_pos)+len(cur_enemy_pos)<25:
            r = 0
            for i in better_pos:
                if i in pos_step:
                    if pos_step[i] > r:
                        selected_position = (90+i[0]*60, 90+i[1]*60)
                        r = pos_step[i]
                    else: continue
                    if selected_position==(None,None): break
                    return selected_position, pygame.USEREVENT
        rw = -64
        for i in pos_step:
            if pos_step[i] > rw:
                selected_position = (90+i[0]*60, 90+i[1]*60)
                rw = pos_step[i]  
        return selected_position, pygame.USEREVENT