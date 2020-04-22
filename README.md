# Python Aurora Solar Client

This is a generic client that can be used to integrate with the Aurora Solar API.

### Requirements
* Python (with pip)
* requests

### Getting Started

It is recommended that you create a virtual environment and then simply install the requests library.

#### Creating a virtual environment
##### MacOS/Linux
	python3 -m venv pyenv
	source pyenv/bin/activate

##### Windows
	py -m venv pyenv
	.\pyenv\Scripts\activate

#### Install Requests

	pip install requests

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
