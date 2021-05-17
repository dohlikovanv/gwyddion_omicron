import gwy
import gwyutils
import glob
import os
import sys
from math import fabs
import glib
import numpy as np
import scipy.signal
import matplotlib.pyplot as plt
import matplotlib as mpl

def block_volt_coord(spectr_tmp): ## function of spectrum treatment
	numb = spectr_tmp.get_n_spectra()##number of SPECTRUM in SPECTRA SET
	data_line1 = spectr_tmp.get_spectrum(0)## get data line
## Creating list of voltage
	voltage = []
	nx_res = data_line1.get_res()
	nx_real = data_line1.get_real()
	nx_offset = data_line1.get_offset()
	nx_dx = nx_real/nx_res
	delta = 0
	for i in range(nx_res):
		volt_x = nx_offset + delta
		voltage.append(volt_x)
		delta = delta + nx_dx
## Creating list of cordinates
	coord_x = []
	coord_y = []
	for i in range (numb):
		temp_str = ((str(spectr_tmp.itoxy(i))).replace('(', '')).replace(')', '')
		temp_list = str(temp_str).split(', ')
		coord_x.append(temp_list[0])
		coord_y.append(temp_list[1])
	return voltage, coord_x, coord_y
	
def block_peaks(data_line_tmp, voltage_tmp):
## Creating list of peaks
	widths = np.arange(0.2, 0.6) # !!!!!PEAKS WIDTHS!!!!! 
	max_distances=np.arange(0.8, 0.9) ## !!!!!VOLTAGE PEAKS DISTANCE!!!!!
	gap_thresh = 1.0## !!!!!MAX VOLTAGE PEAK DISTANCE!!!!!!
	min_snr = 0.001 ##!!!!!MINIMUM SIGNAL-NOISE RATIO
	voltage_peaks_tmp = []
	arr_tmp = gwyutils.data_line_data_as_array(data_line_tmp)
	ind_tmp = scipy.signal.find_peaks_cwt(arr_tmp, widths, max_distances=np.arange(0.1, 0.15), gap_thresh = 0.5, min_snr = 0.001)
	for j in (ind_tmp):## find voltage peaks
		voltage_peaks_tmp.append(voltage_tmp[j])
	return voltage_peaks_tmp
	
container1 = gwy.gwy_app_data_browser_get_current(gwy.APP_CONTAINER) ##load file .par to gwy.container
spectr1 = container1['/sps/0']## spectroscopy is data field fron gwy.Container '/sps/0', here we have ONE spectra set!!!
voltage, coord_x, coord_y = block_volt_coord(spectr1)
numb = spectr1.get_n_spectra()
coord_x_slc = []
coord_y_slc = []
voltage_peaks = []
for i in range(0, numb, 1):
	bl = spectr1.get_spectrum_selected(i)
	if bl == True:
		coord_x_slc.append(coord_x[i])
		coord_y_slc.append(coord_y[i])
		data_line_i = spectr1.get_spectrum(i)
		voltage_peaks_i = block_peaks(data_line_i, voltage) ## function of spectrum treatment
		voltage_peaks = voltage_peaks + voltage_peaks_i
n_dots = len(voltage_peaks)
np_voltage_peaks = np.array(voltage_peaks)
bins_hist = 40
hist_peaks, bin_edges0 = np.histogram(np_voltage_peaks, bins = bins_hist)
bin_edges = np.delete(bin_edges0, 0)
fig_hist = plt.figure()
fig_hist, ax_hist = plt.subplots()
ax_hist = plt.bar(bin_edges, hist_peaks)
fig_hist.savefig('/home/simora/STM_STS/PEAKS/%s_gap_hist.png' % (n_dots), dpi = 600)
with open('/home/simora/STM_STS/PEAKS/%s.dat' % (n_dots), 'w') as file:
	file.write('voltage value interval\t' + 'voltage value frequency\n')
	for i in range (40):## read spectrum from spectra set, numb - numder of spectrum, nx_res - number of points in this spectrum
		file.write('%s\t' % bin_edges[i])
		file.write('%s\n' % hist_peaks[i])
file.close()
#gwy.gwy_app_data_browser_remove(container1)
print('／ﾌﾌ 　　　　　 　　 　ム｀ヽ\n' + '/ ノ)　　 ∧　　∧　　　　）　ヽ\n' + '/ ｜　　(´・ω ・`）ノ⌒（ゝ._,ノ\n' + '/　ﾉ⌒＿⌒ゝーく　 ＼　　／\n' + '丶＿ ノ 　　 ノ､　　|　/\n' + '　　 `ヽ `ー-‘人`ーﾉ /\n' + '　　　 丶 ￣ _人’彡ﾉ\n' + '　　　／｀ヽ _/\__')
