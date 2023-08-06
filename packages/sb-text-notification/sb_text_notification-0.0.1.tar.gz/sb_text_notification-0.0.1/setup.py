from setuptools import setup, find_packages

VERSION = '0.0.1' 
DESCRIPTION = 'A text notification package'
LONG_DESCRIPTION = 'A module for sending a text notification.'

# Setting up
setup(
       # the name must match the folder name 'verysimplemodule'
        name="sb_text_notification", 
        version=VERSION,
        author="Scott B. Williams",
        author_email="<sbwilliaowu@yahoo.com>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'first package'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)