import pandas as pd
import numpy as np
import random
'''
def update():
    Timetable = pd.read_csv("F:/plane_information/timetable.csv" , nrows = 3 , usecols = [0 , 1 , 2 , 3 , 4])
if __name__ == "__main__":
    update()
'''

a = []
b = []
for i in range(100):
    a.append(random.randrange(0 , 60 , 3))
    b.append(random.randint(0 , 2))
a.sort(reverse = False)
dataframe = pd.DataFrame({"etd" : a , "Size" : b})
dataframe.to_csv(r"F:\plane_information\open.csv")
print(a)
