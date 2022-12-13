# Bravia

Welcome to bravia's documentation!

## What is it?

bravia is a python module for Sony Bravia Professional Displays running Android.
See [Sony Developer docs](https://pro-bravia.sony.net/develop/integrate/ip-control/index.html)
for more details.

## What can it do?

bravia will let you control some functions of the display via an API. Some functions require
pre-shared key configuration on the display. They are documented in the developer docs reference
in the [What is it?](#What-is-it?) section.

# Quickstart

## Import bravia

```python
    >>> from bravia import Bravia
```

## Create an instance of the Bravia class

```python
    >>> b = Bravia(ip='192.168.1.25')
```

## Make a request

This will show the API for each service available on the display. Use this developer docs referenced in
[What is it?](#What-is-it?) to see more functionality.

```python
    >>> b.api_info()
```

# Documentation

[Read the docs](https://bravia.readthedocs.io/en/latest/index.html)

[View on github](https://github.com/baconismycopilot/bravia)
