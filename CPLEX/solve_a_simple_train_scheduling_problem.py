import docplex.mp.model as cpx
import random
from plot_timetable import plotTimetable

M = 500


class MILP_model():
    def __init__(self, Ntrain, Nstation):
        self.Ntrain = Ntrain
        self.Nstation = Nstation
        self.set_train = range(Ntrain)
        self.set_station = range(Nstation)
        self.opt_model = cpx.Model(name="MILP")
        # 创建决策变量
        self.arriveTime = {(i, s): self.opt_model.integer_var(name="{0}车在{1}车站的到达时间".format(i, s), lb=1) for i in
                           self.set_train for s in self.set_station}
        self.departTime = {(i, s): self.opt_model.integer_var(name="{0}车在{1}车站的出发时间".format(i, s), lb=1) for i in
                           self.set_train for s in self.set_station}
        self.lambda_arrive = {(i, j, s): self.opt_model.binary_var(name="{0}车与{1}车在{2}车站的到达顺序".format(i, j, s)) for i in
                              self.set_train for j in self.set_train for s in self.set_station if i != j}
        self.lambda_depart = {(i, j, s): self.opt_model.binary_var(name="{0}车与{1}车在{2}车站的出发顺序".format(i, j, s)) for i in
                              self.set_train for j in self.set_train for s in self.set_station if i != j}
        # 添加约束条件
        self.c1 = {
            (i, s): self.opt_model.add_constraint(ct=self.departTime[i, s] - self.arriveTime[i, s] >= 3 * (i % 2)) for i
            in self.set_train for s in self.set_station}  # 所有奇数号车在每个车站要停站三分钟
        # self.c2 = {(i, s): self.opt_model.add_constraint(ct=self.departTime[i, s] - self.arriveTime[i, s] >= 0) for i in
        #            self.set_train for s in self.set_station}  # 所有车的出发时间大于等于到达时间
        self.c3 = {(i, s): self.opt_model.add_constraint(
            ct=self.arriveTime[i, s] - self.departTime[i, s - 1] >= 5 + random.randint(5, 20)) for
                   i in self.set_train for s in self.set_station if
                   s - 1 in self.set_station}  # 所有车在区间运行时间都至少为5分钟加上一个5到20分钟的随机数
        self.c4 = {(i, j, s): self.opt_model.add_constraint(
            ct=self.arriveTime[i, s] - self.arriveTime[j, s] + (1 - self.lambda_arrive[i, j, s]) * M <= M) for i in
            self.set_train for j in self.set_train for s in self.set_station if i != j}
        self.c5 = {(i, j, s): self.opt_model.add_constraint(
            ct=self.arriveTime[i, s] - self.arriveTime[j, s] + (1 - self.lambda_arrive[i, j, s]) * M >= 3) for i in
            self.set_train for j in self.set_train for s in self.set_station if i != j}
        self.c6 = {
            (i, j, s): self.opt_model.add_constraint(ct=self.lambda_arrive[i, j, s] + self.lambda_arrive[j, i, s] == 1)
            for i
            in self.set_train for j in self.set_train for s in self.set_station if i != j}
        self.c7 = {(i, j, s): self.opt_model.add_constraint(
            ct=self.departTime[i, s] - self.departTime[j, s] + (1 - self.lambda_depart[i, j, s]) * M <= M) for i in
            self.set_train for j in self.set_train for s in self.set_station if i != j}
        self.c8 = {(i, j, s): self.opt_model.add_constraint(
            ct=self.departTime[i, s] - self.departTime[j, s] + (1 - self.lambda_depart[i, j, s]) * M >= 3) for i in
            self.set_train for j in self.set_train for s in self.set_station if i != j}
        self.c9 = {
            (i, j, s): self.opt_model.add_constraint(ct=self.lambda_depart[i, j, s] + self.lambda_depart[j, i, s] == 1)
            for i
            in self.set_train for j in self.set_train for s in self.set_station if i != j}
        self.c10 = {
            (i, j, s): self.opt_model.add_constraint(ct=self.lambda_arrive[i, j, s] == self.lambda_depart[i, j, s - 1])
            for i in self.set_train for j in self.set_train for s in self.set_station if i != j if
                                                                                         s - 1 in self.set_station}
        self.c11 = {(i, j, s): self.opt_model.add_constraint(ct=i - j + (1 - self.lambda_depart[i, j, 0]) * M <= M) for
                    i in self.set_train for j in self.set_train for s in self.set_station if i != j} # 在始发站 列车按照编号依次发车
        self.c12 = {(i, j, s): self.opt_model.add_constraint(ct=i - j + (1 - self.lambda_depart[i, j, 0]) * M >= 0) for
                    i in self.set_train for j in self.set_train for s in self.set_station if i != j} # 在始发站 列车按照编号依次发车
        # 设置目标函数
        self.opt_model.set_objective_expr(sum(self.arriveTime[i, s] for i in self.set_train for s in self.set_station))
        self.opt_model.time_limit = 40
        self.sol = self.opt_model.solve()
        for i in self.set_train:
            for s in self.set_station:
                print("{0}车在{1}车站的到达时间为：{2}， 出发时间为：{3}".format(i, s, self.sol.get_var_value(self.arriveTime[i, s]),
                                                               self.sol.get_var_value(self.departTime[i, s])))
        self.ARRTime = {(i, s): self.sol.get_var_value(self.arriveTime[i, s]) for i in self.set_train for s in
                        self.set_station}
        self.DEPTime = {(i, s): self.sol.get_var_value(self.departTime[i, s]) for i in self.set_train for s in
                        self.set_station}


MILP = MILP_model(10, 10)
plotTimetable(MILP.set_train, MILP.set_station, MILP.ARRTime, MILP.DEPTime)
