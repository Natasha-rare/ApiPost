from datetime import datetime

from requests import get, post, delete


print(get('http://localhost:5000/api/v2/jobs').json())
print(post('http://localhost:5000/api/v2/jobs',
            json={'job': 'development new robots',
                  'team_leader': 1,
                  'work_size': 25,
                  'collaborators': '2, 3',
                  'is_finished': False
                  }).json())  # cool request

print(post('http://localhost:5000/api/v2/jobs',
            json={'job': 'development new robots',
                  'team_leader': 1
                  }).json())  # cool request
print(get('http://localhost:5000/api/v2/jobs').json())

print(get('http://localhost:5000/api/v2/jobs/3').json())

print(get('http://localhost:5000/api/v2/jobs/999').json())


print(get('http://localhost:5000/api/v2/jobs/q').json())

print(delete('http://localhost:5000/api/v2/jobs/999').json())
# новости с id = 999 нет в базе

print(delete('http://localhost:5000/api/v2/jobs/3').json())