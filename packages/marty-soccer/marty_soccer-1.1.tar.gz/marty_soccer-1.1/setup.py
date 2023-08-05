from distutils.core import setup
setup(
    name='marty_soccer',
    packages=['marty_soccer'],
    package_dir = {'': 'src'},
    version='1.1',
    license='MIT',
    description='marty AI soccer library for education created by DGS',
    author='DGS',
    author_email='dgs.python@dgs.edu.hk',
    url='https://github.com/DGSpython/marty-package',
    download_url='https://github.com/DGSpython/marty-package/archive/refs/tags/v1.1-beta.tar.gz',
    keywords=['DGS', 'Marty', 'Soccer'],
    install_requires=[
        'nums_from_string==0.1.2',
        'martypy==3.3.1',
        'datetime==4.5',
        'pyserial==3.4',
        'packaging==21.3'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
)