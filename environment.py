import pandas as pd
import numpy as np
import itertools
import math as ma
import random

# import form of timetable and the plane safety_distance
Timetable = pd.read_csv("F:/plane_information/timetable.csv" , nrows = 15 , usecols = [0 , 1 , 2 , 3 , 4 , 5 , 6])
Safety_distance = pd.read_csv("F:/plane_information/Safety_distance.csv" , nrows = 4 , usecols = [0 , 1 , 2 , 3])

class Plane(object):

    def __init__(self):
        super(Plane , self).__init__()
        self.action_space = ["state" , "Up" , "Stop"]
        self.n_actions = len(self.action_space)
        self.re = 0

    # 更新这个表，并返回动作值
    def reset(self):
        n = 15
        Timetable.loc[0: , 2:4] = 0
        Timetable.loc[0: , 5] = 1
        # 单独对第一架飞机提前进行处理：
        if Timetable.loc[0]["atd"] < Timetable.loc[0]["etd"]:
            Timetable.loc[0]["atd"] = Timetable.loc[0]["etd"]

        for i in range(1 , n):
            Timetable.loc[i]["atd"] = Timetable.loc[i - 1]["atd"] + Safety_distance.loc[int(Timetable.loc[i - 1]["Size"])][int(Timetable.loc[i]["Size"])]

            #杜绝提前起飞现象，直接让它等着
            if Timetable.loc[i]["atd"] < Timetable.loc[i]["etd"]:
                Timetable.loc[i]["atd"] = Timetable.loc[i]["etd"]

            Timetable.loc[i]["IPF"] = (Safety_distance.loc[int(Timetable.loc[i]["Size"])][3]) + (Timetable.loc[i]["atd"] - Timetable.loc[i]["etd"]) / Timetable.loc[i]["n"]
            Timetable.loc[i]["dtime"] = Timetable.loc[i]["atd"] - Timetable.loc[i]["etd"]
        s = Timetable["plane_id"].tolist()
        return Timetable["plane_id"].tolist()

    # 当前状态
    def next_change(self , action , s):

        # 找到当前最大的那个 K值，并对该状态的调整时间求和
        now_sum_dtime = 0
        k = 0
        f_ad = False
        max_dtime = -1
        for i in s[1: ]:
            temp_index = s.index(i)
            #print(temp_index)
            now_sum_dtime += Timetable.loc[temp_index]["dtime"]

            #针对提前飞的飞机做出标记,如果出现提前飞，马上标记
            if Timetable.loc[temp_index]["dtime"] < 0:
                f_ad = True
            if max_dtime < Timetable.loc[temp_index]["IPF"]:
                max_dtime = Timetable.loc[temp_index]["IPF"]
                k = temp_index

        #print("*********")
        #k = random.randint(1 , 19)
        #给出动作指令，使得飞机调整
        if action == 1: #该飞机起飞时间向前调整，交换两个飞机的起飞顺序
            temp = np.copy(Timetable.loc[k - 1])
            Timetable.loc[k - 1] = Timetable.loc[k]
            Timetable.loc[k] = temp
            Timetable.loc[k - 1]["n"] += 1
            Timetable.loc[k]["n"] += 1
        else:
            pass
            #该飞机不做调整
            #temp = np.copy(Timetable.loc[k + 1])
            #Timetable.loc[k + 1] = Timetable.loc[k]
            #Timetable.loc[k] = temp



        #将下一步保存，并且保存延迟时间和
        next_s = self.reset()
        next_sum_dtime = Timetable["dtime"].sum()

        #奖励值设计，总的延迟时间短变短，奖励 +1，不变 +0，增加 -1
        if next_sum_dtime < now_sum_dtime:
            reward = 50
        elif next_sum_dtime == now_sum_dtime:
            reward = 10
        else:
            reward = -100


        #返回
        return next_s , reward , next_sum_dtime

    def Record(self , n):
        #按照 FCFS 的顺序将飞机以FCFS序列排序得到延误时间
        record = []
        sum = 0
        ip = []
        #计算所有的延误时间
        ip.append(Timetable.loc[0]["plane_id"])
        for i in range(1, n):
            Timetable.loc[i]["atd"] = Timetable.loc[i - 1]["atd"] + Safety_distance.loc[int(Timetable.loc[i - 1]["Size"])][int(Timetable.loc[i]["Size"])]
            Timetable.loc[i]["dtime"] = Timetable.loc[i]["atd"] - Timetable.loc[i]["etd"]
            ip.append(Timetable.loc[i]["plane_id"])
            #print(Timetable.loc[i]["plane_id"] , Timetable.loc[i]["etd"] , Timetable.loc[i]["atd"])
        id = Timetable["plane_id"].tolist()
        record = Timetable["dtime"].tolist()


        #将延误时间数据导出

        for i in range(n):
            sum += record[i]
        print("延误总时间：" , sum)
        print("飞机离港顺序：" , ip)
        print("飞机延误时间：" , record)
        return record , sum
