import gwy
import gwyutils
import glob
import os
import sys
from math import fabs
import glib
import numpy as np
import scipy.signal

def block_filtr(spectr_tmp, spectr_fltr, file_name_tmp_b): ## function of spectrum treatment
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
	coords_x = []
	coords_y = []
	for i in range (numb):
		temp_str = ((str(spectr_tmp.itoxy(i))).replace('(', '')).replace(')', '')
		temp_list = str(temp_str).split(', ')
		coords_x.append(temp_list[0])
		coords_y.append(temp_list[1])
## Creating list of peaks
	n_order = 4 ## !!!!!FILTR ORDER!!!!!!
	max_rp = 0.01 ## !!!!!MAXIMUM PULSATION!!!!
	min_rs = 50 ## !!!!! DECAY!!!!!
	b, a = scipy.signal.ellip(n_order, max_rp, min_rs, 0.125)
	for i in range (0, numb-1, 1):
		data_line_tmp = spectr_tmp.get_spectrum(i)
		data_line_fltr = spectr_fltr.get_spectrum(i)
		arr_tmp = gwyutils.data_line_data_as_array(data_line_tmp)
		filtr_tmp = scipy.signal.filtfilt(b, a, arr_tmp)
		for j in range(0, nx_res-1, 1):
			print(filtr_tmp[j])
			data_line_fltr.set_val(j, filtr_tmp[j])
		spectr_fltr.set_spectrum(i, data_line_fltr)
	return spectr_fltr

file_list = glob.glob('/home/simora/STM_STS/OMICRON_DATA/*.par')##read file list from work dir /OMICRON_DATA
n_list = len(file_list)
for i in range(n_list):
	file_name = (os.path.basename(file_list[i]))[0:-8]
	try: ## exception exicting topography data .tf0
		container1 = gwy.gwy_file_load(file_list[i], gwy.RUN_NONINTERACTIVE) ##load file .par to gwy.container
		container2 = gwy.gwy_file_load(file_list[i], gwy.RUN_NONINTERACTIVE)
	except glib.GError:
		print('File  %s have not topography data' %file_name)
		with open('/home/simora/STM_STS/GAP/%s_topo_error.dat' % file_name, 'w') as file:
			file.write('File  %s_ori.par have not topography data' %file_name)
	else:
		gwy.gwy_app_data_browser_add(container1)
		gwy.gwy_app_data_browser_add(container2)	
		try: ## exception exicting spectroscopy data .sf0
			gwy.gwy_process_func_run('omicron', container1,  gwy.RUN_IMMEDIATE)##overload topography .tf0 and spectrography .sf0 data by omicron module
			gwy.gwy_process_func_run('spectro', container1,  gwy.RUN_IMMEDIATE)##include gwy.Spectra by spectro module
			spectr1 = container1['/sps/0']## spectroscopy is data field fron gwy.Container '/sps/0', here we have ONE spectra set!!!
		except KeyError:
			print('File %s have not spectroscopy data' % file_name)
			gwy.gwy_app_data_browser_remove(container1)
			gwy.gwy_app_data_browser_remove(container2)
			with open('/home/simora/STM_STS/GAP/%s_spectro_error.dat' % file_name, 'w') as file:
				file.write('File %s_ori.par have not spectroscopy data' % file_name)
		else :
			gwy.gwy_process_func_run('omicron', container1, gwy.RUN_IMMEDIATE)##overload topography .tf0 and spectrography .sf0 data by omicron module
			gwy.gwy_process_func_run('spectro', container1, gwy.RUN_IMMEDIATE)##include gwy.Spectra by spectro module
			gwy.gwy_process_func_run('omicron', container2, gwy.RUN_IMMEDIATE)
			gwy.gwy_process_func_run('spectro', container2, gwy.RUN_IMMEDIATE)
			spectr1 = container1['/sps/0']## spectroscopy is data field fron gwy.Container '/sps/0', here we have ONE spectra set!!!
			spectr2 = container2['/sps/0']
			block_filtr(spectr1, spectr2, file_name) ## function of spectrum treatment 
			gwy_app_file_write(container2, '/home/simora/STM_STS/OMICRON_DATA/%s_filtr.gwy' %file_name)
			gwy.gwy_app_data_browser_remove(container1)
			gwy.gwy_app_data_browser_remove(container2)	
print('／ﾌﾌ 　　　　　 　　 　ム｀ヽ\n' + '/ ノ)　　 ∧　　∧　　　　）　ヽ\n' + '/ ｜　　(´・ω ・`）ノ⌒（ゝ._,ノ\n' + '/　ﾉ⌒＿⌒ゝーく　 ＼　　／\n' + '丶＿ ノ 　　 ノ､　　|　/\n' + '　　 `ヽ `ー-‘人`ーﾉ /\n' + '　　　 丶 ￣ _人’彡ﾉ\n' + '　　　／｀ヽ _/\__')
