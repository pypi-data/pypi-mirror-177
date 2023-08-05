from setuptools import setup
from pathlib import Path

this_dir = Path(__file__).parent

long_description = (this_dir / 'README.md').read_text(encoding='utf8')

setup(
    version='0.0.6',
    name='vialactea',
    packages=['vialactea'],
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Sirius Technology Studio',
    maintainer='Sirius Technology Studio',
    maintainer_email=''
)

