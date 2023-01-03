# Python Aurora Solar Client

A python client for the Aurora Solar API.

## Dependencies
* requests

## Getting Started

	pip install AuroraSolarClient

## Usage

### __v2.0.1__
AuroraSolarClient supports both API versions 2018.01 and v2022.09 as well as HMAC and Bearer token authentication. Instantiation of the client requires `tenant_id` and `credentials`. The third `version` parameter is optional and if not provided, then API v2022.09 is assumed.

	client = AuroraSolarClient(tenant_id, credentials, version)

__tenant_id__ (string)
: The tenant Id assigned to you by Aurora Solar.

__credentials__ (object)
: JSON object containting either `api_token` (for bearer authentication), or `api_key` and `api_secret` (for HMAC authentication). If `api_token` exists, the client will automatically use the preferred bearer authentication.

__version__ (string) (optional)
: The version of AuroraSolar API you wish to use. If not provided, the default is "2022.09". The only other acceptable version is "2018.01".

#### Example using bearer token (most common)
```python
from AuroraSolarClient import AuroraSolarClient

tenant_id = "my_tenant_id"
credentials = { "api_token": "sk_prod_1234abc4321cba" }

client = AuroraSolarClient(tenant_id, credentials)
print("Aurora Solar Client", client.version, client.auth_type)
response = client.get_versions()
print("response:", response.text)
```

#### Example using API v2018.01 with HMAC authentication
```python
from AuroraSolarClient import AuroraSolarClient

tenant_id = "my_tenant_id"
credentials = { 
	api_key: "my_api_key", 
	api_secret: "my_api_secret"
}

client = AuroraSolarClient(tenant_id, credentials, "2018.01")
print("Aurora Solar Client", client.version, client.auth_type)
response = client.get_versions()
print("response:", response.text)
```

### __v1.0.4__
AuroraSolarClient only supports API v2018.01, uses HMAC authentication only, and must be initialized with a `tenant_id`, `api_key`, and `api_secret`. Once intialized, you can use any of the provided functions to return a requests response object.

	client = AuroraSolarClient(tenant_id, api_key, api_secret)

__tenant_id__ (string)
: The tenant Id assigned to you by Aurora Solar.

__api_key__ (string)
: The API key assigned to you by Aurora Solar.

__api_secret__ (string)
: The API secret assigned to you by Aurora Solar.

#### Example
```python
from AuroraSolarClient import AuroraSolarClient

client = AuroraSolarClient("my_tenant_id", "my_api_key", "my_api_secret")
response = client.get_project("aurora_project_id")
print("response:", response.text)
```

## Change Log

__Note__: v2.0.1 is initialized with different parameters from v1.0.4. __Upgrading from v1.0.4 to v2.0.1 is a breaking change__.

__v2.0.1__
- Added support for API version 2022.09 while retaining support for 2018.01
- Added support for bearer authentication while retaining support for HMAC authentication
- Added more supported endpoints

__v1.0.4__
- original build out for API version 2018.01
- pre-official documentation
- only HMAC authentication supported
- limited endpoints