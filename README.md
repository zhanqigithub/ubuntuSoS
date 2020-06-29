Part I
for ACRN quick start from ubuntu,only build EB, You can select all as default to finish compile env install.acrn hypervisor/kernel compile, generate deb package and install
please refer below process
1. ubuntu native 18.04

install python3

config proxy

sudo su

2. config json file according to your needs, please change config.json,default as below

{
	
	"install_package":"true",----------------->if your native ubuntu not install related package for conpile please set as true,if already install, set to false
	
	"gcc_version":"7.3.0",------------>gcc version should higher than this,no need change
	
	"binutils":"2.27",----------->binutils version should higher than this,no need change
	
	"acrn_repo":"https://github.com/projectacrn/acrn-hypervisor.git",---------------->acrn repo, no need change
	
	"release_version":"remotes/origin/release_2.0",-----------------> release version,should change according to release version and branch
	
	"sos_kernel_repo":"https://github.com/projectacrn/acrn-kernel.git",----------->kernel repo, no need change
	
	"build_acrn":"true",--------------> build acrn hypervisor,default true, will remove acrn_hypervisor folder, if do not want to build set to false
	
	"build_source_cmd":"make all BOARD_FILE=misc/acrn-config/xmls/board-xmls/whl-ipc-i5.xml SCENARIO_FILE=misc/acrn-config/xmls/config-xmls/whl-ipc-i5/industry.xml RELEASE=0",------->build command,please input complete build command for acrn
	
	"build_acrn_kernel":"true",--------------> build acrn kernel,default true, will remove acrn_kernel folder, if do not want to build set to false
	
	"acrn_deb_package":"true",----------->create acrn deb package,if do not want to create set to false
	
	"install_acrn_deb":"true",----------->install acrn deb package,if do not want to install set to false
	
	"acrn_kernel_deb_package":"true",----------->create acrn kernel deb package,if do not want to create set to false
	
	"install_acrn_kernel_deb":"true",----------->install acrn kernel deb package,if do not want to install set to false
	
	"auto_reboot":"false"---------------->if need reboot, set to true,default false
	
}

3. python3 main_start.py
after all finished,below two item could find

acrn_deb_package.deb

acrn_kernel_deb_package.deb


uninstall

dpkg -r acrn-package

dpkg -r acrn-kernel-package


install

dpkg -i acrn_kernel_deb_package.deb

dpkg -i acrn_deb_package.deb


Part II
for who need compile all software scenario/platform provided by acrn, You can select all as default to finish compile env install.acrn hypervisor/kernel compile, generate deb package which include all supported and install package according to your board
please refer below process
1. ubuntu native 18.04

install python3

config proxy

sudo su

2. release json file according to your needs, please change release.json,default as below

{

	"//" :"release ubuntu as sos verion",
	
	"build_acrn":"true",------->if your native ubuntu not install related package for conpile please set as true,if already install, set to false
	
	"create_acrn_deb":"true",----------->create deb package,if do not want to create set to false
	
	"acrn_repo":"https://github.com/projectacrn/acrn-hypervisor.git",---------------->acrn repo, no need change
	
	"release_version":"remotes/origin/release_2.0",-----------------> release version,should change according to release version and branch
	
	"sos_kernel_repo":"https://github.com/projectacrn/acrn-kernel.git",----------->kernel repo, no need change
	
	"build_cmd":--------->build command,please input scenario/board for acrn
	
	{
	
		"scenario":
		
		{
		
			"industry":"true",
			
			"hybrid":"true",
			
			"logical_partition":"true"
			

		},
		
		"board":
		
		{
		
			"nuc7i7dnb":"true",
			
			"whl-ipc-i5":"true"
			
		},
		
		"release":"0"
		
	},
	
	"install_acrn_deb":"true"----------->install acrn deb package,if do not want to install set to false
	
}

3. python3 install_uSoS.py
after all finished,below two item could find

acrn_deb_package.deb

acrn_kernel_deb_package.deb


uninstall

dpkg -r acrn-package

dpkg -r acrn-kernel-package


install

dpkg -i acrn_kernel_deb_package.deb

dpkg -i acrn_deb_package.deb
