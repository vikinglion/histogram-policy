#coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import math

def create_gaussain_distribution(loc=30, sigma=10, num=100):
	# 构造符合默认均值为30的正态分布
	random_time = loc + sigma * np.random.randn(num)  # 60为构造随机数的个数
	for i in range(num):
		random_time[i] = math.ceil(random_time[i])
	return random_time	
	
def draw_histogram(distribution):	
	plt.style.use('ggplot')
	fig = plt.figure()  # 初始化画板
	ax1 = fig.add_subplot(1, 2, 1)
	ax1.hist(distribution, bins=60, color='yellow')  # 表示分成60份，即会有60个直方图组成正态分布大图
	ax2 = fig.add_subplot(1, 2, 2)
	ax2.hist(distribution, bins=60, color='green')
	plt.show()

#time_distribution = create_gaussain_distribution()
#draw_histogram(time_distribution)
