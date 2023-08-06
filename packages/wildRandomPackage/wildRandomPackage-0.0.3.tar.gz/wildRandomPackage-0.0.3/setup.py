from setuptools import setup, find_packages

VERSION = '0.0.3' 
DESCRIPTION = 'My first Python package'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description'

# Setting up
setup(
        name="wildRandomPackage", 
        version=VERSION,
        author="Alex Walters",
        author_email="<awalter2@g.emporia.edu>",
        description=DESCRIPTION,
        long_description=LONG_DESCRIPTION,
        packages=find_packages(),
        install_requires=[], # add any additional packages that 
        # needs to be installed along with your package. Eg: 'caer'
        
        keywords=['python', 'simpleCalpackage'],
        classifiers= [
            "Development Status :: 3 - Alpha",
            "Intended Audience :: Education",
            "Programming Language :: Python :: 2",
            "Programming Language :: Python :: 3",
            "Operating System :: MacOS :: MacOS X",
            "Operating System :: Microsoft :: Windows",
        ]
)