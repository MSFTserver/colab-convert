# %%
# !! {"metadata":{
# !!   "id":"colab-convert"
# !! }}

#<cc-imports>
import subprocess
import os

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

if True:
    sub_p_res = subprocess.run(['git', 'clone', 'https://github.com/MSFTserver/pytorch3d-lite.git'], stdout=subprocess.PIPE).stdout.decode('utf-8') #<cc-cm>
    print(sub_p_res) #<cc-cm>
    os.chdir('pytorch3d-lite') #<cc-cm>

os.chdir('..') #<cc-cm>
shutil.rmtree('pytorch3d-lite')

for k, v in os.environ.items(): #<cc-cm>
    print(f'{k}={v}') #<cc-cm>

os.environ['PATH'] #<cc-cm>

os.environ['TEST_COLAB_CONVERT'] = 'HELLO' #<cc-cm>

os.environ['TEST_COLAB_CONVERT'] = 'HELLO' #<cc-cm>

os.environ['TEST_COLAB_CONVERT'] #<cc-cm>

os.environ['TEST_COLAB_CONVERT'] = 'GOODBYE' #<cc-cm>

os.environ['TEST_COLAB_CONVERT'] = 'GOODBYE' #<cc-cm>

os.environ['TEST_COLAB_CONVERT'] #<cc-cm>

#<cc-ac> %testing

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
