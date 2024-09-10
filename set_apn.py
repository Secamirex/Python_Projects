"""
Description:
Script to set the APN name and its parameters for Data Profile 1
Platform: Embedded Linux
Author: Amir Nejad 
"""
import paramiko
import time
import warnings
import logging
import re
import os

logging.basicConfig(filename=r'C:\Users\amirn\Dropbox\Amir\AmirPython\Logs\APN.log',
                    filemode='w', format='%(asctime)s:%(levelname)s:%(message)s', level=logging.INFO)

# To remove the paramiko Cryptography Deprecation Warning
warnings.filterwarnings(action='ignore', module='.*paramiko.*')

HOST = '192.168.1.1'
PORT = 22
USER_NAME = 'root'
PASS = 'Admin@123'

try:
    # SSH into router
    def sshconnect():
        print('APN test & set in progress, details will also be logged once completed!')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.WarningPolicy)
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(HOST, PORT, USER_NAME, PASS)
        logging.info('Connected to the router....')
        time.sleep(2)

        # Checking auto apn
        def apncheck():

            stdin, stdout, stderr = (ssh.exec_command('rdb_get -L | grep link.profile.1.autoapn'))
            apn_status = [data for data in stdout]
            finder = re.findall(r'\s\d{1}', str(apn_status))

            if finder == "[' 1']" or ' 1':
                # Turning auto apn off
                logging.info('Auto APN is on, turning it off')
                logging.info('Setting APN name & parameters ...')
                ssh.exec_command('rdb_set link.profile.1.autoapn 0')
                time.sleep(2)

                # Setting APN name and username, password and Authentication type
                ssh.exec_command('rdb_set link.profile.1.apn apn.wap')
                ssh.exec_command('rdb_set link.profile.1.user test ')
                ssh.exec_command('rdb_set link.profile.1.pass m2m')
                ssh.exec_command('rdb_set link.profile.1.auth_type  chap')
                time.sleep(2)
                stdin1, stout1, stderr1 = (ssh.exec_command('rdb_get -L | grep link.profile.1.apn.current'))
                for data in stout1.readlines():
                    logging.info('APN is now set to: {}'.format(data[27:]))
                logging.info('Checking IP address range...')
                stdin2, stout2, stderr2 = (ssh.exec_command('rdb_get -L | grep link.profile.1.iplocal'))
                wwan_ip = [data for data in stout2]
                ipfinder = re.findall(r'\d{3}.\d{3}.\d{3}.\d{3}',str(wwan_ip))
                logging.info('WWAN IP: {}'.format((ipfinder)))

        apncheck()

        # Showing APN log on CMD console as stdout
        def logread():
            print('Test is completed, reading APN log now...')
            os.chdir(r'C:\Users\amirn\Dropbox\Amir\AmirPython\IoT\Logs\APN.log')
            with open('APN.log', 'r') as apnlog:
                for lines in apnlog:
                    print(lines, end='')

        logread()


    if __name__ == '__main__':
        sshconnect()

except (TypeError,IndexError,FileNotFoundError,NotADirectoryError, paramiko.SSHException) as err:
    print('Error Occurred: {}'.format(err))
