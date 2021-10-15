<p align="center">
    <img src="docs/_static/logo.png" width="328">
</p>
<p align="center">
    <strong>C</strong>omputer <strong>I</strong>mage <strong>Li</strong>keness A<strong>ss</strong>essing <strong>A</strong>utomation
</p>
<p align="center">
    <!-- Badges -->
    <img src="https://github.com/exler/CILISSA/actions/workflows/quality.yml/badge.svg">
    <img src="https://github.com/exler/CILISSA/actions/workflows/tests.yml/badge.svg">
    <a href="https://codecov.io/gh/exler/CILISSA">
        <img src="https://codecov.io/gh/exler/CILISSA/branch/main/graph/badge.svg?token=Dixb5buMQr"/>
    </a>
    <a href="https://cilissa.readthedocs.io/en/latest/">
        <img src="https://img.shields.io/readthedocs/cilissa">
    </a>    
</p>

## Overview

CILISSA allows for the use of various metrics to perform full reference image comparisons. 

It features most popular full reference image quality metrics, image transformations and translations.
CILISSA is also very extensible and new operations can be easily added.

CILISSA has an optional Qt-based graphical interface that lets you experiment with various operations, its orders and properties.

## Requirements

* Python >= 3.7

## Installation
### Build from source

```bash
# Using poetry
$ poetry install

# Install optional dependencies for GUI
$ poetry install -E gui
```

## Usage

### GUI

Information about the GUI can be found in the [cilissa_gui/README.md](cilissa_gui/README.md) file.

### CLI

Currently the CLI only supports working with a single pair of images.

The parameters of metrics and transformations can be modified by passing them to the `--kwargs` argument using the following format:
```
<operation-name>-<parameter-name>=<value>
``` 
where `parameter-name` uses hyphens (-) instead of underscores (_)

## Documentation

Documentation is hosted on [Read the Docs](https://cilissa.readthedocs.io/).
