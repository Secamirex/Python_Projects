"""
Description:
Script to generate the MD5 hash value of a file
Platform: Embedded Linux
Author: Amir Nejad

"""


import hashlib
import sys
import logging
import os



def md5_checksum():
    try:
        while True:

            value = input('Enter the file name:')
            print('*' * 70)
            if value:
                print('Original value : {}'.format(value))
                encoded_value = hashlib.md5(value.encode('utf-8'))
                print("MD5 checksum value: {}".format(encoded_value.hexdigest().upper()))
                print('*' * 70)
                break

            if not value:
                print("Error! no data is submitted, try again! \n")
                continue


    except TypeError as err:
        print('Error occurred: {}'.format(err))
        sys.exit(1)


md5_checksum()



