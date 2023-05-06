import os
import glob
os.chdir(r'Documents/image/')
for index, oldfile in enumerate(glob.glob("*.txt"), start=1):
    os.remove(oldfile)