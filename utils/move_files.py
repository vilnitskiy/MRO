import os, shutil
path = "regalpts_/unzip1/"
moveto = "regalpts_/upload/12/"
files = os.listdir(path)

for f in files:
    src = path+f
    dst = moveto+f
    shutil.move(src,dst)