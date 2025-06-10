from requests import get, post, put, delete

print('get cars')
print(get('http://localhost:8080/api/v2/cars').json())
print('add car')
print(post('http://localhost:8080/api/v2/cars',
           json={'brand': 'LADA', 'model': '2172', 'year': '2012', 'is_taken': 'false', 'place_id': 1,
                 'image': 'default.png'}).json())
print('get 1 car')
print(get('http://localhost:8080/api/v2/cars/2').json())
print('update car')
print(put('http://localhost:8080/api/v2/cars/2',
          json={'brand': 'LADA', 'model': '2172', 'year': '2012', 'is_taken': 'true', 'place_id': 1,
                'image': 'default.png'}).json())
print('updated car')
print(get('http://localhost:8080/api/v2/cars/2').json())
print('delete car')
print(delete('http://localhost:8080/api/v2/cars/2').json())
print('all cars')
print(get('http://localhost:8080/api/v2/cars').json())
