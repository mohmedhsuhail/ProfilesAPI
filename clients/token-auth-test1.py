import requests

def client():
	
	credentials = {'username':'suhail','password':'Praniv8@g'}

	response = requests.post('http://127.0.0.1:8000/api/rest-auth/login/',
							 data=credentials)
	'''token_h = 'Token 89bc12d882709d47d501e1fbdb245d8a24ca0701'

	headers = {'Authorization': token_h}

	response = requests.get('http://127.0.0.1:8000/api/profiles/',headers=headers)'''

	print('status code: ',response.status_code)
	response_data = response.json()
	print(response_data)

if __name__=="__main__":
	client()