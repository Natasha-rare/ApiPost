from requests import get, post


print(post('http://localhost:5000/api/v2/users',
           json={'name': 'Ivan', 'surname': 'Best', 'email':'123@1.c',
                 'age': 30, 'position': 'special', 'speciality': 'doctor',
                 'address': 'absd', 'city_from': 'Moscow', 'hashed_password': '1234'}).json())
print(post('http://localhost:5000/api/v2/users',
           json={'name': 'nac'}).json())
print(get('http://localhost:5000/api/v2/users/1').json())