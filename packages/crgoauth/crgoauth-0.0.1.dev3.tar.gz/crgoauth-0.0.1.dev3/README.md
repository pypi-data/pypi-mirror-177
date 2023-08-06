# CRGOAUTH stand for `Cloudreach Google SignIn OAUTH`


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
