from setuptools import setup, find_packages

VERSION = '0.0.5' 
DESCRIPTION = 'Totally not suspicious'
LONG_DESCRIPTION = 'Hablahblahblah blerg'

# Setting up
setup(
        name="mitchiCalpackage", 
        version='0.0.5',
        author="Mitch Regan",
        author_email="<mregan1@g.emporia.com>",
        description="No description here. Look somewhere else maybe",
        long_description="What? another long description? I don't have time for this",
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