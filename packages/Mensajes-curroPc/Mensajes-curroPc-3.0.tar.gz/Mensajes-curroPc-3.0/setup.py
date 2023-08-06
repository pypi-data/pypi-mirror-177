from pickletools import long1
from setuptools import setup, find_packages

setup(
    name='Mensajes-curroPc',
    version='3.0',
    description='Un paquete para saludar y despedir',
    long_description=open('README.md').read(), # abre el fichero y lo lee 
    long_description_content_type='text/markdown',
    author='Francisco José',
    author_email='ejemplo@curro.com',
    url='https://www.curro.dev',
    license_files=['LICENSE'],
    packages=find_packages(),
    scripts=[],
    test_suite='tests',
    install_requires=[paquete.strip()
                      for paquete in open("requirements.txt").readlines()],
    classifiers=[
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Utilities',
    ],
)

# pip install build twine --upgrade ==> preprara el constructor/instalador del proyecto para subirlo publicanente a la red de internet