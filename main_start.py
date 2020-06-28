# -*- coding: utf-8 -*-
import os,sys,copy,json
import subprocess
import datetime
import time
from USoS_lib import install_compile_package
from USoS_lib import create_acrn_kernel_deb
from USoS_lib import install_acrn_deb
from USoS_lib import install_acrn_kernel_deb
from USoS_lib import build_acrn_kernel
#parse json file
with open("config.json","r") as load_f:
	load_dict = json.load(load_f)
	print(load_dict)
load_f.close()


# build acrn
def build_acrn():
	if os.path.exists('acrn-hypervisor'):
		os.system('rm -rf acrn-hypervisor')

	cmd = 'git clone %s' % load_dict['acrn_repo']
	os.system(cmd)
	cmd = 'cd acrn-hypervisor' + "&&" +'git checkout -b mybranch %s'% load_dict['release_version']
	os.system(cmd)

	# industry
	cmd = 'cd acrn-hypervisor' + "&&" +'%s'% load_dict['build_source_cmd']
	os.system(cmd)

#create acrn deb
def create_acrn_deb():
	if os.path.exists('acrn_deb'):
		os.system('rm -rf acrn_deb')

	os.system('mkdir -p acrn_deb')

	cmd = "cd acrn_deb" + "&&" +"mkdir DEBIAN"
	os.system(cmd)

	cmd = "cd acrn_deb" + "&&" +"touch DEBIAN/control"
	os.system(cmd)

	#control file description
	make_info = load_dict['build_source_cmd']
	acrn_info = make_info.replace(' ','-').replace('=','-')

	listcontrol=['Package: acrn-package\n','version: %s \n'% datetime.date.today(),'Section: free \n','Priority: optional \n','Architecture: amd64 \n','Installed-Size: 66666 \n','Maintainer: Intel\n','Description: %s \n' % acrn_info,'\n']


	with open('acrn_deb/DEBIAN/control','w',encoding='utf-8') as fr:
			fr.writelines(listcontrol)

	#design in acrn_data

	with open("deb.json","r") as load_deb:
		deb_info = json.load(load_deb)

	load_deb.close()

	deb_info_list = list(deb_info)

	for i in deb_info_list:
		source = deb_info[i]['source']
		target = deb_info[i]['target']
		if os.path.exists(target):
			os.system('cp %s %s' % (source,target))
		else:
			os.system('mkdir -p %s' % target)
			os.system('cp %s %s' % (source,target))

	os.system('cp -r usr acrn_deb')
	os.system('rm -rf usr')

	os.system('cp -r boot acrn_deb')
	os.system('rm -rf boot')


	os.system('cp acrn-hypervisor.postinst acrn_deb/DEBIAN/postinst' )
	os.system('chmod +x acrn_deb/DEBIAN/postinst')
	os.system('sed -i \'s/\r//\' acrn_deb/DEBIAN/postinst')
	os.system('dpkg -b acrn_deb acrn_deb_package.deb ')



def main_process():

	#install compile package,after this, compile env ok
	if load_dict['install_package'] == 'true':
		print('start install compile package')
		install_compile_package()

	else:
		print('You decide NOT install compile package')

	if load_dict['build_acrn'] == 'true':
		print('start bild acrn/kernel')
		build_acrn()

	else:
		print('You decide NOT build ACRN')

	if load_dict['build_acrn_kernel'] == 'true':
		print('start bild acrn/kernel')
		build_acrn_kernel(load_dict['sos_kernel_repo'],load_dict['release_version'])

	else:
		print('You decide NOT build ACRN kernel')
	#create deb
	if load_dict['acrn_deb_package'] == 'true':
		print('start create ACRN deb package')
		create_acrn_deb()
	else:
		print('You decide NOT create ACRN deb')

	#install deb
	if load_dict['install_acrn_deb'] == 'true':
		print('start install through acrn deb package')
		install_acrn_deb()

	else:
		print('You decide NOT install ACRN through deb')
	#create deb
	if load_dict['acrn_kernel_deb_package'] == 'true':
		print('start create ACRN kernel deb package')
		create_acrn_kernel_deb()
	else:
		print('You decide NOT create ACRN kernel deb')

	#install deb
	if load_dict['install_acrn_kernel_deb'] == 'true':
		print('start install through acrn kernel deb package')
		install_acrn_kernel_deb()

	else:
		print('You decide NOT install ACRN through deb')

	if load_dict['auto_reboot'] == 'true':
		print('You decide to reboot!!!!!!!!!!!!!!!!!!!!!!!')
		os.system('reboot')

	else:
		print('You decide NOT reboot')
if __name__ == "__main__":
		main_process()