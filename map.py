import gwy
import gwyutils
import glob
import os
import glib
import scipy.stats as sps
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def block_map(file_tmp):## function reading ONE file from list
	file_name = os.path.basename(file_tmp)[0:-8]
	with open(file_tmp, 'r') as file:
		lines = file.readlines()
	file.close()
	lines.pop(0)
	nlns = len(lines)
	if nlns == 0:
		pass
	else:
		gap = []
		xx = []
		yy = []
		x_cord = []
		y_cord = []
		for i in range (nlns):
			str_tmp = lines[i].split()
			xx.append(float(str_tmp[0])*1e+9)
			yy.append(float(str_tmp[1])*1e+9)
			gap.append(float(str_tmp[2]))
		[x_cord.append(x) for x in xx if x not in x_cord]
		[y_cord.append(y) for y in yy if y not in y_cord]
		np_x = np.array(x_cord)
		np_y = np.array(y_cord)		
		m = len(x_cord)
		n = len(y_cord)
		np_gap = np.zeros((m, n))
		k = 0
		for i in range (0, m-1, 1):
			for j in range (0, n-1, 1):
				np_gap[j][i] = gap[k]
				k = k + 1
		fig_gap = plt.figure()
		fig_gap, ax_gap = plt.subplots()
		lev_gap = [0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2]
		color_gap = np.zeros((12, 3))
		color_gap[:, 1:] = 0.2
		color_gap[:, 0] = np.linspace(0, 1, 12)
		contourf_gap = ax_gap.contourf(np_x, np_y, np_gap, levels = lev_gap, colors = color_gap)
		cbar_gap = fig_gap.colorbar(contourf_gap)
		ax_gap.set_xlabel('nm')
		ax_gap.set_ylabel('nm')
		fig_gap.savefig('/home/simora/STM_STS/MAP/%s_gap_map.png' % file_name, dpi = 600)
	pass

file_list = glob.glob('/home/simora/STM_STS/GAP/*_gap.dat')##read file list from work dir /OMICRON_DATA
n_list = len(file_list)
for i in range(n_list):
	block_map(file_list[i])## function reading ONE file from list	
print('／ﾌﾌ 　　　　　 　　 　ム｀ヽ\n' + '/ ノ)　　 ∧　　∧　　　　）　ヽ\n' + '/ ｜　　(´・ω ・`）ノ⌒（ゝ._,ノ\n' + '/　ﾉ⌒＿⌒ゝーく　 ＼　　／\n' + '丶＿ ノ 　　 ノ､　　|　/\n' + '　　 `ヽ `ー-‘人`ーﾉ /\n' + '　　　 丶 ￣ _人’彡ﾉ\n' + '　　　／｀ヽ _/\__')
