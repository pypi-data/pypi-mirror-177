from setuptools import setup, find_packages

VERSION = '0.0.2' 
DESCRIPTION = 'My first Python package but the second version'
LONG_DESCRIPTION = 'My first Python package with a slightly longer description. This is my added description.'

# Setting up
setup(
        name="EmmaMatiCalPackage", 
        version=VERSION,
        author="Emma Hall",
        author_email="<elohall01@gmail.com>",
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