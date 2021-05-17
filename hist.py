import gwy
import gwyutils
import glob
import os
import glib
import scipy.stats as sps
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

def block_hist(file_tmp):## function reading ONE file from list
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
		for i in range (nlns):
			str_tmp = lines[i].split()
			gap.append(float(str_tmp[2]))
		np_gap = np.array(gap)
		bins_hist = 10 ##!!!!!NUMBER OF INTERVAL!!!!!!!!!!!!!!!!
		hist, bin_edges0 = np.histogram(np_gap, bins=bins_hist)
		bin_edges = np.delete(bin_edges0, 0)
		fig_hist = plt.figure()
		fig_hist, ax_hist = plt.subplots()
		ax_hist = plt.bar(bin_edges, hist)
		fig_hist.savefig('/home/simora/STM_STS/DISTRIBUTION/%s_gap_hist.png' % file_name, dpi = 600)
		with open('/home/simora/STM_STS/DISTRIBUTION/%s_gap_hist.dat' % file_name, 'w') as file:
			file.write('gap value interval\t' + 'gap value frequency\n')
			for i in range(bins_hist):
				file.write('%s\t' % bin_edges[i])
				file.write('%s\n' % hist[i])
		file.close()
	pass

file_list = glob.glob('/home/simora/STM_STS/GAP/*_gap.dat')##read file list from work dir /OMICRON_DATA
n_list = len(file_list)
for i in range(n_list):
	block_hist(file_list[i])## function reading ONE file from list	
print('／ﾌﾌ 　　　　　 　　 　ム｀ヽ\n' + '/ ノ)　　 ∧　　∧　　　　）　ヽ\n' + '/ ｜　　(´・ω ・`）ノ⌒（ゝ._,ノ\n' + '/　ﾉ⌒＿⌒ゝーく　 ＼　　／\n' + '丶＿ ノ 　　 ノ､　　|　/\n' + '　　 `ヽ `ー-‘人`ーﾉ /\n' + '　　　 丶 ￣ _人’彡ﾉ\n' + '　　　／｀ヽ _/\__')
