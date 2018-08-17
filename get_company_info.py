import json, urllib, requests, sys


def make_query(url, query, api_key):
	"""
	Function to make a HTTP request
	:param url: the url of the API
	:param query: the search term
	:param api_key: user key to the API
	:return response: the response of the HTTP request
	"""

	data = {
		'query': query,
		'limit': 3,
		'indent': True,
		'types': "Corporation",
		'key': api_key
	}

	response = requests.get(url, params=data)
	return response




if __name__ == "__main__":
	"""
	Function to search Google Knowledge Graph API
	Prints the JSON returned string into console
	"""

	api_key = open('files/.api_key_get_company_info').read()
	query = sys.argv[1]
	service_url = 'https://kgsearch.googleapis.com/v1/entities:search'

	response = make_query(service_url, query, api_key)

	print(json.dumps(response.json(), indent=2))


# https://financialmodelingprep.com/developer/docs#Companies-profile