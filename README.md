# colab-convert

Converts ipython/Google Colab Notebooks into runable Python code and vice versa 

Atom/Hydrogen or VSCode/Python allows creating a python files split into cells with `# %%` separators with the ability to run cells via backend Jupyter session and interactively show results back.

[colab-convert](https://pypi.python.org/pypi/colab-convert) python module converts files: .ipynb to .py and .py to .ipynb.

**colab-convert** is a fork of the [ipynb-py-convert](https://github.com/kiwi0fruit/ipynb-py-convert).

## Features

- converts ipython/colab magic % and ! to regular python code
- comments out unsupported ipython magic
- creates new import blocks for converted code
- logs all changes to a log file for review
- converted magic commands are prefixed with `#<cc-cm>`
- commented magic commands are appended with `#<cc-ac>`


## Install & Basic Usage

```console
pip install colab-convert
```

```console
Usage: colab-convert <input_file> <output_file> <flags>

<input_file>: input file to convert
<output_file>: output file to write to
<flags>: extra flags to pass to the converter

all flags are optional and have set defaults for best results
use flags to enable or disable certain functions on/off by default
```

```console
colab-convert in.ipynb out.py -nc -rm -o
```

## Default options and Flags
```console
Default Flags Set (defaults are determined by input file)
  ipynb input file:
    [YES] convert magic , [YES] auto comment , [YES] imports , [NO] Outputs
  py input file:
    [NO] convert magic , [NO] auto comment , [NO] imports , [NO] Outputs

Available Flags
  toggle certain items on or off

  --retain-magic  (-rm)  : Keep magic commands in the output
      .py default    [ON]
      .ipynb default [OFF]
  --convert-magic  (-cm) : Convert magic commands to python code
      .py default    [OFF]
      .ipynb default [ON]
  --auto-comment  (-ac)  : Convert unsupported magic commands to comments
      .py default    [OFF]
      .ipynb default [ON]
  --no-comment  (-nc)    : Keep unsupported magic commands
      .py default    [ON]
      .ipynb default [OFF]
  --no-imports  (-ni)    : Do not add imports from converted magic commands
      .py default    [OFF]
      .ipynb default [OFF]
  --outputs  (-o)        : Outputs to console of conversions and commented lines.
      .py default    [OFF]
      .ipynb default [OFF]
```

## Troubleshooting

* If encoding problems on Windows try using `python>=3.7`, setting `set PYTHONUTF8=1` in Windows console and use `colab-convert` for UTF-8 files only. If using [Git-Bash on Windows](https://git-scm.com/download/win) setting:

```console
export LANG=C.UTF-8
export PYTHONIOENCODING=utf-8
export PYTHONUTF8=1
```
should be enough. Also try setting default Bash settings to UTF-8: [Options] - [Text] - [Locale / Character set] - [C / UTF-8]. It might affect all Bash runs so there would be no need to setting encoding every time. 

## Example

`colab-convert examples/plot.py examples/plot.ipynb`

or

`colab-convert examples/plot.ipynb examples/plot.py`


**VSCode**

![](https://github.com/MSFTserver/colab-convert/raw/master/examples/vscode.png)

Markdown cells are converted to python multiline strings `'''`. Code cells are left as is.

eg. will render header section

```python
"""
## Matplot example

** Run the cell below to import some packages and show a line plot **
"""
```

`# %%` is used by vscode as the cell marker on which 'Run Cell' action is available.


eg. will render a code cell

```python
# %%
import matplotlib.pyplot as plt
```

Metadata is converted from notebooks into .py and vise versa using `# !!` to denote the meta data lines in the .py files

eg.
```python
# %%
# !! {"metadata":{
# !!   "id": "PlotIt"
# !! }}
import matplotlib.pyplot as plt
```

eg. final code block must include atleast this
```python
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
```


**Jupyter ipynb notebook**

![](https://github.com/MSFTserver/colab-convert/raw/master/examples/jupyter.png)
