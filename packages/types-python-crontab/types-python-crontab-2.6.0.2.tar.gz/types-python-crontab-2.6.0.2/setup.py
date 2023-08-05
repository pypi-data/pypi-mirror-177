from setuptools import setup

name = "types-python-crontab"
description = "Typing stubs for python-crontab"
long_description = '''
## Typing stubs for python-crontab

This is a PEP 561 type stub package for the `python-crontab` package.
It can be used by type-checking tools like mypy, PyCharm, pytype etc. to check code
that uses `python-crontab`. The source for this package can be found at
https://github.com/python/typeshed/tree/main/stubs/python-crontab. All fixes for
types and metadata should be contributed there.

See https://github.com/python/typeshed/blob/main/README.md for more details.
This package was generated from typeshed commit `c6261372d7a43c71600de07ecfdf0692f74d6d85`.
'''.lstrip()

setup(name=name,
      version="2.6.0.2",
      description=description,
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/python/typeshed",
      project_urls={
          "GitHub": "https://github.com/python/typeshed",
          "Changes": "https://github.com/typeshed-internal/stub_uploader/blob/main/data/changelogs/python-crontab.md",
          "Issue tracker": "https://github.com/python/typeshed/issues",
          "Chat": "https://gitter.im/python/typing",
      },
      install_requires=[],
      packages=['cronlog-stubs', 'crontabs-stubs', 'crontab-stubs'],
      package_data={'cronlog-stubs': ['__init__.pyi', 'METADATA.toml'], 'crontabs-stubs': ['__init__.pyi', 'METADATA.toml'], 'crontab-stubs': ['__init__.pyi', 'METADATA.toml']},
      license="Apache-2.0 license",
      classifiers=[
          "License :: OSI Approved :: Apache Software License",
          "Programming Language :: Python :: 3",
          "Typing :: Stubs Only",
      ]
)
