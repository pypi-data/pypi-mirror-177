# IPdon

IPdon is a fast IP intelligence solution for Python. It benchmarks as the fastest Python library for obtaining IP data. Natively it provides 
* Direct access to Geographical, Network, Company or Domain based information on any IP in the world.
* A 30-40x speed increase versus competing services due to the services algorithm
* Provides a multi-dimensional `dictionary` based response identical to the IPdon service itself.
* Internally utilizes [orjson](https://github.com/ijl/orjson) for fast binary-based serialization.

IPdon supports CPython

 1. [Install](https://github.com/ijl/orjson#install)
 2. [Quickstart](https://github.com/ijl/orjson#quickstart)


## Usage

### Install

To install a wheel from PyPI:

```sh
pip install --upgrade ipdon
```

### Quickstart

This is an example of calling the service

```python
>>> import ipdon
>>> token = "5ae79d31-6e48-4641-a0fd-bcee9cd30ff6" #Leave string "" empty to use the Free tier instead.    
>>> ipdon = IPdon(token)
>>> response = ipdon.query("86.84.0.0", "location/")
>>> print(response["location"])
{'continent': 'Europe', 'region': 'Western Europe', 'country_iso': 'NL', 'country': 'Netherlands', 'state': 'Gelderland', 'city': 'Maasbommel', 'postalcode': '6627', 'latitude': 51.8289, 'longitude': 5.5406, 'currency': 'Euro', 'languages': ['nl-NL', 'fy-NL'], 'dialcode': '31', 'map_image': 'https://staticmap.thisipcan.cyou/?lat=51.8289&lon=5.5406'}
