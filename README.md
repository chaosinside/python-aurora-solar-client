# Python Aurora Solar Client

A python client for the Aurora Solar API.

### Dependencies
* requests

### Getting Started

	pip install AuroraSolarClient

### Usage
AuroraSolarClient must be initialized with a tenant_id, api_key, and api_secret. Once intialized, you can use any of the provided functions to return a requests response object.

### Example
```python
from .client import AuroraSolarClient

tenant_id = "my_tenant_id"
api_key = "my_api_key"
api_secret = "my_api_secret"
aurora_project_id = "my_aurora_project_id"

client = AuroraSolarClient(tenant_id, api_key, api_secret)
response = client.get_project(aurora_project_id)
print("response:", response.text)
```
