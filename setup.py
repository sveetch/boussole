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
        'Programming Language :: Python',
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.4",
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        "Development Status :: 5 - Production/Stable",
        'Intended Audience :: Developers',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    install_requires=[
        'six',
        'click>=5.1,<6.0',
        'pathtools==0.1.2',
        'watchdog==0.8.3',
        'libsass>=0.11.2',
        'colorama',
        'colorlog',
    ],
    tests_require=[
        'pytest',
        'pytest-catchlog',
    ],
    entry_points={
        'console_scripts': [
            'boussole = boussole.cli.console_script:cli_frontend',
        ]
    },
    include_package_data=True,
    zip_safe=False
)