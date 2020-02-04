from environment import Plane
from RL_Core import SarsaTable
import matplotlib.pyplot as plt

def update():
    min_d_time = 48
    range_record = []
    for episode in range(100):
        print("第:{} 次".format(episode))
        cnt = 0
        record = []

        #确定最初的状态和动作
        observation = env.init_start()
        action = RL.choose_action(observation)

        while True:
            #记录动作
            record.append(action)
            # 下一个状态，奖励值
            next_observation , reward = env.next_change(action , observation , record)
            next_action = RL.choose_action(next_observation)
            # 追加奖励：如果本次效果比上次结束的时间早，则追加奖励，（必须在状态结束之前解决否则无法更新）
            if next_observation == [0 , 0 , 0 , 0 , 0] and len(record) == 4:
                this_d_time = env.reset(record)
                if min_d_time > this_d_time:
                    min_d_time = this_d_time
                    reward += 20

            #学习下一个状态的数据(s,a,r,s,a)
            RL.learn(observation , action , reward , next_observation , next_action)

            #给出下一个数据的奖励值和动作值
            observation = next_observation
            action = next_action

            # the end
            if observation == [0 , 0 , 0 , 0 , 0]:
                break
        range_record.append(min_d_time)
    return range_record


if __name__ == "__main__":
    n = 4
    a = []
    env = Plane()
    fcfs_record , fc_sum = env.Record(n)
    RL = SarsaTable(actions = list(range(env.n_actions)))
    finall = update()
    print(finall)
    #rl_record , rl_sum = env.Record(n)

    # 绘制图像

    x_data = []
    b = []
    #print(a)
    for i in range(100):
        #i += 1
        #x_data.append(i)
        b.append(48)
    plt.plot(finall , label = "RL" , marker = "o" , color = "blue" , linestyle = "-")
    plt.plot(b , label = "FCFS" , marker = "o" , color = "red" , linestyle = "-")
    #plt.plot(fcfs_record , label = "FCFS" , color = "blue" , linestyle = "-.")
    #plt.plot(rl_record , label = "reinforcement Learning" , color = "red" , linestyle = "-")
    plt.ylabel("Delay Time")
    plt.xlabel("Number of Iteration")
    #plt.annotate("FCFS_sum:"+str(fc_sum) + "\nRL_sum:" + str(rl_sum) ,  xy=(12,1))
    plt.legend()
    plt.show()

