from setuptools import setup, find_packages
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='encpy',
    packages=find_packages(),
    include_package_data=True,
    version="1.0.0",
    description='Python encryption!',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ITSN0B1T4',
    author_email='toxinum.org@gmail.com',
    #install_requires=[],

    
    keywords=["python encrypt"],
    classifiers=[
            'Development Status :: 4 - Beta',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: MIT License',
            'Programming Language :: Python :: 2',
            'Operating System :: OS Independent',
            'Environment :: Console',
    ],
    
    license='MIT',
    entry_points={
            'console_scripts': [
                'encpy = encpy.encpy:encpy',
            ],
    },
    python_requires='>=3.9.5'
)
