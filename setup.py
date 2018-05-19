from setuptools import setup, find_packages

setup(
    name='boussole',
    version=__import__('boussole').__version__,
    description=__import__('boussole').__doc__,
    long_description=open('README.rst').read(),
    author='David Thenon',
    author_email='sveetch@gmail.com',
    url='https://github.com/sveetch/boussole',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Internet",
        "Topic :: Software Development :: Compilers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    install_requires=[
        'six',
        'click>=5.1,<6.0',
        'pathtools==0.1.2',
        'watchdog==0.8.3',
        'libsass>=0.14.5',
        'pyaml',
        'colorama',
        'colorlog',
    ],
    entry_points={
        'console_scripts': [
            'boussole = boussole.cli.console_script:cli_frontend',
        ]
    },
    include_package_data=True,
    zip_safe=False
)