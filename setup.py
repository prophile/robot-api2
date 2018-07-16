from setuptools import setup, find_packages


with open('README.rst') as f:
    long_description = f.read()


setup(
    name='robot-api2',
    version='0.1.0',
    packages=find_packages(),
    description='Robot API',
    long_description=long_description,
    author='Alistair Lynn',
    author_email='alistair@alynn.co.uk',
    url='about:blank',
    license='MIT',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering',
    ],
    tests_require=[
        'pytest',
        'pytest-cov',
    ],
)
