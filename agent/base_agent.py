import random
import pygame
import sys
from pygame.constants import MOUSEBUTTONDOWN, MOUSEMOTION
import math

class BaseAgent():
    def __init__(self, color = "black", rows_n = 8, cols_n = 8, width = 600, height = 600):
        self.color = color
        self.rows_n = rows_n
        self.cols_n = cols_n
        self.block_len = 0.8 * min(height, width)/cols_n
        self.col_offset = (width - height)/2 + 0.1 * min(height, width) + 0.5 * self.block_len
        self.row_offset = 0.1 * min(height, width) + 0.5 * self.block_len
        

    def step(self, reward, obs):
        """
        Parameters
        ----------
        reward : dict
            current_score - previous_score
            
            key: -1(black), 1(white)
            value: numbers
            
        obs    :  dict 
            board status

            key: int 0 ~ 63
            value: [-1, 0 ,1]
                    -1 : black
                     0 : empty
                     1 : white

        Returns
        -------
        tuple:
            (x, y) represents position, where (0, 0) mean top left. 
                x: go right
                y: go down
        event_type:
            non human agent uses pygame.USEREVENT
        """

        raise NotImplementError("You didn't finish your step function. Please override step function of BaseAgent!")
     

    def find_valid_step(self,m):
        
        if self.color == 'black':
            c = -1
        else: c = 1


        exist_pos = []
        valid_list = []

        
        for i in m:
            if m[i] == c: #noted color change
                exist_pos.append((i%8, i//8))
        #print(exist_pos)
        for p in exist_pos:
        #print(p)
            valid_list.append(self.find_pos(p,m,c))
        #print(merge_pos_rewards(valid_list))
        return self.merge_pos_rewards(valid_list)
    

    def find_pos(self,t,m,c):
        pos_reward = {}
       
        move = [[1,1],[1,0],[0,1],[-1,-1],[0,-1],[-1,0],[-1,1],[1,-1]]
        for i in move:
            ate = 0
            edible = False
            tasty = False
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


    def valid_move(self,l):

            if l[0]<0 or l[0]>7 or l[1]<0 or l[1]>7:
                return False
            else: return True

    def merge_pos_rewards(self,rs):
        merged_result = {}
        for r in rs:
            for k in r:
                if k not in merged_result:
                    merged_result.update({k:r[k]})
                else:
                    merged_result[k] += r[k]
        return merged_result

'''
    def max_reward_move(self,obs):#return the most reward move
        valid_move = self.find_valid_step(obs)
        return max(valid_move,key = valid_move.keys)

    def minimax(self,position ,isblack_player,depth = 2):

        if depth == 0 :
            return position
        elif  isblack_player:
            maxeval = -math.inf
            
            for child in position:
                cur_eval = self.minimax(child,depth - 1 ,False)
                maxeval = max(maxeval,cur_eval)
            return maxeval
        else:  
            mineval = math.inf

            for child in position:
                cur_eval = self.minimax(child,depth - 1 ,True)
                maxeval = max(maxeval,cur_eval)
            return mineval
'''
#that's the algorithm i'm working with 


class HumanAgent(BaseAgent):
    def step(self, reward, obs):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEMOTION:
                return event.pos, event.type
            if event.type == pygame.MOUSEBUTTONDOWN:
                return event.pos, pygame.USEREVENT

        return (-1, -1), None


class RandomAgent(BaseAgent):
    def step(self, reward, obs):    
        pos_step = self.find_valid_step(obs)
        selected_position = random.choice(list(pos_step.keys()))
        x,y = selected_position
        pos = (90+x*60, 90+y*60)
        return pos,pygame.USEREVENT    
            
          
        

        
        #return (self.col_offset + random.randint(0, self.cols_n-1) * self.block_len, self.row_offset + random.randint(0, self.rows_n-1) * self.block_len), pygame.USEREVENT

        # return (-1,-1),pygame.USEREVENT

class MyAgent(BaseAgent):
    def step(self,reward,obs):
    
        pos_step = self.find_valid_step(obs)
        print(pos_step)
        corner_corner = [(0,0),(0,7),(7,0),(7,7)]
        selected_position = (None, None)
        for i in corner_corner:
            if i in pos_step:
                selected_position = (90+i[0]*60, 90+i[1]*60)
                return selected_position, pygame.USEREVENT


        corner = [(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (0, 6),
(7, 1), (7, 2), (7, 3), (7, 4), (7, 5), (7, 6), 
(1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0),
(1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7)]
        selected_position = (None, None)
        for i in corner:
            if i in pos_step:
                selected_position = (90+i[0]*60, 90+i[1]*60)
                return selected_position, pygame.USEREVENT

        rw = 0
        if selected_position == (None, None):
            for i in pos_step:
                if pos_step[i] > rw:
                    selected_position = (90+i[0]*60, 90+i[1]*60)
                    rw = pos_step[i]
        #print(type(selected_position))   
        return selected_position, pygame.USEREVENT

    


# if __name__ == "__main__":
#     agent = RandomAgent()
#     print(agent.step(None, None))
