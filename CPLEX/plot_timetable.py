import matplotlib.pyplot as plt
import random


def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color


def plotTimetable(set_train, set_station, arriveTime, departTime):
    for i in set_train:
        color = randomcolor()
        for s in set_station:
            if s+1 in set_station:
                plt.plot([arriveTime[i, s], departTime[i, s]], [s, s], color=color)
            if s - 1 in set_station:
                plt.plot([arriveTime[i, s], departTime[i, s - 1]], [s, s - 1], color=color)
    plt.show()
