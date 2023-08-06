from setuptools import setup, find_packages
from sys import platform

VERSION = '0.0.1'
DESCRIPTION = 'test_package_for_blendedUx'
LONG_DESCRIPTION = 'A Test Package for blendedUx'

js_lib = 'PyExecJS'
if platform.lower().startswith('linux') or platform.lower().startswith('darwin'):
    js_lib = 'py-mini-racer==0.1.18' 

# Setting up
setup(
    name="blendedUx_staging",
    version=VERSION,
    author="Sunny Prakash",
    author_email="<sprakash@cognam.com>",
    description=DESCRIPTION,
    packages=find_packages(),
    include_package_data=True,
    package_data={'':['*.js']},

    install_requires=[
        
        'colorama==0.4.1',         
        'certifi==2022.5.18.1',
        'click==5.1',
        'colorama==0.4.1',
        'Flask==0.11.1',
        'itsdangerous==2.0.1',
        'Jinja2==2.8',
        'MarkupSafe==1.1.1',
        'Pillow==8.0.1',
        'python-dateutil==2.8.2',
        'six==1.16.0',
        'urllib3==1.26.9',
        'Werkzeug==2.0.1',
        'blendedUx-Lang==1.0.0', 
        'PyYAML==5.2', 
        'antlr4-python2-runtime==4.5.2', 
        'beautifultable==0.8.0',
        'blendedUx-Lang==1.0.0',
        'cmd2==0.8.2',
        'requests',
        'cliff==2.16.0',
        'django==1.8.4', 
        'jinja2==2.8.0', 
        'json_source_map==1.0.4',  
        js_lib
        # 'blendedcli@git+https://github.com/agua-man/blended-python.git@linter_branch#subdirectory=blendedcli',
    ],

        entry_points={
        'console_scripts': [
            'blended = blended.blendedcli.blendedcli:main',
            'bd = blended.blendedcli.blendedcli:main'
        ],
    },

)