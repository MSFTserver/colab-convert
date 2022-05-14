from setuptools import setup
from os import path
import io

here = path.abspath(path.dirname(__file__))
with io.open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='colab-convert',
    packages=['colab_convert'],
    version='2.0.0',
    description='Convert .py files runnable in VSCode/Python or Atom/Hydrogen to jupyter/colab .ipynb notebooks and vice versa',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='HostsServer',
    author_email='msftserver@gmail.com',
    license='MIT',
    url='https://github.com/MSFTserver/colab-convert',
    keywords=['vscode', 'jupyter', 'convert', 'ipynb', 'py', 'atom', 'hydrogen', 'colab', 'google', 'google colab', 'notebook'],
    classifiers=[],
    entry_points={
        'console_scripts': [
            'colab-convert=colab_convert.__main__:main',
        ],
    },
)
