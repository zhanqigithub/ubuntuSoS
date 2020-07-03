# ubuntuSoS
this scripts show how to build acrn-hypervisor and acrn-kernel deb package

1. setup native ubuntu

install python3

config proxy

sudo su


2. config json file


{

	"//":"release ubuntu as sos verion",

	"install_package":"true",---------->this 1st time should set to true if you did not install acrn related compile package, if already install,set to false

	"gcc_version":"7.3.0",---------->higher than this

	"binutils":"2.27",---------->higher than this

	"//":"acrn-hypervisor config",

	"build_acrn":"true",---------->if you need build acrn-hypervisor

	"sync_acrn_code":"true",---------->if you need sync acrn-hypervisor code 

	"acrn_repo":"https://github.com/projectacrn/acrn-hypervisor.git",---------->acrn repo

	"release_version":"remotes/origin/release_2.0",---------->acrn release branch

	"acrn_deb_package":"true",---------->if you need create acrn-hypervison deb

	"install_acrn_deb":"false",---------->if you need install acrn-hypervisor deb

	"build_cmd":---------->acrn-hypervisor build command should include scenario and board info and release type

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

	"//":"kernel config",

	"build_acrn_kernel":"true",---------->if you need build acrn-kernel

	"sync_acrn_kernel_code":"true",---------->if you need sync acrn-kernel code 

	"kernel_release_version":"remotes/origin/release_2.0",---------->acrn kernel release branch


	"sos_kernel_repo":"https://github.com/projectacrn/acrn-kernel.git",---------->acrn kernel repo


	"acrn_kernel_deb_package":"true",---------->if you need create acrn-kernel deb

	"install_acrn_kernel_deb":"false",---------->if you need install acrn-kernel deb

	"//":"misc",

	"auto_reboot":"false"---------->if you need ireboot

}

3.pythons install_uSoS.py

after finished , will get below two item

acrn_deb_package.deb

acrn_kernel_deb_package.deb


install command

dpkg -i acrn_deb_package.deb

dpkg -i acrn_kernel_deb_package.deb


uninstall

dpkg -r acrn-package

dpkg -r acrn-kernel-package

