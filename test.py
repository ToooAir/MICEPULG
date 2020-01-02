def test1(func):
    def wrapper(*args,**kwargs):
        print("test1 start!")
        func(*args,**kwargs)
        print("test1 end!")
    return wrapper

def test2(func):
    def wrapper(*args,**kwargs):
        print("test2 start!")
        func(*args,**kwargs)
        print("test2 end!")
    return wrapper

@test1
@test2
def test3(name):
    print(name)

test4 = test3("GG")