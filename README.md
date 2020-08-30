# jsonVC

Tiny version control for json data

---

[![Python version](https://img.shields.io/pypi/pyversions/jsonvc.svg)](https://img.shields.io/pypi/pyversions/jsonvc.svg)
[![PyPI version](https://badge.fury.io/py/pypipal.svg)](https://badge.fury.io/py/pypipal)
[![MIT License](https://img.shields.io/badge/license-MIT-blue.svg?style=flat)](http://choosealicense.com/licenses/mit/)
[![Released with pypipal](https://img.shields.io/static/v1?label=released%20with&message=pypipal&color=informational)](https://test.pypi.org/project/pypipal/)

---

# Contents

[Description](#Description)

[Installation](#Installation)

[Usage](#Usage)

[Known Issues](#Known Issues)

[License](#License)

# Description

> Store json data as a list of changes and deletions,
> being able to reset data by index or to a certain
> point in time.

# Installation

```shell script
pip install jsonvc
```

# Usage

- Typical Examples:

```python
# load json data as a dict-like object and change its value
repo = JSONVC('/path/to/repo.jsonvc')
repo['change'] = True
```

```python
# by default changes get auto-added and auto-commited
repo = JSONVC('/path/to/repo.jsonvc')
repo.update(dict(hello='world'))
repo.add()
repo.commit()
```

**More will follow in the future**

# Known Issues

At moment, changes to stored objects within the json dictionary
(e.g. `dict`, `list`) are not properly registered. 

# License

[MIT](https://choosealicense.com/licenses/mit/)

---

_This file was automatically created with the help of **pypipal**._

