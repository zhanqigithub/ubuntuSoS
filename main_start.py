# -*- coding: utf-8 -*-
import os,sys,copy,json
import subprocess
import datetime
import time

#parse json file
with open("config.json","r") as load_f:
	load_dict = json.load(load_f)
	print(load_dict)
load_f.close()

# 1st check env
version = os.popen('uname -a')
if load_dict['ubuntu_version'] in version.read():
	print('ubuntu version is expected')
else:
	print('ubuntu version not recommend!!!')


# 2nd install docker
def install_docker():
	version = os.popen('docker -v')
	if 'Docker version' in version.read():
		print('Docker already install')
	else:
		os.system('apt install docker.io -y')

def enable_docker():
	os.system('systemctl start docker')
	os.system('systemctl enable docker')
	version = os.popen('systemctl status docker')
	if 'active (running)' in version.read():
		print('Docker enabled')
	else:
		print('Docker broken!!!')
		exit()

def config_docker():
	os.system('mkdir -p /etc/systemd/system/docker.service.d')
	os.system('touch /etc/systemd/system/docker.service.d/http-proxy.conf')
	docker_proxy = 'Environment=' + load_dict['docker_proxy']
	with open('/etc/systemd/system/docker.service.d/http-proxy.conf','w') as f:
		f.write('[Service]\n')
		f.write(docker_proxy)
	os.system('systemctl daemon-reload')
	os.system('systemctl restart docker')
	os.system('systemctl show --property=Environment docker')

def docker_pull():
	ubuntu_version = load_dict['docker_image']
	os.system('docker image pull %s' % (ubuntu_version))
	docker_id_out = os.popen('docker ps -aq --filter name=%s' % load_dict['docker_name'])
	docker_id = docker_id_out.read().replace('\n', '').replace('\r', '')
	if not docker_id == None:
			print("acrn ubuntu docker %s alread exist, upgrade" % docker_id)
			os.system('docker stop %s' % docker_id)
			os.system('docker rm  %s' % docker_id)
	os.system('docker create -it --name %s %s' % (load_dict['docker_name'],load_dict['docker_image']))
	docker_id_out = os.popen('docker ps -aq --filter name=%s' % load_dict['docker_name'])
	docker_id = docker_id_out.read().replace('\n', '').replace('\r', '')
	print(docker_id)
	os.system('systemctl daemon-reload')
	os.system('systemctl restart docker')
	os.system('docker start %s' % docker_id)
	cmd  = 'docker cp %s %s:/home' % (load_dict['scripts_path'],docker_id)
	print(cmd)
	os.system('docker cp %s %s:/' % (load_dict['scripts_path'],docker_id))
	os.system('docker exec -it %s /bin/bash' % docker_id)
	#!!!!!!!!!!!You Enter Docker!!!!!!!!!!!!!!!!!!!!!!!!!!!

# 3rd install compile package
def install_compile_package():
	#check compile env
	os.system('apt install gcc \
     git \
     make \
     gnu-efi \
     libssl-dev \
     libpciaccess-dev \
     uuid-dev \
     libsystemd-dev \
     libevent-dev \
     libxml2-dev \
     libusb-1.0-0-dev \
     python3 \
     python3-pip \
     libblkid-dev \
     e2fslibs-dev \
     pkg-config \
     libnuma-dev -y')
	gcc_version_out = os.popen('gcc --version')
	gcc_version = gcc_version_out.read()
	if tuple(gcc_version.split(' ')[3].split("\n")[0].split(".")) < tuple(load_dict['gcc_version'].split('.')):
		print("your gcc version is too old")
	binutils_version_out = os.popen('ld -v')
	binutils_version = binutils_version_out.read().split(" ")
	if tuple(binutils_version[-1].split("\n")[0].split(".")) < tuple(load_dict['binutils'].split('.')):
		print("your binutils version is too old")
	os.system('apt install python-pip -y')
	os.system('pip3 install kconfiglib')
	os.system('apt-get install bison -y')
	os.system('apt-get install flex -y')
	os.system('apt install liblz4-tool -y')

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
	#logical partition

	if os.path.exists('acrn-kernel'):
		os.system('rm -rf acrn-kernel')
	os.system('git clone %s' % load_dict['sos_kernel_repo'])
	# build kernel
	cmd = 'cd acrn-kernel' + "&&" +'cp kernel_config_uefi_sos .config'
	os.system(cmd)

	cmd = 'cd acrn-kernel' + "&&" +'make olddefconfig'
	os.system(cmd)

	cmd = 'cd acrn-kernel' + "&&" +'make targz-pkg'
	os.system(cmd)

#create acrn deb
def create_acrn_deb():
	path = load_dict['acrn_deb_path']
	if os.path.exists(path):
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


	os.system('dpkg -b acrn_deb acrn_deb_package.deb ')


#install
def install_acrn_deb():
	os.system('dpkg -r acrn-package')
	os.system('dpkg -i acrn_deb_package.deb ')

	#change grub



