class A(StandardError):
    def __init__(self):
        print "A"

class A():
    def __init__(self,a):
        print a

A()