import psycopg2

connection = psycopg2.connect(
    database='project',
    user='postgres',
    password=123,
    host='localhost'
)


class CharField:
    def __init__(self, username):
        self.username = username

    def __get__(self, instance, owner):
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError('username must be str')


class PasswordField:
    def __init__(self, password):
        self.password = password

    def __set__(self, instance, value):
        if not isinstance(value, int):
            raise TypeError('Password must be integer')


def commit(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        conn.commit()
        return result

    return wrapper


class User:
    username = CharField()
    password = PasswordField()
    phone_number = PhoneNumber()
