class Hello:
    def __init__(self):
        pass


b = Hello()
a = [b, 2, "a"]
print(a)
del b
print(a)
del a[0]
print(a)
del a
print(a)
