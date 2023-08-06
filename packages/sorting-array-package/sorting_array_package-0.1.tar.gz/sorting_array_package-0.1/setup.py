from os import path
from setuptools import setup
from package.listfunc import __about__

try:
    current_path = path.abspath(path.dirname(__file__))
except NameError:
    current_path = None
try:
    with open(path.join(current_path, 'README.md'), encoding='utf-8') as f:
        long_description = f.read()
except FileNotFoundError:
    long_description = ''

setup(
    name=__about__.__title__,
    version=__about__.__version__,
    license='MIT License',
    author=__about__.__author__,
    author_email=__about__.__email__,
    description='selection sort',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.5',
    install_requires=['numpy'],
)
