from base_agent import BaseAgent
class MyAgent(BaseAgent):
    def step(self, rewards, obs):
        if self.color == 'black':
                c = -1
        else: c = 1
        
        def find_valid_step(m):
            exist_pos = []
            valid_list = []
            for i in m:
                if m[i] == c: #noted color change
                    exist_pos.append((i%8, i//8))
            #print(exist_pos)
            def find_pos(t):
                pos_reward = {}
                def valid_move(l):
                    if l[0]<0 or l[0]>7 or l[1]<0 or l[1]>7:
                        return False
                    else: return True
                move = [[1,1],[1,0],[0,1],[-1,-1],[0,-1],[-1,0],[-1,1],[1,-1]]
                for i in move:
                    ate = 0
                    edible = False
                    tasty = False
                    pos = [t[0]+i[0], t[1]+i[1]]
                    if not valid_move(pos) or m[pos[0]+pos[1]*8] != -c: #noted color change
                        continue
                    else:
                        ate+=1
                        pos = [pos[0]+i[0], pos[1]+i[1]]
                        while valid_move(pos):
                            if m[pos[0]+pos[1]*8] == 1:
                                ate+=1
                                pos = [pos[0]+i[0], pos[1]+i[1]]
                            elif m[pos[0]+pos[1]*8] == -1:
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
                #print(p)
                valid_list.append(find_pos(p))
            #print(merge_pos_rewards(valid_list))
            return merge_pos_rewards(valid_list)
        pos_step = find_valid_step(obs)
        corner = [(0,0), (7,7), (7,0), (0,7)]
        selected_position = (None, None)
        for i in corner:
            if i in pos_step:
                i = selected_position
        rw = 0
        if selected_position == (None, None):
            for i in pos_step:
                if pos_step[i] > rw:
                    selected_position = (90+i[0]*60, 90+i[1]*60)
                    rw = pos_step[i]
        #print(type(selected_position))   
        return selected_position, pygame.USEREVENT
