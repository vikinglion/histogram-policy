#coding=utf-8
import numpy as np
import matplotlib.pyplot as plt
import math

def create_gaussain_distribution(loc=30, sigma=10, num=100):
	# �������Ĭ�Ͼ�ֵΪ30����̬�ֲ�
	random_time = loc + sigma * np.random.randn(num)  # 60Ϊ����������ĸ���
	for i in range(num):
		random_time[i] = math.ceil(random_time[i])
	return random_time	
	
def draw_histogram(distribution):	
	plt.style.use('ggplot')
	fig = plt.figure()  # ��ʼ������
	ax1 = fig.add_subplot(1, 2, 1)
	ax1.hist(distribution, bins=60, color='yellow')  # ��ʾ�ֳ�60�ݣ�������60��ֱ��ͼ�����̬�ֲ���ͼ
	ax2 = fig.add_subplot(1, 2, 2)
	ax2.hist(distribution, bins=60, color='green')
	plt.show()

#time_distribution = create_gaussain_distribution()
#draw_histogram(time_distribution)
