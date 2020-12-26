import requests

def client():
	
	'''data = {'username':'admin',
				   'email':'test@tst.com',
				   'password1':'testps123',
				   'password2':'testps123'}

	response = requests.post('http://127.0.0.1:8000/api/rest-auth/registration/',
							 data=data)'''
	token_h = 'Token f38d7254f094447cd1f75ef85b9bba35f93cd049'

	headers = {'Authorization': token_h}

	response = requests.get('http://127.0.0.1:8000/api/profiles/',headers=headers)

	print('status code: ',response.status_code)
	response_data = response.json()
	print(response_data)

if __name__=="__main__":	
	client()