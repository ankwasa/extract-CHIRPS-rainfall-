#!/usr/bin/env python
'''this script unzips the downloaded CHIRPS precipitation data.

Author  : albert nkwasa
Contact : nkwasa.albert@gmail.com / albert.nkwasa@vub.be 
Date    : 2021.07.30

'''
import gzip
import shutil
import os


working_dir = os.path.dirname(os.path.realpath(__file__))
os.chdir(working_dir)
try:
    os.makedirs(f"{working_dir}/extracted_tifs")
except:
    pass

# os.chdir(f'{working_dir}/extracted_tifs')
for file in os.listdir():
    if file.endswith('.gz'):
        with gzip.open(file, 'rb') as f_in:
            old_name = file.split('.')
            new_name = old_name[0]+'_' + old_name[1]+'_' + old_name[2] + \
                '_' + old_name[3]+'_' + old_name[4]+'.' + old_name[5]
            out_path = f'{working_dir}/extracted_tifs/{new_name}'
            with open(out_path, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

os.chdir(working_dir)
for k in os.listdir():
    if k.endswith('.gz'):
        os.remove(k)

print('\t >finished')
