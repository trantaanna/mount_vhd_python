import logging
import os
import subprocess



def unmount_vhd(path=r'C:\testusb'):
	##--------------------
	#  Create batch file for attaching USB

	if not os.path.exists(path):
		os.makedirs(path)

	#assume usb.vhd already exist
	usb_drive = os.path.join(path, "usb.vhd")
	delete_vhd_batch = os.path.join(path, "UnMountVHD.bat")
	unmount_usb = os.path.join(path, "deleteusb.txt")

	logging.info("Creating UnMountVHD.bat ...")
	textList = [
		r'(echo select vdisk file="{}"'.format(usb_drive),
		r'echo detach vdisk',
		r')> {}'.format(unmount_usb),
		r'diskpart /s {}'.format(unmount_usb)]
	textList = map(lambda x: x + "\n", textList)
	with open(delete_vhd_batch, 'w') as f:
		f.writelines(textList)
	f.close()

	logging.info("UnMounting USB device from R: drive ...")
	#--------------------
	#  run bat script to mount device
	try:
		logging.info('Launching {}...'.format(delete_vhd_batch))
		subprocess.check_output(delete_vhd_batch, shell=True)
	except subprocess.CalledProcessError as error:
		logging.info("Error detach USB drive: {}".format(error))


if __name__ == '__main__':
	logging.info('Calling mount_vhd')
	unmount_vhd(r'C:\testusb')

