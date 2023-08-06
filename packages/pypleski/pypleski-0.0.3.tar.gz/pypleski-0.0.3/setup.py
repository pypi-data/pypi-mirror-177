from setuptools import setup

setup(
    name='pypleski',
    version='0.0.3',    
    description='Simplified API access of the PLESK XML API',
    url='https://codingcow.de/pypleski',
    author='Uli Toll',
    author_email='pypleski@codingcow.de',
    packages=['pypleski'],
    install_requires=['xmltodict',                                           
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)',  
        'Operating System :: POSIX :: Linux',   
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.8',
    ],
)


