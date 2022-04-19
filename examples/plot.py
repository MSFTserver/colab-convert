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

# test nesting and subprocesses
if True:
    !touch test_file.txt
    !git clone https://github.com/MSFTserver/pytorch3d-lite.git
    %pip list --outdated

#test directory magic
%ls
%cd ..
%ls
%rm -r pytorch3d-lite
%mkdir test_dir/test_subdir
%cat test_file.txt
%mv test_file.txt test_dir
%ls test_dir
%cp test_dir/test_file.txt test_dir/test_subdir/test_file.txt
%ls
%rm test_file.txt
%ls
%mv test_dir/test_file.txt test_dir/test_subdir/test_file.txt

# test environment magic
%env
%env PATH
%env TEST_COLAB_CONVERT=HELLO
%set_env TEST_COLAB_CONVERT=HELLO
%env TEST_COLAB_CONVERT
%env TEST_COLAB_CONVERT GOODBYE
%set_env TEST_COLAB_CONVERT GOODBYE
%env TEST_COLAB_CONVERT

%notValid

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
