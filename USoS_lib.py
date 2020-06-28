# -*- coding: utf-8 -*-
import os,sys,copy,json
import subprocess
import datetime
import time

#create acrn deb

def create_acrn_kernel_deb():

	if os.path.exists('acrn_kernel_deb'):
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


	cmd = 'cd acrn_kernel_deb/boot' + '&&' + 'ls vmlinuz*'
	version = os.popen(cmd)

	f = open("acrn_kernel_deb/boot/version.txt",'w')
	f.write(version.read())
	f.close()

	os.system('cp acrn-kernel.postinst acrn_kernel_deb/DEBIAN/postinst' )

	os.system('chmod +x acrn_kernel_deb/DEBIAN/postinst')

	os.system('sed -i \'s/\r//\' acrn_kernel_deb/DEBIAN/postinst')

	os.system('rm acrn_kernel_deb/%s' % filename)

	os.system('dpkg -b acrn_kernel_deb acrn_kernel_deb_package.deb ')

def build_acrn_kernel(acrn_repo,acrn_version):
	if os.path.exists('acrn-kernel'):
		os.system('rm -rf acrn-kernel')

	os.system('git clone %s' % acrn_repo)

	cmd = 'cd acrn-kernel' + "&&" +'git checkout -b mybranch %s'% acrn_version
	os.system(cmd)
	# build kernel
	cmd = 'cd acrn-kernel' + "&&" +'cp kernel_config_uefi_sos .config'
	os.system(cmd)

	cmd = 'cd acrn-kernel' + "&&" +'make olddefconfig'
	os.system(cmd)

	cmd = 'cd acrn-kernel' + "&&" +'make targz-pkg'
	os.system(cmd)

# install compile package
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
     libelf-dev\
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

#install acrn
def install_acrn_deb():
	os.system('dpkg -r acrn-package')
	os.system('dpkg -i acrn_deb_package.deb ')


#install kernel
def install_acrn_kernel_deb():
	os.system('dpkg -r acrn-kernel-package ')
	os.system('dpkg -i acrn_kernel_deb_package.deb ')