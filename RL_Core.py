import numpy as np
import pandas as pd

class RL(object):
    #初始化
    def __init__(self , actions_space , learning_rate = 0.1 , reward_decay = 0.9 , e_greedy = 0.9):
        self.actions = actions_space
        self.lr = learning_rate
        self.gamma = reward_decay
        self.epsilon = e_greedy
        self.sarsa_table = pd.DataFrame(columns = self.actions , dtype = np.float64)


    # 选择动作
    def choose_action(self , observation):
        self.check_and_update(observation)
        if np.random.rand() < self.epsilon:
            #  == 返回该数据的index的数值，然后挑一个选择 ==
            state_index_list = self.sarsa_table[0].tolist()
            k = state_index_list.index(observation)
            state_action = self.sarsa_table.loc[k , 1:]
            action = np.random.choice(state_action[state_action == np.max(state_action)].index) # 随机找一个最大的
        else:
            action = np.random.choice(self.actions[1:]) # 其他的随即找
        return action

    #检查并更新 Sarsa表
    def check_and_update(self , state):
        if state not in self.sarsa_table[0].tolist():
            self.sarsa_table = self.sarsa_table.append({0 : state , 1 : 0 , 2 : 0} , ignore_index = True)


class SarsaTable(RL):
    #继承 RL模块初始化
    def __init__(self , actions , learning_rate = 0.1 , reward_decay = 0.9 , e_greedy = 0.9):
        super(SarsaTable , self).__init__(actions , learning_rate , reward_decay , e_greedy)

    #学习
    def learn(self, s, a, r, next_s, next_a):
        # 检查是否在Q表中，不在就加进去
        self.check_and_update(next_s)

        # 找到对应的下标
        plane_row = self.sarsa_table[0].tolist()
        s_index = plane_row.index(s)
        next_s_index = plane_row.index(next_s)

        sarsa_predict = self.sarsa_table.loc[s_index , a]

        if r <= 0:
            sarsa_target = r + self.gamma * self.sarsa_table.loc[next_s_index , 1:].max()
        else:
            sarsa_target = r
        self.sarsa_table.loc[s_index , a] += self.lr * (sarsa_target - sarsa_predict)
        print(self.sarsa_table)
