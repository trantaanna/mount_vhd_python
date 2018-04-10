import logging
import os
import subprocess



def mount_vhd(path=r'C:\testusb'):
	##--------------------
	#  Create batch file for attaching USB

	if not os.path.exists(path):
		os.makedirs(path)


	usb_drive = os.path.join(path, "usb.vhd")
	create_vhd_batch = os.path.join(path, "MountVHD.bat")
	mount_usb = os.path.join(path, "createusb.txt")

	logging.info("Creating MountVHD.bat ...")
	textList = [
		r'(echo create vdisk file="{}" maximum=100'.format(usb_drive),
		r'echo select vdisk file="{}"'.format(usb_drive),
		r'echo attach vdisk',
		r'echo convert mbr',
		r'echo create partition primary',
		r'echo format fs=ntfs label=install quick',
		r'echo assign letter=R',
		r'echo list vdisk',
		r')> {}'.format(mount_usb),
		r'diskpart /s {}'.format(mount_usb)]
	textList = map(lambda x: x + "\n", textList)

	with open(create_vhd_batch, 'w') as f:
		f.writelines(textList)
	f.close()

	logging.info("Mounting USB device to R: drive ...")
	#--------------------
	#  run bat script to mount device
	try:
		logging.info('Launching {}...'.format(create_vhd_batch))
		subprocess.check_output(create_vhd_batch, shell=True)
	except subprocess.CalledProcessError as error:
		logging.info("Error creating and attaching USB drive: {}".format(error))

	##--------------------
	#  create a file on R drive
	with open(r'R:\hello.txt', 'w') as f:
		f.write("Hellow World!!!")
	f.close()

if __name__ == '__main__':
	logging.info('Calling mount_vhd')
	mount_vhd(r'C:\testusb')

