import os
path = '/home/andrey_g/mro/schneider/pdf'
files = os.listdir(path)

for file in files:
    os.rename(os.path.join(path, file), os.path.join(path, 'schneiderpdf_' + os.path.splitext(os.path.basename(file))[0] +'.pdf'))
