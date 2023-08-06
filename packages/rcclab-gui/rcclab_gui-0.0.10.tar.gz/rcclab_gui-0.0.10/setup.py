from setuptools import setup, find_packages
  
with open('README.md') as file:
    long_description = file.read()

short_description = 'Primer intento de subir algo a PyPI'
requirements = ['tk', 'pandas', 'numpy', 'openpyxl']
  

setup(  name ='rcclab_gui',
        version ='0.0.10',
        author='Bruno A. Franco',
        author_email='rosariocclab@gmail.com',
        url='https://github.com/RosarioCCLab/GUI',
        description =short_description	,
        long_description = long_description,
        long_description_content_type ="text/markdown",
        license ='MIT',
        #packages = find_packages(),
        #package_data={'': ['data/*.dat', 'examples/*', 'examples/menthol_ML_dJ-DP4/*', 'examples/menthol_ML_iJ-dJ-DP4/*']},
        entry_points = {'console_scripts': ['rcclab_gui = rcclab_gui.rcclab_gui:main']},
        classifiers = [
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent"],
        keywords ='Graphical User Interface',
        install_requires = requirements
        )


