# CRGOAUTH stand for `Cloudreach Google SignIn OAUTH`

## Autentication and authorization Overview
This package will be published on PyPi as downloadable package.
The main purpose of it is to Oauth2 authenticate a user of the Jupiter Notebook (**JpN**) that will need access to Google Sheets application. The security context is the current macOS user who use the Jupiter notebook and is logged in with Google's account.
In order to ustilize the Google's Sheets API the JpN code would need to:
- install the package `crgoauth` from PyPi;
- recieve a file `credentials.json` from her line manager and copy it to `~/crgoauth` folder. This file contains the JpN application's credentials. The security context for the credentials is `https://www.googleapis.com/auth/spreadsheets`;
- Logging in the Cloudreach's google account and in the prompted window authorized the JpN application to access the Google Sheets API.


### HowTos
- [The guide](https://github.com/MichaelKim0407/tutorial-pip-package) to publish python package on GitHub

- [Building and Distributing Packages with Setuptools](https://setuptools.pypa.io/en/latest/setuptools.html)

- when the package is published on GitHub, install it by:

```bash
   $ pip install git+git://github.com/nikolay-tonev/crgoauth.git#egg=crgoauth
```

- to build the package from the local macOS terminal:
```zsh

   python setup.py sdist
```

- testing PyPi for used files:
```zsh

  twine upload --repository testpypi dist/*
```

- to publish on PyPi from the local macOS terminal (change the file name with the latest build):
```zsh
   
   twine upload dist/crgoauth-0.0.1.dev0.tar.gz
```