def change_grub():
	#uuid
	# cmd = 'blkid |grep EFI'
	# devicelist = os.popen(cmd).read().split(' ')
	# uuid = [i for i in devicelist if "UUID=" in i and "PARTUUID" not in i]
	# uuid = str(uuid).split('"')[1]


	#partuuid
	cmd = 'blkid |grep -v EFI |grep UUID |grep nvme |grep -v PTUUID'
	devicelist = os.popen(cmd).read().replace('\n','').split(' ')
	alluuid = [i for i in devicelist if "UUID" in i]
	uuid = str(alluuid).split('"')[1]
	partuuid = alluuid[-1].split('"')[1]

	cmd = 'cd acrn_kernel_deb/boot' + '&&' + 'ls vmlinuz*'
	bzimgname = os.popen(cmd).read().replace('\n', '').replace('\r', '')

	grubfile=["#!/bin/sh \n","exec tail -n +3 $0 \n","menuentry 'ACRN ' --id ACRN ","{ ","\n", "	load_video \n","	insmod gzio\n","	insmod part_gpt\n","	insmod ext2\n","	search --no-floppy --fs-uuid  --set %s\n" % uuid,"echo $root \n","echo 'loading ACRN...'\n","multiboot2 /boot/acrn.bin root=PARTUUID=\"%s\"\n" % partuuid,"module2 /boot/%s Linux_bzImage\n" % bzimgname,"}\n"]

	path = load_dict['grub']

	with open('%s' % path,'w',encoding='utf-8') as fr:

	 	fr.writelines(grubfile)

	with open('/etc/default/grub','r',encoding='utf-8') as f:
	 	line = f.readlines()

	with open('/etc/default/grub',"w",encoding="utf-8") as fr:
			for lines in line:
				if 'GRUB_DEFAULT' in lines:
						fr.write('GRUB_DEFAULT=ACRN\n')
				elif 'GRUB_TIMEOUT' in lines:
						fr.write('GRUB_TIMEOUT=10\n')
				else:
	 				fr.write(lines)

	os.system('sync')
	os.system('update-grub')
#create acrn deb

def create_acrn_kernel_deb():

	path = load_dict['acrn_kernel_deb_path']
	if os.path.exists(path):
		os.system('rm -rf acrn_kernel_deb')

	os.system('mkdir -p acrn_kernel_deb')

	cmd = "cd acrn_kernel_deb" + "&&" +"mkdir DEBIAN"
	os.system(cmd)

	cmd = "cd acrn_kernel_deb" + "&&" +"touch DEBIAN/control"
	os.system(cmd)

	#control file description

	listcontrol=['Package: acrn-kernel-package\n','version: %s \n'% datetime.date.today(),'Section: free \n','Priority: optional \n','Architecture: amd64 \n','Installed-Size: 66666 \n','Maintainer: Intel\n','Description: sos_kernel \n','\n']


	with open('acrn_kernel_deb/DEBIAN/control','w',encoding='utf-8') as fr:
			fr.writelines(listcontrol)

	cmd = 'cd acrn-kernel' + '&&' + 'ls *.gz'
	filename = os.popen(cmd).read().replace('\n', '').replace('\r', '')
	cmd = 'cp acrn-kernel/%s acrn_kernel_deb/' % filename
	os.system(cmd)

	cmd = 'cd acrn_kernel_deb' + '&&' + 'tar -zvxf %s' % filename
	os.system(cmd)


	#cmd = 'cd acrn_kernel_deb/boot' + '&&' + 'mv %s bzImage' %bzimgname
	#os.system(cmd)

	os.system('rm acrn_kernel_deb/%s' % filename)

	os.system('dpkg -b acrn_kernel_deb acrn_kernel_deb_package.deb ')


#install
def install_acrn_kernel_deb():
	os.system('dpkg -r acrn-kernel-package ')
	os.system('dpkg -i acrn_kernel_deb_package.deb ')


	#change grub
def install_acrn_replace():
	pass

def install_acrn_makeinstall():
	if load_dict['in_native_ubuntu'] == 'true':
		cmd = 'cd acrn-hypervisor' + "&&" +'make install'
		os.system(cmd)
		cmd = 'cd acrn-kernel' + "&&" +'make modules_install'
		os.system(cmd)
	else:
		print('You are NOT in native ubuntu, can NOT make install!!!!')

def main_process():
	#install compile package,after this, compile env ok
	if load_dict['in_docker'] == 'true':
		with open("config.json","w") as load_out:
			load_dict['install_docker'] = 'false'
			load_out.write(json.dumps(load_dict))
		load_out.close()
	#docker install and enter dock, after this, enter docker enviroment
	if load_dict['install_docker'] == 'true':
		print('start install docker')
		install_docker()
		enable_docker()
		config_docker()
		docker_pull()
		exit()
	else:
		print('You decide NOT install docker')


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
	#install replace
	if load_dict['install_acrn_replace'] == 'true':
		print('start install through replace')
		install_acrn_replace()

	else:
		print('You decide NOT install ACRN through replace')

	#make install
	if load_dict['install_acrn_makeinstall'] == 'true':
		print('start install through make install')
		install_acrn_makeinstall()

	else:
		print('You decide NOT install ACRN through make install')

	if load_dict['grub_edit'] == 'true':
		print('start grub_edit')
		change_grub()

	else:
		print('You decide NOT grub_edit')

	if load_dict['auto_reboot'] == 'true':
		print('You decide to reboot!!!!!!!!!!!!!!!!!!!!!!!')
		os.system('reboot')

	else:
		print('You decide NOT reboot')
if __name__ == "__main__":
		main_process()