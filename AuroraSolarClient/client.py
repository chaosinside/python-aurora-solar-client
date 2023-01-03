import requests, json, hashlib, hmac, base64, urllib.parse
from datetime import datetime

class AuroraSolarClient:
	BASE_URL = "https://api.aurorasolar.com"
	headers = { "Content-Type": "application/json", "Accept": "application/json" }

	def __init__(self, tenant_id, credentials, version="2022.09"):
		self.tenant_id = tenant_id
		self.version = version
		if credentials.get("api_token") != None:
			self.auth_type = "bearer"
			self.api_token = credentials.get("api_token")
			self.headers = {**self.headers, "Authorization": "Bearer "+ self.api_token }
		else:
			self.auth_type = "hmac"
			self.api_key = credentials.get("api_key")
			self.api_secret = credentials.get("api_secret")

	def create_project(self, payload):
		endpoint = "/tenants/"+ self.tenant_id +"/projects"
		response = requests.post(self.url(endpoint, "POST", payload), headers=self.headers, data=json.dumps(payload))
		return response

	def get_project(self, project_id):
		endpoint = "/tenants/"+ self.tenant_id +"/projects/"+ project_id
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_projects(self):
		endpoint = "/tenants/"+ self.tenant_id +"/projects"
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_designs(self, project_id):
		endpoint = "/tenants/"+ self.tenant_id +"/projects/"+ project_id +"/designs"
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_design_summary(self, design_id):
		endpoint = "/tenants/"+ self.tenant_id +"/designs/"+ design_id +"/summary"
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_design_assets(self, design_id):
		endpoint = "/tenants/"+ self.tenant_id +"/designs/"+ design_id +"/assets"
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_design_pricing(self, design_id):
		endpoint = "/tenants/"+ self.tenant_id +"/designs/"+ design_id +"/pricing"
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_design_roof_summary(self, design_id):
		endpoint = "/tenants/"+ self.tenant_id +"/designs/"+ design_id +"/roof_summary"
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_design_web_proposal(self, design_id):
		endpoint = "/tenants/"+ self.tenant_id +"/designs/"+ design_id +"/web_proposal"
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_roles(self):
		endpoint = "/tenants/"+ self.tenant_id +"/roles"
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_sso_provider(self):
		endpoint = "/tenants/"+ self.tenant_id +"/sso_provider"
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_tenant(self):
		endpoint = "/tenants/"+ self.tenant_id
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_user(self, user_id):
		endpoint = "/tenants/"+ self.tenant_id +"/users/"+ user_id
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_users(self):
		endpoint = "/tenants/"+ self.tenant_id +"/users"
		return requests.get(self.url(endpoint), headers=self.headers)

	def get_versions(self):
		endpoint = "/versions"
		return requests.get(self.url(endpoint), headers=self.headers)

	# returns the proper URL based on version and authentication settings
	def url(self, endpoint, method="GET", payload=None):
		if self.version == "2018.01": endpoint = "/v2"+ endpoint
		if self.auth_type == "hmac": return self.signed_url(method, endpoint, payload)
		else: return self.BASE_URL + endpoint

	# required for HMAC authentication
	def signed_url(self, method, endpoint, payload=None):
		# prepare canonical string
		key_param = "AuroraKey="+ self.api_key
		timestamp_param = "Timestamp=" + datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC").replace(" ","%20")
		canonical_string = method +"\n"+ endpoint +"\n"+ key_param +"\n"+ timestamp_param +"\n"
		if payload != None: canonical_string += self.order_and_flatten(payload) +"\n"
		# create signature (Base64-encoded HMAC-SHA256 hash of canonical string with "=" removed from the end)
		secret = bytes(self.api_secret, "utf-8")
		message = bytes(canonical_string, "utf-8")
		signature = base64.b64encode(hmac.new(secret, message, digestmod=hashlib.sha256).digest())[:-1]
		return self.BASE_URL + endpoint +"?"+ key_param +"&"+ timestamp_param +"&Signature="+ signature.decode()

	# required for HMAC authentication. payload needs to be sorted by key and flattened for signature
	def order_and_flatten(self, payload):
		object_name = next(iter(payload))
		object_data = payload[object_name]
		sortedkeys = sorted(object_data.keys(), key=str.lower)
		out = ""
		for key in sortedkeys:
			if len(out) > 0: out += "&"
			out += object_name +"."+ key +"="+ urllib.parse.quote(str(object_data[key]), safe=",()")
		return out