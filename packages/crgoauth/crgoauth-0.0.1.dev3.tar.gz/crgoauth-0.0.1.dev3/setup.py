from setuptools import setup, find_packages

from crgoauth import __version__

setup (
    name='crgoauth',
    version=__version__,
    description='Cloudreach implementation of Google SignIn OAuth',

    url='https://github.com/nikolay-tonev/crgoauth',
    author='Cloudreach',
    author_email='nikolay.tonev@cloudreach.com',

    packages=find_packages(),

    install_requires=[
        'returns-decorator>=1.1',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: MacOS X',
    ],
)