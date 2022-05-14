# %%
# !! {"metadata":{
# !!   "id":"cc-imports"
# !! }}

#<cc-imports>

import subprocess
import os
import shutil

# %%
# !! {"metadata":{
# !!   "id": "TitleTop"
# !! }}
"""
## Matplot example

** Run the cell below to import some packages and show a line plot **
"""

# %%
# !! {"metadata":{
# !!   "id": "PlotIt"
# !! }}
import matplotlib.pyplot as plt
import numpy as np
import shutil

# test nesting and subprocesses
if True:
    sub_p_res = subprocess.run(['touch', 'test_file.txt'], stdout=subprocess.PIPE).stdout.decode('utf-8') #<cc-cm>
    print(sub_p_res) #<cc-cm>
    sub_p_res = subprocess.run(['git', 'clone', 'https://github.com/MSFTserver/pytorch3d-lite.git'], stdout=subprocess.PIPE).stdout.decode('utf-8') #<cc-cm>
    print(sub_p_res) #<cc-cm>
    pip_sub_p_res = subprocess.run(['pip', 'list', '--outdated'], stdout=subprocess.PIPE).stdout.decode('utf-8') #<cc-cm>
    print(pip_sub_p_res) #<cc-cm>

#test directory magic
os.listdir() #<cc-cm>
os.chdir('..') #<cc-cm>
os.listdir() #<cc-cm>
shutil.rmtree('pytorch3d-lite') #<cc-cm>
os.makedirs('test_dir/test_subdir') #<cc-cm>
cat_read_file = open('test_file.txt', 'r') #<cc-cm>
cat_read_text = cat_read_file.read() #<cc-cm>
print(cat_read_text) #<cc-cm>
cat_read_file.close() #<cc-cm>
shutil.move('test_file.txt', 'test_dir/test_file.txt') #<cc-cm>
os.listdir('test_dir') #<cc-cm>
shutil.copy('test_dir/test_file.txt', 'test_dir/test_subdir/test_file.txt') #<cc-cm>
os.listdir() #<cc-cm>
os.remove('test_file.txt') #<cc-cm>
os.listdir() #<cc-cm>
shutil.move('test_dir/test_file.txt', 'test_dir/test_subdir/test_file.txt') #<cc-cm>

# test environment magic
for k, v in os.environ.items(): #<cc-cm>
    print(f'{k}={v}') #<cc-cm>
os.environ['PATH'] #<cc-cm>
os.environ['TEST_COLAB_CONVERT'] = 'HELLO' #<cc-cm>
os.environ['TEST_COLAB_CONVERT'] = 'HELLO' #<cc-cm>
os.environ['TEST_COLAB_CONVERT'] #<cc-cm>
os.environ['TEST_COLAB_CONVERT'] = 'GOODBYE' #<cc-cm>
os.environ['TEST_COLAB_CONVERT'] = 'GOODBYE' #<cc-cm>
os.environ['TEST_COLAB_CONVERT'] #<cc-cm>

#<cc-ac> %notValid

x = np.linspace(0, 20, 100)
plt.plot(x, np.sin(x))
plt.show()

# %%
# !! {"main_metadata":{
# !!   "anaconda-cloud": {},
# !!   "kernelspec": {
# !!     "display_name": "Python 3",
# !!     "language": "python",
# !!     "name": "python3"
# !!   },
# !!   "language_info": {
# !!     "codemirror_mode": {
# !!       "name": "ipython",
# !!       "version": 3
# !!     },
# !!     "file_extension": ".py",
# !!     "mimetype": "text/x-python",
# !!     "name": "python",
# !!     "nbconvert_exporter": "python",
# !!     "pygments_lexer": "ipython3",
# !!     "version": "3.6.1"
# !!   }
# !! }}
