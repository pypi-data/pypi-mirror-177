import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import math
import copy
from geopy.distance import geodesic
import heapq
from sklearn.neighbors import NearestNeighbors
from scipy.optimize import curve_fit
from scipy.spatial.distance import cdist

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

class U_ST:      #univariate Space&Time
    def __init__(self):
        self.distances, self.indices, self.distances_k, self.indices_k = [], [], [], []
        self.l0, self.l, self.C0 = 0, 0, 0
        self.weight_list, self.weight_index, self.P = [], [], []
        self.filter_count, self.lvbo_count, self.RL_list = 0, 0, [0]
        self.cc, self.C, self.A, self.B, self.x, self.y = 0, 0, 0, 0, [], []

    # -----------------------------------------------------------------------------------------------------------定义抽象的函数
    # --------------------------------------------------------------------------------------------------计算k近邻
    def nbrs_k(self, n_k, count_k, k):
        nbrs = NearestNeighbors(n_neighbors=n_k, algorithm='ball_tree').fit(count_k)
        self.distances, self.indices = nbrs.kneighbors(count_k)
        self.distances_k, self.indices_k = np.array(copy.copy(self.distances[:, 1:k])), np.array(copy.copy(self.indices[:, 1:k]))
    # --------------------------------------------------------------------------------------------------计算l与l0
    def l0_l(self):
        self.l0 = np.mean(self.distances_k)
        self.l = pow(2, 0.5) * self.l0  # l表示基本游动区间半径
    # --------------------------------------------------------------------------------------------------计算权重
    def weight(self, count):
        for m in range(count):
            list = self.distances[m]  # 矩阵形式
            list = list.tolist()
            self.weight_list.append([t for t in list if t < self.l])  # 寻找游动区间内的点的距离
            self.weight_index.append(self.indices[m][0:len(self.weight_list[m])])
            P_pa = []
            for i in range(len(self.weight_index[m])):  # 计算权重
                P_pa.append(4 * math.exp(-0.693 * (self.weight_list[m][i] / self.l0) ** 2))
            self.P.append(P_pa)

        #print("weight_list: ", self.weight_list)   #输出权重值
        #print("weight_index: ", self.weight_index)   #输出权重值对应的点值
        print("P: ", self.P)
    # --------------------------------------------------------------------------------------------------滤波
    def lvbo(self, data, count1, count2):  # 定义滤波函数
        G, R, G_list = 0.0, 0.0, []
        for t in range(count1):
            G_list_ave = []
            for m in range(count2):
                pq = 0
                for n in range(len(self.weight_index[m])):  # len(index_weight[m])为游动区间内点的个数
                    if(np.isnan(data[t][self.weight_index[m][n]])==0):
                        pq = pq + self.P[m][n] * data[t][self.weight_index[m][n]]  # 算出pq的和
                G_list_ave.append(pq / sum(self.P[m]))  # 算出新的q值
            G_list.append(G_list_ave)
        G = np.nanmean(np.nanvar(G_list, axis=1))  # 算出G(L)
        R = self.C0 - G
        return G_list, R

    def filter(self, data, count1, count2):
        R1, R2 = 0, 0
        G1list = []  # k-1遍滤波的q值
        G2list = copy.copy(data)  # k遍滤波的q值
        T = 1
        while T > 0.03:  # 滤波终止条件：Ta=(R2-R1)/R2<=0.08,多滤几遍
            R1 = R2
            G1list = copy.copy(G2list)
            G2list, R2 = self.lvbo(G1list, count1, count2)
            self.RL_list.append(R2)
            self.lvbo_count = self.lvbo_count + 1
            T = (R2 - R1) / R2
            if (T > 0.08):  # 滤波终止条件：Ta=(R2-R1)/R2<=0.08
                self.filter_count = self.filter_count + 1
        self.filter_count = self.filter_count + 1
    # -------------------------------------------------------------------------------------------------求解c
    def Cal_C(self):
        VR = self.cc / (self.C0 * self.lvbo_count * self.l)
        self.C = 2 * (1 - VR)  # 0.5<=c<=1.5
        self.C = round(self.C, 3)
        if self.C > 1.5 or self.C < 0.5:
            self.C = 1
    # -------------------------------------------------------------------------------------------------求解参数
    def func(self, x, A, B):
        x = x + 0.001
        return A * np.exp(-B / x ** self.C)
    # -------------------------------------------------------------------------------------------------拟合曲线
    def curve(self):
        self.cc = (np.nansum(self.RL_list) - 0.5 *self.RL_list[len(self.RL_list) - 1]) * self.l
        self.Cal_C()

        for i in range(len(self.RL_list)):
            self.x.append(i * self.l)
        popt, pcov = curve_fit(self.func, self.x, self.RL_list, [1000, 1])
        self.A, self.B = popt[0], popt[1]
        for i in range(len(self.x)):
            self.y.append(self.func(self.x[i], self.A, self.B))
    # -------------------------------------------------------------------------------------------------绘制曲线
    x_tick = [0, 'L', '2L', '3L', '4L', '5L', '6L', '7L', '8L', '9L', '10L',
              '11L', '12L', '13L', '14L', '15L', '16L', '17L', '18L', '19L', '20L']

    def plot_curve(self):
        print("\tl(X值): ", self.x)
        print("\tR(l)(计算值）: ", self.RL_list)
        print("\tR(l)(拟合值）：", self.y)

        fig = plt.figure(figsize=(8, 6), dpi=100)

        plot1 = plt.plot(self.x, self.RL_list, 'o', label='计算值')
        plot2 = plt.plot(self.x, self.y, 'r-', label='拟合值')

        plt.axhline(y=self.C0, color='black', linestyle='-', alpha=0.3)
        plt.axhline(y=self.C0 / 2, color='black', linestyle='-', alpha=0.3)
        plt.axvline(x=self.l * self.filter_count, color='red', linestyle='-', alpha=0.2, label='滤波终止值')
        plt.text(0.0, self.C0 / 2, "C0/2", fontdict={'size': '14', 'color': 'black'}, alpha=0.3)
        plt.text(0.0, self.C0 , "C0", fontdict={'size': '14', 'color': 'black'}, alpha=0.3)
        plt.grid(True, linestyle='--', alpha=0.5)
        plt.xlabel('L/m')
        plt.ylabel('R(L)')
        plt.xticks(self.x, self.x_tick[:len(self.x)])
        plt.legend(loc='best')
