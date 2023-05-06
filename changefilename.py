import os
import glob
text = 'image'
os.chdir(r'Documents/' + text)
for index, oldfile in enumerate(glob.glob("*.jpg"), start=1):
    newfile = text.lower() + '{}.jpg'.format(index)
    os.rename(oldfile,newfile)
