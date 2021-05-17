import gwy
import gwyutils
import glob
import os
import sys
from math import fabs
import glib
import numpy as np
import scipy.signal

def block_gap(spectr_tmp, file_name_tmp_b): ## function of spectrum treatment
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
## Creating list of gap
	homo = [0]*numb
	lumo = [0]*numb
	gap = []
	deriav = 5.00e-11##!!!!!!TUNNEL CURRENT DEVIATION!!!!!!!
	for i in range (0, numb-1, 1):
		data_line_tmp = spectr_tmp.get_spectrum(i)
		for j in range (0, nx_res-1, 1):
			temp_current = data_line_tmp.get_val(j)
			if fabs(temp_current) <= deriav and homo[i] == 0 and voltage[j] <= 0:
				homo[i] = voltage[j]
		for j in range(nx_res-1, 0, -1):	
			temp_current = data_line_tmp.get_val(j)
			if fabs(temp_current) <= deriav and lumo[i] == 0 and voltage[j] >= 0:
				lumo[i] = voltage[j]
## find gap
	for i in range(numb):
		gap.append(lumo[i] - homo[i])
	with open('/home/simora/STM_STS/GAP/%s_gap.dat' % file_name_tmp_b, 'w') as file:
		file.write('abciss\t' + 'ordinat\t' + 'gap value\n')
		for i in range (numb):
        	    file.write('%s\t' % coords_x[i])
        	    file.write('%s\t' % coords_y[i])
        	    file.write('%s\n' % gap[i])
	file.close()
	pass
	
def block_container(container_tmp, file_name_tmp): ## function loading spectroscopy container
	gwy.gwy_app_data_browser_add(container_tmp)	
	try: ## exception exicting spectroscopy data .sf0
		gwy.gwy_process_func_run('omicron', container_tmp,  gwy.RUN_IMMEDIATE)##overload topography .tf0 and spectrography .sf0 data by omicron module
		gwy.gwy_process_func_run('spectro', container_tmp,  gwy.RUN_IMMEDIATE)##include gwy.Spectra by spectro module
		spectr1 = container_tmp['/sps/0']## spectroscopy is data field fron gwy.Container '/sps/0', here we have ONE spectra set!!!
	except KeyError:
		print('File %s have not spectroscopy data' % file_name_tmp)
		gwy.gwy_app_data_browser_remove(container_tmp)
		with open('/home/simora/STM_STS/GAP/%s_gap.dat' % file_name_tmp, 'w') as file:
			file.write('File %s have not spectroscopy data' % file_name_tmp)
		pass
	else :
		gwy.gwy_process_func_run('omicron', container_tmp,  gwy.RUN_IMMEDIATE)##overload topography .tf0 and spectrography .sf0 data by omicron module
		gwy.gwy_process_func_run('spectro', container_tmp,  gwy.RUN_IMMEDIATE)##include gwy.Spectra by spectro module
		spectr1 = container_tmp['/sps/0']## spectroscopy is data field fron gwy.Container '/sps/0', here we have ONE spectra set!!!
		gwy.gwy_app_data_browser_remove(container_tmp)
		block_gap(spectr1, file_name_tmp) ## function of spectrum treatment 
	return block_gap

def block_file(file_tmp):## function reading ONE file from list
	file_name_ext = os.path.basename(file_tmp)
	file_name = file_name_ext[:-8]
	try: ## exception exicting topography data .tf0
		container1 = gwy.gwy_file_load(file_tmp, gwy.RUN_NONINTERACTIVE) ##load file .par to gwy.container
	except glib.GError:
		print('File  %s have not topography data' %file_name)
		with open('/home/simora/STM_STS/GAP/%s_gap.dat' % file_name, 'w') as file:
			file.write('File  %s have not topography data' %file_name)
		pass
	else:
		block_container(container1, file_name)## function loading spectroscopy container
	return block_container

file_list = glob.glob('/home/simora/STM_STS/OMICRON_DATA/*.par')##read file list from work dir /OMICRON_DATA
n_list = len(file_list)
for i in range(n_list):
	block_file(file_list[i])## function reading ONE file from list	
print('／ﾌﾌ 　　　　　 　　 　ム｀ヽ\n' + '/ ノ)　　 ∧　　∧　　　　）　ヽ\n' + '/ ｜　　(´・ω ・`）ノ⌒（ゝ._,ノ\n' + '/　ﾉ⌒＿⌒ゝーく　 ＼　　／\n' + '丶＿ ノ 　　 ノ､　　|　/\n' + '　　 `ヽ `ー-‘人`ーﾉ /\n' + '　　　 丶 ￣ _人’彡ﾉ\n' + '　　　／｀ヽ _/\__')
