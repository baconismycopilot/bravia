# Bravia

This is a work in progress.

bravia is a python package to interact with the
Sony Bravia line of displays. 


[Sony Developer Docs](https://pro-bravia.sony.net/develop/integrate/ip-control/index.html)

Example:

```python
>>> from bravia import Bravia
>>> b = Bravia(ip='192.168.1.25')
>>> b.api_info()
```
