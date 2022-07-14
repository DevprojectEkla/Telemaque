#! python3.10
import os
import sys
import socket
import getopt
import threading
import subprocess
import shlex

# pour importer les modules personnels
def import_fmodule(filename: str):
    path = os.getcwd()
    module = open(os.path.join(os.path.normpath(path),filename),"r")
    sortie = module.read()
    return (sortie)
    
  


    

