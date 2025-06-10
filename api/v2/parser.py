from flask_restful.reqparse import RequestParser


class ParserUsers(RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('login', required=True)
        self.add_argument('is_admin', required=False)
        self.add_argument('password', required=False)

class ParserCars(RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('brand', required=True)
        self.add_argument('model', required=True)
        self.add_argument('year', required=True)
        self.add_argument('is_taken', required=False)
        self.add_argument('place_id', required=True)
        self.add_argument('image', required=False)

class ParserPlaces(RequestParser):
    def __init__(self):
        super().__init__()
        self.add_argument('name', required=True)
        self.add_argument('owner_id', required=True)
        self.add_argument('address', required=True)