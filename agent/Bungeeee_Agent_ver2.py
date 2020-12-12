from base_agent import BaseAgent

class MyAgent(BaseAgent):
    def step(self, rewards, obs):
        if self.color == 'black':
                c = -1
        else: c = 1
        
        def find_valid_step(m):
            exist_pos = []
            valid_list = []
            risk_list = []
            for i in m:
                if m[i] == c: #noted color change
                    exist_pos.append((i%8, i//8))
            #print(exist_pos)
            def find_pos(t):
                pos_reward = {}
                pos_risk = {}
                def valid_move(l):
                    #print(l)
                    if l[0]<0 or l[0]>7 or l[1]<0 or l[1]>7:
                        return False
                    else: return True
                def avoid_enemy_helper(pos, i):
                    if pos in [[0,0], [0,7], [7,7], [7,0]]:
                        return True
                    if valid_move([t[0]-i[0],t[1]-i[1]]) and m[(t[0]-i[0])+(t[1]-i[1])*8] == -c and valid_move([pos[0]+i[0],pos[1]+i[1]]) and m[(pos[0]+i[0])+(pos[1]+i[1])*8] == 0 :
                        return False
                    elif valid_move([t[0]-i[0],t[1]-i[1]]) and m[(t[0]-i[0])+(t[1]-i[1])*8] == c:
                        if not valid_move([t[0]-i[0]*2,t[1]-i[1]*2]):
                            return True
                        else:
                            pos_p = [t[0]-i[0]*2,t[1]-i[1]*2]
                            enemy = False
                            while not enemy:
                                if valid_move(pos_p):
                                    if m[pos_p[0]+pos_p[1]*8] == c:
                                        pos_p = [pos_p[0]-i[0], pos_p[1] - i[1]]
                                        continue
                                    elif m[pos_p[0]+pos_p[1]*8] == 0:
                                        if valid_move([pos[0]+i[0],pos[1]+i[1]]) and m[(pos[0]+i[0])+(pos[1]+i[1])*8] == -c:
                                            return False
                                        else:
                                            return True
                                        break
                                    else:
                                        enemy = True
                                        if valid_move([pos[0]+i[0],pos[1]+i[1]]) and m[(pos[0]+i[0])+(pos[1]+i[1])*8] == 0:
                                            return False
                                        else:
                                            return True
                                else: break
                            return True
                    return True
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
                            if m[pos[0]+pos[1]*8] == -c:
                                ate+=1
                                pos = [pos[0]+i[0], pos[1]+i[1]]
                            elif m[pos[0]+pos[1]*8] == c:
                                break
                            else:
                                ate+=1
                                pos_t = tuple(pos)
                                if pos_reward  == {} or pos_t not in pos_reward:
                                    if avoid_enemy_helper(pos, i):
                                        pos_reward.update({pos_t : ate})
                                    else:
                                        pos_reward.update({pos_t : -ate})
                                elif pos_t in pos_reward:
                                    if avoid_enemy_helper(pos, i):
                                        pos_reward[pos_t] += ate-1
                                    else:
                                        pos_reward[pos_t] -= ate
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
                rew = find_pos(p)
                valid_list.append(rew)
            #print(merge_pos_rewards(valid_list))
            return merge_pos_rewards(valid_list)
        pos_step = find_valid_step(obs)
        #print(pos_step)
        corner = [(0,0), (7,7), (7,0), (0,7)]
        selected_position = (None, None)
        for i in corner:
            if i in pos_step:
                selected_position = (90+i[0]*60, 90+i[1]*60)
                return selected_position, pygame.USEREVENT
        rw = -64
        for i in pos_step:
                if pos_step[i] > rw:
                        selected_position = (90+i[0]*60, 90+i[1]*60)
                        rw = pos_step[i]
        #print(type(selected_position))   
        return selected_position, pygame.USEREVENT
