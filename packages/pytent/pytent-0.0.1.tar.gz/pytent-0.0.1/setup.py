from setuptools import setup

with open("README.md", "r") as fh:
    readme = fh.read()

setup(name='pytent',
    version='0.0.1',
    url='https://github.com/raulivan/pytent',
    license='MIT License',
    author='Raulivan Rodrigo da Silva',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='raulivanrodrigo@gmail.com',
    keywords='pytent, patent, inpi, espacenet, data science',
    description=u'Package for collecting, processing and visualizing patent data for data science',
    packages=['pytent'],
    install_requires=['requests','tqdm'],)