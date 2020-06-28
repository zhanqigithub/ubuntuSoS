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
with open("release.json","r") as load_f:
	load_dict = json.load(load_f)
load_f.close()

with open("deb.json","r") as load_fdeb:
	load_dictdeb = json.load(load_fdeb)
load_fdeb.close()

# build acrn
def build_acrn():
	install_compile_package()
	if os.path.exists('acrn_release_img'):
		os.system('rm -rf acrn_release_img')
	os.system('mkdir -p acrn_release_img')
	cmd = 'git clone %s' % load_dict['acrn_repo']
	os.system(cmd)

	if not os.path.exists('acrn-hypervisor'):
		#os.system('rm -rf acrn-hypervisor')

		cmd = 'git clone %s' % load_dict['acrn_repo']
		os.system(cmd)
	cmd = 'cd acrn-hypervisor' + "&&" +'git checkout -b mybranch %s'% load_dict['release_version']
	os.system(cmd)

	# industry

	make_cmd_list =[]

	release = load_dict['build_cmd']['release']
	scenario = load_dict['build_cmd']['scenario']
	board = load_dict['build_cmd']['board']
	info_list = []

	for i in scenario:
		if scenario[i] == 'true':
			for j in board:
				if board[j] == 'true':
					info_list.append((i,j))
					make_cmd = 'make all BOARD_FILE=misc/acrn-config/xmls/board-xmls/%s.xml SCENARIO_FILE=misc/acrn-config/xmls/config-xmls/%s/%s.xml RELEASE=%s'%(j,j,i,release)
					make_cmd_list.append(make_cmd)

	for i in range(len(make_cmd_list)):
		cmd = 'cd acrn-hypervisor' + "&&" +'make clean'
		os.system(cmd)

		cmd = 'cd acrn-hypervisor' + "&&" +'%s'% make_cmd_list[i]
		os.system(cmd)

		bin_name ='acrn.%s.%s.bin' % (info_list[i][0],info_list[i][1])
		out_name ='acrn.%s.%s.32.out' % (info_list[i][0],info_list[i][1])
		efi_name ='acrn.%s.%s.efi' % (info_list[i][0],info_list[i][1])

		cmd = 'cp %s acrn_release_img/%s' %(load_dictdeb['acrn.bin']['source'],bin_name)
		os.system(cmd)

		cmd = 'cp %s acrn_release_img/%s' %(load_dictdeb['acrn.32.out']['source'],out_name)
		os.system(cmd)

		if os.path.exists(load_dictdeb['acrn.efi']['source']):
				cmd = 'cp %s acrn_release_img/%s' %(load_dictdeb['acrn.efi']['source'],efi_name)
				os.system(cmd)

	build_acrn_kernel(load_dict['sos_kernel_repo'],load_dict['release_version'])

def create_release_deb():

	path = 'acrn_release_deb'
	if os.path.exists(path):
		os.system('rm -rf acrn_release_deb')
	os.system('mkdir -p acrn_release_deb')
	cmd = "cd acrn_release_deb" + "&&" +"mkdir DEBIAN"
	os.system(cmd)

	cmd = "cd acrn_release_deb" + "&&" +"touch DEBIAN/control"
	os.system(cmd)

	#control file description
	acrn_info = load_dict['release_version']

	listcontrol=['Package: acrn-package\n','version: %s \n'% datetime.date.today(),'Section: free \n','Priority: optional \n','Architecture: amd64 \n','Installed-Size: 66666 \n','Maintainer: Intel\n','Description: %s \n' % acrn_info,'\n']


	with open('acrn_release_deb/DEBIAN/control','w',encoding='utf-8') as fr:
			fr.writelines(listcontrol)

	#design in acrn_data

	with open("deb.json","r") as load_deb:
		deb_info = json.load(load_deb)

	load_deb.close()

	deb_info_list = list(deb_info)

	for i in deb_info_list:
		source = deb_info[i]['source']
		target = deb_info[i]['target']
		if target == 'boot':
			continue
		if os.path.exists(target):
			os.system('cp %s %s' % (source,target))
		else:
			os.system('mkdir -p %s' % target)
			os.system('cp %s %s' % (source,target))

	os.system('cp -r usr acrn_release_deb')
	os.system('rm -rf usr')

	os.system('mkdir -p acrn_release_deb/boot')
	cmd = "mv acrn_release_img/acrn.* acrn_release_deb/boot"
	os.system(cmd)


	os.system('cp acrn-hypervisor.postinst acrn_release_deb/DEBIAN/postinst' )
	os.system('chmod +x acrn_release_deb/DEBIAN/postinst')
	os.system('sed -i \'s/\r//\' acrn_release_deb/DEBIAN/postinst')

	os.system('dpkg -b acrn_release_deb acrn_deb_package.deb ')

	create_acrn_kernel_deb()


def install_process():
	if load_dict['build_acrn'] == 'true':
		print('start build acrn')
		build_acrn()

	if load_dict['create_acrn_deb'] == 'true':
		print('start create acrn release deb')
		create_release_deb()

	if load_dict['install_acrn_deb'] == 'true':
		print('start install acrn release deb')
		install_acrn_deb()
		install_acrn_kernel_deb()
if __name__ == "__main__":
		install_process()