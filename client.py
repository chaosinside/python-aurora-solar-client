import requests, json, hashlib, hmac, base64, urllib.parse
from datetime import datetime

class AuroraClient:
	# static variables
	BASE_URL = "https://api.aurorasolar.com"
	headers = { "Content-Type": "application/json", "Accept": "application/json" }

	def __init__(self, tenant_id, api_key, api_secret):
		# instance variables
		self.tenant_id = tenant_id
		self.api_key = api_key
		self.api_secret = api_secret

	def create_project(self, payload):
		endpoint = "/v2/tenants/"+ self.tenant_id +"/projects"
		url = self.signed_url("POST", endpoint, payload)
		response = requests.post(url, headers=self.headers, data=json.dumps(payload))
		return response

	def get_project(self, project_id):
		endpoint = "/v2/tenants/"+ self.tenant_id +"/projects/"+ project_id
		url = self.signed_url("GET", endpoint)
		response = requests.get(url, headers=self.headers)
		return response

	def get_designs(self, project_id):
		endpoint = "/v2/tenants/"+ self.tenant_id +"/projects/"+ project_id +"/designs"
		url = self.signed_url("GET", endpoint)
		response = requests.get(url, headers=self.headers)
		return response

	def get_design_summary(self, design_id):
		endpoint = "/v2/tenants/"+ self.tenant_id +"/designs/"+ design_id +"/summary"
		url = self.signed_url("GET", endpoint)
		response = requests.get(url, headers=self.headers)
		return response

	def get_design_assets(self, design_id):
		endpoint = "/v2/tenants/"+ self.tenant_id +"/designs/"+ design_id +"/assets"
		url = self.signed_url("GET", endpoint)
		response = requests.get(url, headers=self.headers)
		return response

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

	# payload needs to be sorted by key and flattened for signature
	def order_and_flatten(self, payload):
		object_name = next(iter(payload))
		object_data = payload[object_name]
		sortedkeys = sorted(object_data.keys(), key=str.lower)
		out = ""
		for key in sortedkeys:
			if len(out) > 0: out += "&"
			out += object_name +"."+ key +"="+ urllib.parse.quote(str(object_data[key]), safe=",()")
		return out