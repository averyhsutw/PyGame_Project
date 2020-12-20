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
                    white_in_back = False
                    white_in_front = False
                    blank_in_front = False
                    blank_in_back = False
                    b_pos = [t[0]-i[0],t[1]-i[1]]
                    f_pos = [pos[0]+i[0],pos[1]+i[1]]
                    f_count = 0
                    b_count = 0
                    while valid_move(b_pos):
                        #print('b', b_pos, i)
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
                    while valid_move(f_pos):
                        #print('f', f_pos, i)
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
