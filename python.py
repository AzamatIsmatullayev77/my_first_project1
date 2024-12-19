import psycopg2

connection = psycopg2.connect(
    database='project',
    user='postgres',
    password='123',
    host='localhost',
    port=5432
)


class CharField:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")
        instance.__dict__[self.name] = value


class PasswordField:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise TypeError(f"{self.name} must be a string")
        instance.__dict__[self.name] = value


class PhoneNumber:
    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name)

    def __set__(self, instance, value):
        if not isinstance(value, str) or not value.isdigit() or len(value) != 10:
            raise ValueError(f"{self.name} must be a 10-digit string")
        instance.__dict__[self.name] = value


def commit(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        connection.commit()
        return result

    return wrapper


class User:
    username = CharField()
    password = PasswordField()
    phone_number = PhoneNumber()

    def __init__(self, username, password, phone_number):
        self.username = username
        self.password = password
        self.phone_number = phone_number

    @commit
    def save(self):
        with connection.cursor() as cursor:
            cursor.execute(
                "INSERT INTO users (username, password, phone_number) VALUES (%s, %s, %s)",
                (self.username, self.password, self.phone_number)
            )

    @classmethod
    def get(cls, username):
        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT username, password, phone_number FROM users WHERE username = %s",
                (username,)
            )
            result = cursor.fetchone()
            if result:
                return cls(*result)
            else:
                return None
