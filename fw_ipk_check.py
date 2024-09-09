"""
Description:
Script to check router , Module firmware and
installed IPK packages on LTE IoT router 
Platform: Embedded Linux
"""

import paramiko
import warnings
import logging
import sys

logging.basicConfig(filename=r'C:\Users\amirn\Dropbox\Amir\PYTHON\AmirPython\IoT\Logs\FW_IPK.log',
                    filemode='w', format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

# Setting login global variables

HOST = '192.168.1.1'
PORT = 22
USER_NAME = 'root'
PASS = "4dm1n@1234"

# To remove the paramiko Cryptography Deprecation Warning if pops up
warnings.filterwarnings(action='ignore', module='.*paramiko.*')

try:
    def sshconnect():
        print('FW test in progress, details will be logged!')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, PORT, USER_NAME, PASS)
        
        # Checking installed IPK packages
        def ipk_check():
            stdin, stdout, stderr = ssh.exec_command('ipkg-cl list_installed')
            logging.info('*' * 46)
            logging.info('Checking installed packages...... \n')
            time.sleep(2)
            for package in stdout:
                if package:
                    logging.info('installed package: {}'.format(package))
            logging.info('*' * 16 + 'DEVICE DETAILS' + '*' * 16 + '\n')

        ipk_check()

        #  Checking router's info ( Model, Router FW, Module FW, IMEI, SerialNumber)
        def firmware_check():
            stdin1, stdout1, stderr1 = (ssh.exec_command('rdb_get -L | grep sw.version | cut -d " " -f 2'))
            stdin2, stdout2, stderr2 = (ssh.exec_command('rdb_get -L | grep wwan.0.firmware_version | cut -d " " -f 2'))
            stdin3, stdout3, stderr3 = (ssh.exec_command('rdb_get -L | grep system.product.model  | cut -d " " -f 2'))
            stdin4, stdout4, stderr4 = (ssh.exec_command('rdb_get -L | grep wwan.0.imei | cut -d " " -f 2'))
            stdin5, stdout5, stderr5 = (ssh.exec_command('rdb_get -L | grep uboot.sn | cut -d " " -f 2'))
            model = [data for data in stdout3.readlines()]
            logging.info('Router Model: {}'.format(model[0]))


            r_fw = [data for data in stdout1.readlines()]
            logging.info('Router Firmware: {}'.format((r_fw[0])))

            m_fw = [data for data in stdout2.readlines()]
            logging.info('Module Firmware: {}'.format(m_fw[0]))

            imei = [data for data in stdout4.readlines()]
            logging.info('Module IMEI: {}'.format(imei[0]))

            sn = [data for data in stdout5.readlines()]
            logging.info(('Serial Number: {}'.format(sn[0])))

            logging.info('*' * 47)

        firmware_check()


    if __name__ == '__main__':
        sshconnect()

except paramiko.SSHException as err:
    logging.info(' Error occurred: {}'.format(err))
    sys.exit(1)
