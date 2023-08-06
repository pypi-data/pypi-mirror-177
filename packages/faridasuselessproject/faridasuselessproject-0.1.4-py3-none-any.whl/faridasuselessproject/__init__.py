import sys
import os
import subprocess

try:
    import numpy as np
except ImportError:
    FNULL = open(os.devnull, 'w')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-Iv','numpy==1.22.0'], stdout=FNULL, 
    stderr=subprocess.STDOUT)
    

def vector(x):
    return np.ones(x)
