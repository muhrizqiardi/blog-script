import subprocess
import sys
import os
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ENDC = '\033[0m'

def open_external(path):  
  try:
    subprocess.Popen(["powershell.exe",
    "start",
    f'"{path}"'],
    stdout=sys.stdout).communicate()

  except Exception as e:
    print(f'{bcolors.FAIL}⚠ An error happened: {e}{bcolors.ENDC}')
