# coding: utf-8

from setuptools import setup

setup(
    name='lpi-api',
    version='0.3.4',
    author='François Ménabé',
    author_email='francois.menabe@unistra.fr',
    url='https://github.com/unistra/python-lpi-api',
    license='GPLv3+',
    description='Wrap calls to GLPI REST API.',
    long_description=open('README.rst').read(),
    keywords=['rest', 'api', 'glpi'],
    classifiers=[
        'License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)',
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3'
    ],
    py_modules=['glpi_api'],
    install_requires=['requests']
)
