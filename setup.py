#!/usr/bin/env python
from setuptools import setup, find_packages


setup(
    name='django-flowplayer',
    version='0.3.1',
    description='Mediaplayer application for Django based on flowplayer flash player',

    author='Martin Fitzpatrick',
    author_email='martin.fitzpatrick@gmail.com',
    license='BSD',
    url='http://github.com/mfitzp/django-flowplayer',

    packages=find_packages(exclude=['tests.*', 'tests', 'example.*', 'example']),
    include_package_data=True, # declarations in MANIFEST.in

    install_requires=['Django >=1.3'],
    tests_require=['Django >=1.3'],
#~ Nestor 
    #~ Nestor test_loader='tests:loader',
    #~ Nestor test_suite='tests.everything',

    classifiers=[
        'Environment :: Web Environment',
        'Development Status :: 4 - Beta',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
    ],
)
