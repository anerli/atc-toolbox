# ATC Toolbox
ATC Toolbox was written by members of Algorithmic Trading Club at ISU and is meant for use by ATC members, as well as anyone else who feels like using it. 

This is a set of tools that can be used for financial data analysis, for use in trading algorithms, and whatever else you might desire to use it for.

## Installation

Normally you install modules with `pip install packagename`, however since this is not on pypi (the pip package repository), you have to install it slightly differently.

Clone (or just download if you want) this repository, and (assuming you are running a terminal in the parent directory of this repository) `pip install -e atc-toolbox`. Then you will be able to access the `atc_toolbox` module from python. The -e flag means that when you pull new changes from atc-toolbox the changes will be automatically reflected without having to pip re-install it.

## Docs
- There are no docs for this yet :(
- For now look at the code to see what stuff does.

## Examples

See the [examples](./examples) folder.

## How to use the Test Suite

### Downloading Data
- Make sure to install the the repository as a package first

Run:
```
python -m atc_toolbox.test_suite.synchronizer
```

### Test a Model against the Test Database
See the example script [using_test_suite.py](./examples/using_test_suite.py).
