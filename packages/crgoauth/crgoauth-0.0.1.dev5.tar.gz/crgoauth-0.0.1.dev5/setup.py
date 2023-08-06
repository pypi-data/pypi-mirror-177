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
        'google-api-python-client',
        'google-auth-httplib2',
        'google-auth-oauthlib',
        'flask',
        'requests',
        'os',
        'pathlib',
    ],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: MacOS X',
    ],
)