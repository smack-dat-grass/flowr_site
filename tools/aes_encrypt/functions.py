import os
import traceback

from subprocess import Popen, PIPE, STDOUT
from django.conf import settings

MODE_ENCRYPT='encrypt'
MODE_DECRYPT='decrypt'
def aes_encrypt(key, value):
    try:
         value = run_encryption_jar(key, value, MODE_ENCRYPT)
         if "java." in value or "javax." in value:
             raise Exception(value)
         return value
    except Exception as e:
        traceback.print_exc()
        raise e
def aes_decrypt(key, value):
    try:
        value = run_encryption_jar(key, value, MODE_DECRYPT)
        if "java." in value or "javax." in value:
            raise Exception(value)
        return value
    except Exception as e:
        traceback.print_exc()
        raise e

def run_encryption_jar(key, value, mode):
    p = Popen(['java', '-jar', 'aes-encrypt.jar', key, mode, value], stdout=PIPE, stderr=STDOUT, cwd=settings.BASE_DIR)
    for line in p.stdout:
        return line.decode('utf-8').replace("\n", "").replace("\r","")

