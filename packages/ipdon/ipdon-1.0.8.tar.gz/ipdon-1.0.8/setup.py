import setuptools

long_desc = open("README.md").read()
required = ["orjson", "requests"] # Comma seperated dependent libraries name

setuptools.setup(
    name="ipdon",
    version="1.0.8",
    author="Christian",
    author_email="christian@ipdon.com",
    license="MIT",
    description="IPdon is a low-latency IP intelligence API for Python",    
    long_description="""# IPdon

[IPdon](https://ipdon.com) is a fast IP intelligence solution. This is the official Python library which benchmarks as the fastest Python library for obtaining data from any IP. 

Natively it provides: 
* Direct access to Geographical, Network, Company or Domain based information on any IP in the world.
* A 30-40x speed increase versus competing services due to the services algorithm
* Provides a multi-dimensional `dictionary` response identical to the IPdon service itself.
* Internally utilizes [orjson](https://github.com/ijl/orjson) for fast binary-based serialization.
* Has a free tier without needing an API key (token) Learn more about [plans](https://ipdon.com/pricing) here.

IPdon happily supports CPython

## Usage

### Install

To install a wheel from PyPI:

```sh
pip install --upgrade ipdon
```

### Quickstart

This is an example of calling the service

```python
from ipdon import IPdon

# Leave string '' empty to use the Free tier.
token = '5ae79d31-6e48-4641-a0fd-bcee9cd30ff6' 
ipdon = IPdon(token)

# You can add another argument to filter response (faster), use ipdon.query(<ip>, <filter>)
response = ipdon.query('34.241.171.232') 

print(response)
```

Example response:
```
{   'abuse': {'contacts': ['abuse@amazonaws.com']},
    'domains': ['might-d-light.com'],
    'location': {   'city': 'Dublin',
                    'continent': 'Europe',
                    'country': 'Ireland',
                    'country_iso': 'IE',
                    'currency': 'Euro',
                    'dialcode': '353',
                    'languages': ['en-IE', 'ga-IE'],
                    'latitude': 53.3379,
                    'longitude': -6.2591,
                    'map_image': 'https://staticmap.thisipcan.cyou/?lat=53.3379&lon=-6.2591',
                    'postalcode': 'D02',
                    'region': 'Northern Europe',
                    'state': 'Leinster'},
    'network': {   'cidr_size': 4194304.0,
                   'cidr_subsegment': '34.240.0.0/13',
                   'ip_subsegment_end': '34.247.255.255',
                   'ip_subsegment_end_int': 586678271,
                   'ip_subsegment_start': '34.240.0.0',
                   'ip_subsegment_start_int': 586153984,
                   'ip_type': 'ipv4',
                   'rir': 'arin',
                   'rir_cidr_segment': '34.192.0.0/10'},
    'organization': {   'asn': '16509',
                        'description': 'Amazon NA Prefix',
                        'name': 'NET34'},
    'request': {   'query': '34.241.171.232',
                   'status': 'success',
                   'subscription': False},
    'time': {   'timezone': 'Europe/Dublin',
                'timezone_is_dst': True,
                'timezone_utc_offset': 0.0}}
```
See IPdon documentation for an elaborate description on how to use the API [here](https://ipdon.com/documentation)

""",
    long_description_content_type="text/markdown",
    url="https://github.com/cwittenberg/ipdon/tree/main/python",    
    project_urls={
        "Bug Tracker": "https://github.com/cwittenberg/ipdon/issues",
    },
    key_words="IP intelligence, IP service, IP api, geoip, geographical IP, IP tacking",
    install_requires=required,
    packages=['ipdon'],
    python_requires=">=3.6",
)