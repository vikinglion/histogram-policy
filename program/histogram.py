#coding=utf-8
from matplotlib import pyplot as plt
import numpy as np
from gaussian_distribution import * 

def draw_result(histogram_dict, prewarm_win, keepalive_win, total_start, cold_start_num1, cold_start_num2, keepalive_time1, keepalive_time2):
	plt.subplot(212)
	x = np.arange(1, len(histogram_dict)+1)
	y = histogram_dict.values()
	# prewarm line
	x1 = prewarm_win
	y1 = max(y) + 5
	if prewarm_win:
		plt.plot([x1,x1],[y1, histogram_dict[prewarm_win]], color ='r', linewidth=1.5, linestyle="--")
	else:
		plt.plot([x1,x1],[y1, 0], color ='r', linewidth=1.5, linestyle="--")
	# keepalive line
	x2 = keepalive_win
	y2 = y1
	plt.plot([x2,x2],[y2, 0], color ='r', linewidth=1.5, linestyle="--")
	plt.bar(x, y)
	plt.xlabel('1-min bins', fontsize=15)
	plt.ylabel('Frequency', fontsize=15)
	plt.title("Histogram", fontsize=20)
	
	plt.subplot(221)
	labels1 = ['total starts','Fixed policy', 'Histogram policy']
	quants1 = [total_start, cold_start_num1, cold_start_num2]
	plt.bar(x=labels1, height=quants1, color='blue', alpha=0.8, width = 0.1)
	for x,y in zip(labels1,quants1):
		plt.text(x,y+0.05,'%i' %y, ha='center',va='bottom')
	plt.xticks(range(-1,4), fontsize=15)
	plt.title("Cold start number", fontsize=20)
	
	plt.subplot(222)
	labels2 = ['Fixed policy', 'Histogram policy']
	quants2 = [keepalive_time1, keepalive_time2]
	plt.bar(x=labels2, height=quants2, color='blue', alpha=0.8, width = 0.1)
	for x,y in zip(labels2,quants2):
		plt.text(x,y+0.05,'%i' %y, ha='center',va='bottom')
	plt.xticks(range(-1,3), fontsize=15)
	plt.title("Keep alive time(mins)", fontsize=20)
	plt.show()

random_num = 1000 # 随机生成的次数, 可能包含负数以及大于240
histogram_dict = {}

for minute in range(1,241):
	histogram_dict[minute] = 0

#random_activate = np.random.randint(0,10,[61])
#random_activate = np.random.normal(loc=0, scale=0.5, size=60)
#random_activate = np.random.randn(60)
#random_activate = (random_activate + 2) * 5
time_distribution = create_gaussain_distribution(0, 20, random_num)
random_activate_series = time_distribution
print(random_activate_series)
print('\n')

random_activate = []
# histogram plicy count
cold_start_num1 = 0
keepalive_time1 = 0
# traditional policy count
cold_start_num2 = 0
keepalive_time2 = 0
# default keepalive policy
prewarm_win = 0
keepalive_win = 10

for i in range(random_num):
	
	random_activate.append(random_activate_series[i])
	#print(len(random_activate), random_activate_series[i])
	
	# filter the negative value and beyond max value(4 hours)
	if random_activate_series[i] < 1:
		pass
	elif random_activate_series[i] > 240:
		pass
	else:
		histogram_dict[random_activate_series[i]] += 1
		cumu_count = []
		total_count = 0 
			
		for count in histogram_dict.values():
			total_count += count
			cumu_count.append(total_count)
		# 有效的总启动次数
		activate_num = cumu_count[-1] 

		prewarm_win_count = 0.05 * activate_num
		keepalive_win_count = 0.99 * activate_num
		
		# 统计直方图策略累积冷启动次数
		if random_activate_series[i] >= prewarm_win and random_activate_series[i] <= keepalive_win:
			pass
		else:
			cold_start_num2 += 1
		
		# 统计传统策略累积冷启动次数
		if random_activate_series[i] >= 20:
			cold_start_num1 += 1
			
		# 统计资源占用时间
		keepalive_time1 += 20
		keepalive_time2 += (keepalive_win - prewarm_win)
		
		# 根据当前的启动调整直方图以及预热窗和保留窗	
		mins = 0
		# 重置
		prewarm_win = 0
		prewarm_decide = False
		keepalive_win = 0
		keepalive_decide = False
		for count in cumu_count:
			mins += 1
			if count >= prewarm_win_count and not prewarm_decide:
				# prewarm_win length decrease 10% for error
				temp_mins = mins - 24
				if temp_mins < 0:
					prewarm_win = 0
				else:
					prewarm_win = temp_mins
				prewarm_decide = True
			if count >= keepalive_win_count and not keepalive_decide:
				# keepalive_win length increase 10% for error
				temp_mins = mins + 24
				if temp_mins > 240:
					keepalive_win = 240
				else:
					keepalive_win = temp_mins
				keepalive_decide = True

	

	
print("Total activate number:", cumu_count[-1], "\n")
print("Pre-warming windows:", prewarm_win, "Keepalive windows:", keepalive_win, "\n")
print("Traditional fixed keepalive policy:")
print("Cold start numbers:", cold_start_num1, "Keepalive time:", keepalive_time1)
print("Histogram policy:")
print("Cold start numbers:", cold_start_num2, "Keepalive time:", keepalive_time2, "\n")

draw_result(histogram_dict, prewarm_win, keepalive_win, cumu_count[-1], cold_start_num1, cold_start_num2, keepalive_time1, keepalive_time2)

