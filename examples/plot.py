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
        !git clone https://github.com/MSFTserver/pytorch3d-lite.git
        %cd pytorch3d-lite

%cd ..
shutil.rmtree(f'{os.getcwd()}/pytorch3d-lite')

%env

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
