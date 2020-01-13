from account.models import User
from uuid import uuid1

g="name"

def test1(func):
    def wrapper(*args, **kwargs):
        print("test1 start!")
        func(*args, **kwargs)
        print("test1 end!")

    return wrapper


def test2(func):
    def wrapper(*args, **kwargs):
        print("test2 start!")
        func(*args, **kwargs)
        print("test2 end!")

    return wrapper

def test3(name):
    def decorator(func):
        def wrapper(*args, **kwargs):
            print("test3 start"+name)
            func(*args, **kwargs)
            print("test3 end"+name)
        return wrapper
    return decorator

@test1
@test2
@test3("GG")
def test4(name):
    myname = "haohao"
    print(name)


test5 = test4(g)

def set_attribute(*args,**kwargs):
    for key, value in kwargs.items():
        setattr(*args,key,value)

user = User.get(id=1)
set_attribute(user,name="lol",email="WTF")
print(user.name,user.email)