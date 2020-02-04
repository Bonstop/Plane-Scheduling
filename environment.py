import pandas as pd
import numpy as np
import itertools
import math as ma
import random

# import form of timetable and the plane safety_distance
Timetable = pd.read_csv("F:/plane_information/timetable.csv" , nrows = 4 , usecols = [0 , 1 , 2 , 3 , 4])
Safety_distance = pd.read_csv("F:/plane_information/Safety_distance.csv" , nrows = 4 , usecols = [0 , 1 , 2 , 3])

class Plane(object):

    def __init__(self):
        super(Plane , self).__init__()
        self.action_space = ["state" , 1 , 2 , 3 , 4]
        self.n_actions = len(self.action_space)
        self.init_state = [0 , 0 , 0 , 0 , 0]

    #初始化状态集
    def init_start(self):
        n = 4
        for i in range(1 , n + 1):
            self.init_state[i] = 1
        return self.init_state

    # 更新这个表，并返回状态值
    def reset(self , record):
        # 更新一下数据
        n = len(record)
        sum_d_time = 0
        Timetable.loc[0:, 2:3] = 0
        
        #按照 record 直接计算数据拿到答案，不需要再去排序
        for i in range(1 , n):
            list_plane = Timetable["plane_id"].tolist()
            lp = list_plane.index(record[i])
            lp_1 = list_plane.index(record[i - 1])
            Timetable.loc[lp]["atd"] = Timetable.loc[lp_1]["atd"] + Safety_distance.loc[int(Timetable.loc[lp_1]["Size"])][int(Timetable.loc[lp]["Size"])]

            # 防止出现提前起飞现象，直接让它等着
            if Timetable.loc[lp]["atd"] < Timetable.loc[lp]["etd"]:
                Timetable.loc[lp]["atd"] = Timetable.loc[lp]["etd"]
            Timetable.loc[lp]["dtime"] = Timetable.loc[lp]["atd"] - Timetable.loc[lp]["etd"]
            #print(Timetable.loc[lp]["dtime"])
            sum_d_time += Timetable.loc[lp]["dtime"]
        return sum_d_time

    '''
    :当前状态
    :设置奖赏：如果 a飞机被选择了，还要再去选择，那就扣 10分。
    :         如果最后走到结果了，则加 10 分。
    :         没有走到结果，得 0 分。
    '''
    def next_change(self , action , s , record):
        reward = 0
        min_dtime = 68

        if s[action] == 0:
            reward -= 10
        if s == [0 , 0 , 0 , 0 , 0]:
            reward += 10
            if min_dtime < self.reset(record):
                min_dtime = this_dtime
                reward += 20
        else:
            reward += 0

        next_s = s.copy()
        next_s[action] = 0
        return next_s , reward

    def Record(self , n):
        #按照 FCFS 的顺序将飞机以FCFS序列排序得到延误时间
        record = []
        sum = 0
        ip = []

        #计算所有的延误时间
        ip.append(Timetable.loc[0]["plane_id"])
        for i in range(1 , n):
            Timetable.loc[i]["atd"] = Timetable.loc[i - 1]["atd"] + Safety_distance.loc[int(Timetable.loc[i - 1]["Size"])][int(Timetable.loc[i]["Size"])]
            Timetable.loc[i]["dtime"] = Timetable.loc[i]["atd"] - Timetable.loc[i]["etd"]
            ip.append(Timetable.loc[i]["plane_id"])
        id = Timetable["plane_id"].tolist()
        record = Timetable["dtime"].tolist()

        #将延误时间数据导出
        for i in range(n):
            sum += record[i]
        print("延误总时间：" , sum)
        print("飞机离港顺序：" , ip)
        print("飞机延误时间：" , record)
        return record , sum
