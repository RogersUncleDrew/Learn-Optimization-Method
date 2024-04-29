import docplex.mp.model as cpx


class MILP_model():
    def __init__(self):
        self.opt_model = cpx.Model(name="MILP")
        self.x1 = self.opt_model.continuous_var()  # x1 in continuous
        self.x2 = self.opt_model.continuous_var()  # x2 in continuous
        self.x3 = self.opt_model.integer_var()  # x3 in integer
        self.c1 = self.opt_model.add_constraint(ct=self.x1 + self.x2 >= 5.367)  # x1+x2>=5.367
        self.c2 = self.opt_model.add_constraint(ct=self.x2 + self.x3 >= 20.756)  # x2+x3>=20.756
        self.c3 = self.opt_model.add_constraint(ct=self.x1 + self.x3 >= 15.787)  # x1+x3>=15.787
        self.obj = self.opt_model.set_objective_expr(self.x1 + self.x2 + self.x3)  # min(x1+x2+x3)
        self.solveAndOutputResult()

    def solveAndOutputResult(self):
        self.sol = self.opt_model.solve()  # 开始求解模型
        x1 = self.sol.get_var_value(self.x1)  # 利用求解结果得到决策变量的取值 x1
        print("x1的求解结果为{0}".format(x1))
        print("x2的求解结果为{0}".format(self.sol.get_var_value(self.x2)))  # 利用求解结果得到决策变量的取值 x1
        print("x3的求解结果为{0}".format(self.sol.get_var_value(self.x3)))  # 利用求解结果得到决策变量的取值 x1
        print("目标函数为{0}".format(self.opt_model.objective_value))  # 利用模型得到模型求解的结果


MILP = MILP_model()
