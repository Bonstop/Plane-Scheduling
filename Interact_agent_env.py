from environment import Plane
from RL_Core import SarsaTable
import matplotlib.pyplot as plt

def update():
    for episode in range(6):
        print("第:{} 次".format(episode))
        cnt = 0
        #Step1: get the obervation of environment , observation is a list
        observation = env.reset()
        # Core choose action based on environment
        action = RL.choose_action(observation)
        while True:
            #更新环境
            observation = env.reset()

            # 下一个状态，奖励值
            next_observation , reward , R = env.next_change(action , observation)
            next_action = RL.choose_action(next_observation)

            #学习下一个状态的数据(s,a,r,s,a)
            RL.learn(observation , action , reward , next_observation , next_action)

            #swap observation
            observation = next_observation
            action = next_action
            cnt += 1
            a.append(R)
            # robust: the agent will die
            if cnt == 500:
                break




if __name__ == "__main__":
    n = 15
    a = []
    env = Plane()
    fcfs_record , fc_sum = env.Record(n)
    RL = SarsaTable(actions = list(range(env.n_actions)))
    update()

    rl_record , rl_sum = env.Record(n)

    # 绘制图像

    x_data = []
    b = []
    #print(a)
    for i in range(10):
        #i += 1
        #x_data.append(i)
        b.append(688)
    plt.plot(a , label = "RL" , marker = "o" , color = "blue" , linestyle = "-")
    plt.plot(b , label = "FCFS" , marker = "o" , color = "red" , linestyle = "-")
    #plt.plot(fcfs_record , label = "FCFS" , color = "blue" , linestyle = "-.")
    #plt.plot(rl_record , label = "reinforcement Learning" , color = "red" , linestyle = "-")
    plt.ylabel("Delay Time")
    plt.xlabel("Number of Iteration")
    #plt.annotate("FCFS_sum:"+str(fc_sum) + "\nRL_sum:" + str(rl_sum) ,  xy=(12,1))
    plt.legend()
    plt.show()

