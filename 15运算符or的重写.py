"""
需求：
让a|b|c的代码得到一个自定义的类对象（类似列表即[a,b,c]）
调用run方法依次输出a,b,c
需要重写  | 即__or__方法
"""

class MyTest(object):
    def __init__(self,name):
        self.name = name

    def __or__(self, other):
        return MySequence(self,other)

    def __str__(self):          # 魔法，想打印什么就打印什么 
        return self.name

class MySequence(object):
    def __init__(self,*args):
        self.sequence = []
        for arg in args:
            self.sequence.append(arg)

    def __or__(self, other):
        self.sequence.append(other)
        return self

    def run(self):
        for i in self.sequence:
            print(i)

if __name__ == '__main__':
    a = MyTest('a')
    b = MyTest('b')
    c = MyTest('c')

    d = a | b | c

    d.run()
    print(type(d))
