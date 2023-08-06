from setuptools import setup, find_packages
import os
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='webvibe',
    packages=find_packages(),
    include_package_data=True,
    version="2.0.5",
    description='',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ITSN0B1T4',
    author_email='toxinum.org@gmail.com',
    install_requires=["whois", "pytz", "requests"],

  
    keywords=["webvibe"],
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'Environment :: Console',
    ],
    
    license='MIT',
    entry_points={
            'console_scripts': [
                'webvibe = webvibe.webvibe:main',
            ],
    },
    python_requires='>=3.9.5'
)
