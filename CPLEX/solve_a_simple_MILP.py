import docplex.mp.model as cpx


class MILP_model_1():
    def __init__(self):
        self.opt_model = cpx.Model(name="MILP")
        self.x1 = self.opt_model.integer_var()  # x1 in integer
        self.x2 = self.opt_model.integer_var()  # x2 in integer
        self.x3 = self.opt_model.binary_var()  # x3 in binary
        self.c1 = self.opt_model.add_constraint(ct=self.x1 - self.x2 +self.x3 *200<= 200)  # x1-x2+x3*200<=200
        self.c2 = self.opt_model.add_constraint(ct=self.x1 - self.x2 + self.x3 * 200 >= 20)  # x1-x2+x3*200>=20
        self.c3 = self.opt_model.add_constraint(ct=self.x2 - self.x1 + (1-self.x3) * 200 <= 200)  # x1-x2+(1-x3)*200<=200
        self.c4 = self.opt_model.add_constraint(ct=self.x2 - self.x1 + (1-self.x3) * 200 >= 20)  # x1-x2+(1-x3)*200>=20
        self.c5 = self.opt_model.add_constraint(ct=self.x1 <= 80)  # x1<=80
        self.c6 = self.opt_model.add_constraint(ct=self.x1 >= 30)  # x1>=30
        self.c7 = self.opt_model.add_constraint(ct=self.x2 <= 50)  # x2<=50
        self.c8 = self.opt_model.add_constraint(ct=self.x2 >= 30)  # x2>=30
        self.obj = self.opt_model.set_objective_expr(self.x1 + self.x2)  # min(x1+x2)
        self.solveAndOutputResult()

    def solveAndOutputResult(self):
        self.sol = self.opt_model.solve()  # 开始求解模型
        x1 = self.sol.get_var_value(self.x1)  # 利用求解结果得到决策变量的取值 x1
        print("x1的求解结果为{0}".format(x1))
        print("x2的求解结果为{0}".format(self.sol.get_var_value(self.x2)))  # 利用求解结果得到决策变量的取值 x1
        print("x3的求解结果为{0}".format(self.sol.get_var_value(self.x3)))  # 利用求解结果得到决策变量的取值 x1
        print("目标函数为{0}".format(self.opt_model.objective_value))  # 利用模型得到模型求解的结果


MILP = MILP_model_1()


class MILP_model_2():
    def __init__(self):
        self.opt_model = cpx.Model(name="MILP")
        self.x1 = self.opt_model.integer_var(lb=30,ub=80)  # x1 in integer 30<=x1<=80
        self.x2 = self.opt_model.integer_var(lb=30,ub=50)  # x2 in integer 30<=x2<=50
        self.x3 = self.opt_model.binary_var()  # x3 in binary
        self.c1 = self.opt_model.add_constraint(ct=self.x1 - self.x2 +self.x3 *200<= 200)  # x1-x2+x3*200<=200
        self.c2 = self.opt_model.add_constraint(ct=self.x1 - self.x2 + self.x3 * 200 >= 20)  # x1-x2+x3*200>=20
        self.c3 = self.opt_model.add_constraint(ct=self.x2 - self.x1 + (1-self.x3) * 200 <= 200)  # x1-x2+(1-x3)*200<=200
        self.c4 = self.opt_model.add_constraint(ct=self.x2 - self.x1 + (1-self.x3) * 200 >= 20)  # x1-x2+(1-x3)*200>=20
        self.obj = self.opt_model.set_objective_expr(self.x1 + self.x2)  # min(x1+x2)
        self.solveAndOutputResult()

    def solveAndOutputResult(self):
        self.sol = self.opt_model.solve()  # 开始求解模型
        x1 = self.sol.get_var_value(self.x1)  # 利用求解结果得到决策变量的取值 x1
        print("x1的求解结果为{0}".format(x1))
        print("x2的求解结果为{0}".format(self.sol.get_var_value(self.x2)))  # 利用求解结果得到决策变量的取值 x1
        print("x3的求解结果为{0}".format(self.sol.get_var_value(self.x3)))  # 利用求解结果得到决策变量的取值 x1
        print("目标函数为{0}".format(self.opt_model.objective_value))  # 利用模型得到模型求解的结果

MILP=MILP_model_2()
