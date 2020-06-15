# ubuntuSoS
for ACRN quick start from ubuntu
1. ubuntu native 18.04

install python3

config proxy

sudo su

2. config json file according to your needs

	"//" :"basic information",
        
	"username":"root",
        
	"password":"intel@123",
        
	"ubuntu_version":"18.04",
        
	"scripts_path":"/home/acrn/sherry",------------------scripts path
        
	"//":" docker",
        
	"install_docker":"false",---------------------------------------------do you need install docker?
        
	"docker_proxy":"HTTPS_PROXY=http://child-prc.intel.com:913",------------proxy
        
	"docker_image":"ubuntu:18.04",
        
	"docker_name":"acrn_ubuntu",
        
	"docker_rebuild":"true",
        
	"export_docker":"true",
        
	"//":" install compile pakage",
        
	"in_docker":"false",
        
	"in_native_ubuntu":"true",-----------------------are you in native ubuntu?
        
	"install_package":"false",------------------------do you need install compile related package
        
	"gcc_version":"7.3.0",
        
	"binutils":"2.27",
        
	"acrn_repo":"https://github.com/projectacrn/acrn-hypervisor.git",
        
	"release_version":"remotes/origin/release_2.0",-----------------------------whcih branch do you need?
        
	"sos_kernel_repo":"https://github.com/projectacrn/acrn-kernel.git",
        
	"build_acrn":"true",
        
	"build_source_cmd":"make all BOARD_FILE=misc/acrn-config/xmls/board-xmls/whl-ipc-i5.xml SCENARIO_FILE=misc/acrn-config/xmls/config-xmls/whl-ipc-i5/industry.xml RELEASE=0",---------------------hypervisor build cmd
        
	"build_tool_cmd":"flase",
        
	"build_kernel":"true",
        
	"build_RT_kernel":"false",
        
	"acrn_deb_package":"true",------------------do you need create deb ?
        
	"acrn_deb_path":"acrn_deb",
        
	"install_acrn_deb":"true",-----------------------do you need install from deb?
        
	"acrn_kernel_deb_package":"true",---------------------do you need create kernel deb?
        
	"acrn_kernel_deb_path":"acrn_kernel_deb",
        
	"install_acrn_kernel_deb":"true",---------------do you need install kernel deb?
        
	"grub":"/etc/grub.d/40_custom",
        
	"grub_edit":"true",-------------------------do you need change grub?
        
	"install_acrn_replace":"false",
        
	"install_acrn_makeinstall":"false",
        
	"auto_reboot":"true"----------------------------do you need reboot?
        
