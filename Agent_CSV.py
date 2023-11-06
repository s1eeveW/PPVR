import pandas as pd
import numpy as np

# path = r'/datasets/virtualhome_22_classes/samples/0_0_0_Female2_0.hdf5'

from sklearn.decomposition import PCA
import math
import os
import h5py
import numpy as np
import pandas as pd
# 5

x = []
y = []
z = []

# 将生成的CSV文件的范围控制在100x100内，这是之后heatmaps的精度.
test1 = np.zeros((100, 100))
test2 = np.zeros((100, 100))
test3 = np.zeros((100, 100))

scen = 5
room = 2

# 7
agents = ["Male1", "Male2", "Male6", "Male10", "Female1", "Female2", "Female4"]
# agents = ["Male1"]

for agent in agents:
    for i in range(0, 852):
        # if not os.path.exists('./picture/samples/' + str(scen) + '_' + str(room) + '_' + str(i) + '_' + str(agent) + '_0.hdf5'):
        #     continue
        dataset = h5py.File('E:/Programming/Datasets/samples/' + str(scen) + '_' + str(room) + '_' + str(i) + '_' + str(agent) + '_0.hdf5', 'r')

        for l in range(dataset['skeleton_joints'].shape[0]):
            # 提取数据, 第10列是headset的位置数据, 第0个是hip joint的.
            joint = dataset['skeleton_joints'][l, 10]

            # joint的维度是x, y, z的相对位置数据.
            x.append(float(joint[0]))
            # print(x)

            y.append(float(joint[1]))
            # print(y)

            z.append(float(joint[2]))
            # print(z)


        combine = list(zip(x, y, z))
        combine = np.array(combine)

        # 方便后续计算
        combine = combine.transpose(1, 0)

        # 确认两个维度的最大值与最小值, 为了求heatmap相邻坐标间的相差值.
        left = min(combine[0])
        right = max(combine[0])
        minimum = min(combine[1])
        maximum = max(combine[1])
        up = max(combine[2])
        bottom = min(combine[2])



        vertical = float(up - bottom)
        y_axis = float(maximum - minimum)
        horizontal = float(right - left)

        # 精度100：
        # diff2 = float(vertical / 100)
        # diff1 = float(horizontal / 100)

        # 精度100(求heatmap相邻坐标间的相差值)：
        diff2 = float(vertical / 99)
        diff1 = float(horizontal / 99)
        diff3 = float(y_axis / 99)

        # # 确定每个数值落在heatmap的哪个坐标中，例如(3, 4).
        # for ip in range(0, combine.shape[1]):
        #     num1 = abs(combine[0, ip] - left)
        #     result1 = int(num1 / diff1)
        #
        #     num2 = abs(combine[2, ip] - bottom)
        #     result2 = int(num2 / diff2)
        #     test1[result1, 99 - result2] += 1
        #
        # # 保存成CSV文件, 方便heatmap文件直接读取并生成heatmaps.
        # pd.DataFrame(test1).to_csv('E:/Programming/Datasets/Agent_Heatmaps/CSV/' + str(scen) + '_' + str(room) + '_' + str(i) + '_' + str(agent) + '.csv')

        # 确定每个数值落在heatmap的哪个坐标中，例如(3, 4).
        for ip in range(0, combine.shape[1]):
            num1 = abs(combine[0, ip] - left)
            result1 = int(num1 / diff1)

            num2 = abs(combine[2, ip] - bottom)
            result2 = int(num2 / diff2)
            test1[result1, result2] += 1

        # 保存成CSV文件, 方便heatmap文件直接读取并生成heatmaps.
        pd.DataFrame(test1).to_csv('E:/Programming/Datasets/Agent_Heatmaps/CSV_xz/' + str(scen) + '_' + str(room) + '_' + str(i) + '_' + str(agent) + '.csv')

        # 确定每个数值落在heatmap的哪个坐标中，例如(3, 4).
        for ip in range(0, combine.shape[1]):
            num1 = abs(combine[0, ip] - left)
            result1 = int(num1 / diff1)

            num2 = abs(combine[1, ip] - minimum)
            result2 = int(num2 / diff3)
            test2[result1, result2] += 1

        # 保存成CSV文件, 方便heatmap文件直接读取并生成heatmaps.
        pd.DataFrame(test2).to_csv('E:/Programming/Datasets/Agent_Heatmaps/CSV_xy/' + str(scen) + '_' + str(room) + '_' + str(i) + '_' + str(agent) + '.csv')

        # 确定每个数值落在heatmap的哪个坐标中，例如(3, 4).
        for ip in range(0, combine.shape[1]):
            num1 = abs(combine[2, ip] - bottom)
            result1 = int(num1 / diff2)

            num2 = abs(combine[1, ip] - minimum)
            result2 = int(num2 / diff3)
            test3[result1, result2] += 1

        # 保存成CSV文件, 方便heatmap文件直接读取并生成heatmaps.
        pd.DataFrame(test3).to_csv('E:/Programming/Datasets/Agent_Heatmaps/CSV_zy/' + str(scen) + '_' + str(room) + '_' + str(i) + '_' + str(agent) + '.csv')

        x = []
        y = []
        z = []

        test1 = np.zeros((100, 100))
        test2 = np.zeros((100, 100))
        test3 = np.zeros((100, 100))
        print(str(agent) + " " + str(i) + " done")
        print()

