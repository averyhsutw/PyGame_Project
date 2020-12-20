# Reversi Game Project Report

### Team members
- Team leader:
    - name: Ya-hsuan HSU
    - student_id: b08902145
    - github: [averyhsutw](https://github.com/averyhsutw)
 - member:
    - name: Pang-chi LO
    - student_id: b08902146
    - github: [Bungeeee](https://github.com/Bungeeee)
 - member:
    - name: Chi-hei lei 
    - student_id: b09902089
    - github: [FrankyLei](https://github.com/FrankyLei)
    
### Report   (๑•̀ω•́)ノ(๑•̀ω•́)ノ(๑•̀ω•́)ノ

Each group memebers has their own agent. The following are the strategies and the algorithms we used.

- Avery:ʕ•ᴥ•ʔ
    - It's an improved version of Bungee's agent 3. Therefore, the way how to calculate the score of each position is described in the **Sean (Bungee)** part.
    - Strategies added:
        - strategy 1: avoid positions (1,0), (6,0), (0,1), (7,1), (0,6), (7,6), (1,7), (6,7).
        - strategy 2: get to positions (2,0), (5,0), (0,2), (7,2), (0,5), (7,5), (2,7), (5,7).
        - strategy 3: go to the position having the highest score.
    - When to change the strategy?
        - At first, I try to get to the corner. Hence, I use strategy 1 and 2. 
        - Then, change to strategy 3.
        - When is the timepoint to change strategies? I use Bungee_ver3 Agent and Franky's Agent to make these two agent play with my agent. Therefore I know when is the time to change strategies if my agent can beat these two agent. 

- Franky:( Φ ω Φ )
    - ~~Basically stole Sean (Bungee)'s get_available_move~~ ⁄(⁄ ⁄•⁄ω⁄•⁄ ⁄)⁄ and make a agent based on minimax algorithm. 
    - Minimax algorithm calculate all the possible move'rewards in the following turn(the "depth number" in the program), and return the best move. **(minimize white's rewards, maximize black' rewards)** (ﾉ>ω<)ﾉ
    - Also added feature like corners first in my agent (,,・ω・,,)

- Sean (Bungee):
    - Calculate the reward of each move and then compute the max possible loss of it. Sum up the reward and loss and store it in a dictionary as { position : sum(reward:+1:, loss:-1:) }
    - 4 corners are prior to others in selection while they're avalible 
    - Otherwise, use the dictionary of positions which is mentioned above to select the best position for the next move via Greedy Algorithm. :yum: 

At the end, we choose the agent of Avery's version just because it can beat the other two. We can not sure which agent of us can win more if we play with other group's agents. ~~We gamble anyway.~~(⁎⁍̴̛ᴗ⁍̴̛⁎)
