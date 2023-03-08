# 入门学习
参考[廖雪峰python教程](https://www.liaoxuefeng.com/wiki/1016959663602400)
## start 
### hello world
创建一个hello.py文件，文件名只能是数字、字母、下划线的组合，输入：
```python
print('hello world')
```
在命令行执行代码：
```bash
ztc@ztc-ubuntu:~/code/study/python_study$ python hello.py 
hello world
```
在linux环境下也可以./直接执行py文件，加上：
```python
#!/usr/bin/env python3
print('hello world')
```
给文件添加权限：
```bash
chmod a+x hello.py
```
在命令行执行：
```bash
ztc@ztc-ubuntu:~/code/study/python_study$ ./hello.py 
hello world
```
### 输入和输出
#### 输出
```bash
ztc@ztc-ubuntu:~$ python3
>>> print('hello','world')
hello world
```
print()会依次打印每一个字符，遇到逗号","会输出一个空格
#### 输入
```bash
>>> name = input()
>>> name = input('please enter your name:')
tianshu
>>> name
'tianshu'
>>> print(name)
tianshu
>>> print('hello',name)
hello tianshu
```
## python基础
python采用缩进方式\
以`#`开头的语句是注释
### 数据类型和变量
#### 数据类型
- 整形\
  整数，python允许数字中间以`_`分隔
- 浮点型\
  小数，用科学计数法表示，把10用`e`替代
- 字符串\
  以单引号`''`或者双引号`""`括起来的文本，引号不是字符串的一部分，如果字符串内部包含`''`可以用`""`包`''`，如果字符串内部既包含`''`也包含`""`，可以用转义字符`\`来标识，比如
  ```bash
  >>> print("I\'m \"OK\"")
  I'm "OK"
  ```
  \n表示换行，多行换行可以用`'''xxxxx'''`表示，如
  ```bash
  >>> print('''line1
  ... line2
  ... line3''')
  line1
  line2
  line3
  ```
- 布尔值\
  True和False\
  `and`、`or`、`not`运算
#### 变量
`=`赋值
- `/`计算结果是浮点数
- `//`计算结果是整数
- `%`计算结果是余数
### 字符串和编码
`ord()`获取字符串的整数表示，`chr()`把编码转换为对应字符
```bash
>>> ord('A')
65
>>> ord('天')
22825
>>> chr(20070)
'书'
>>> chr(48)
'0'
```
知道字符的整数编码，还可以用十六进制写`str`：
```bash
>>> '\u5929\u4E66'
'天书'
```
在python中的字符串类型是`str`，在内存中以Unicode表示。如果在网络上传输或保存到磁盘，需要把`str`变为以字节为单位的`bytes`。\
python对`bytes`类型的数据用带`b`前缀的单引号或双引号表示：
```python
x = b'ABC'
```
`bytes`每个字符只占一个字节。\
以Unicode表示的`str`通过`encode()`方法可以编码为指定的`bytes`，如：
```bash
>>> 'ABC'.encode('ascii')
b'ABC'
>>> '天书'.encode('utf-8')
b'\xe5\xa4\xa9\xe4\xb9\xa6'
```
把`bytes`变成`str`，用`decode()`方法
```bash
>>> b'\xe5\xa4\xa9\xe4\xb9\xa6'.decode('utf-8')
'天书'
```
计算`str`包含多少个字符，用`len()`函数，换成`bytes`计算字节数：
```bash
>>> len("天书")
2
>>> len("天书".encode('utf-8'))
6
>>> len(b'\xe5\xa4\xa9\xe4\xb9\xa6')
6
```
在python文件开头写上两行保证python解释器按照`UTF-8`编码读取：
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
```
第一行注释是为了告诉Linux/OS X系统，这是一个Python可执行程序，Windows系统会忽略这个注释;\
第二行注释是为了告诉Python解释器，按照`UTF-8`编码读取源代码，否则，你在源代码中写的中文输出可能会有乱码。\
#### 格式化字符串
##### 用占位符
| 占位符 | 替换内容 |
| --- | --- |
| %d | 整数 |
| %f | 浮点数 |
| %s | 字符串 |
| %x | 十六进制整数 |
整数可以补零，浮点数可以指定小数位数
```bash
>>> print('%2d-%02d' % (3, 1))
 3-01
>>> print('%2d-%03d' % (3, 1))
 3-00
 >>> print('%.2f' % 3.1415926)
3.14
```
字符里的`%`要转义，用`%%`来表示`%`
```bash
>>> 'growth rate: %d %%' % 7
'growth rate: 7 %'
```
##### `format()`方法
`format()`方法，会用传入的参数依次代替{0}、{1}...
```bash
>>> 'Hello, {0}, 成绩提升了 {1:.1f}%'.format('小明', 17.125)
'Hello, 小明, 成绩提升了 17.1%'
```
##### `f-string`方法
字符串如果包含{xxx}，直接以对应的变量替换：
```bash
>>> a=1
>>> name="天书"
>>> print(f"your number is {a}, name is {name}")
your number is 1, name is 天书
```
### 使用list和tuple
#### list
列表。有序组合，可以随时添加、删除元素
```bash
>>> classmates = ['Michael', 'Bob', 'Tracy']
>>> classmates
['Michael', 'Bob', 'Tracy']
```
`len()`函数获取list元素个数
```bash
>>> len(classmates)
3
```
用索引获取列表中的元素，索引是从0开始的
```bash
>>> classmates[0]
'Michael'
```
list是可变的有序表，可以在list中追加元素到末尾：
```bash
>>> classmates.append('Adam')
>>> classmates
['Michael', 'Bob', 'Tracy', 'Adam']
```
也可以把元素插入到指定位置，比如索引为`1`的位置：
```bash
>>> classmates.insert(1, 'Jack')
>>> classmates
['Michael', 'Jack', 'Bob', 'Tracy', 'Adam']
```
要删除list末尾的元素，用`pop()`方法：
```bash
>>> classmates.pop()
'Adam'
>>> classmates
['Michael', 'Jack', 'Bob', 'Tracy']
```
要删除指定位置的元素，用`pop(i)`方法，其中`i`是索引位置：
```bash
>>> classmates.pop(1)
'Jack'
>>> classmates
['Michael', 'Bob', 'Tracy']
```
list元素的数据类型可以不同
#### tuple
元祖。有序，一旦初始化就不能修改
```bash
>>> classmates = ('Michael', 'Bob', 'Tracy')
```
### 条件判断
```python
age = 3
if age >= 18:
    print('adult')
elif age >= 6:
    print('teenager')
else:
    print('kid')
```
### 循环
for
```python
names = ['Michael', 'Bob', 'Tracy']
for name in names:
    print(name)
```
while
```python
sum = 0
n = 99
while n > 0:
    sum = sum + n
    n = n - 2
print(sum)
```
`break`跳出循环
`continue`跳出当前循环
### 使用dict和set
#### dict
字典
```bash
>>> d = {'Michael': 95, 'Bob': 75, 'Tracy': 85}
>>> d['Michael']
95
```
可以用dict提供的`get()`方法判断key是否存在
```bash
>>> d.get('Thomas')
>>> d.get('Thomas', -1)
-1
```
删除一个key，用`pop(key)`方法
#### set
有key没有value，元素不可重复，可以用`add()`增，`remove()`删
#### 不可变对象
str是不可变对象
```bash
>>> a = 'abc'
>>> b = a.replace('a', 'A')
>>> b
'Abc'
>>> a
'abc'
```
## 函数
### 调用函数
#### 数据类型转换
```bash
>>> int('123')
123
>>> int(12.34)
12
>>> float('12.34')
12.34
>>> str(1.23)
'1.23'
>>> str(100)
'100'
>>> bool(1)
True
>>> bool('')
False
```
### 定义函数
定义一个函数用`def()`语句
```python
def my_abs(x):
    if x >= 0:
        return x
    else:
        return -x
```
如果你已经把`my_abs()`的函数定义保存为abstest.py文件了，那么，可以在该文件的当前目录下启动Python解释器，用`from abstest import my_abs`来导入`my_abs()`函数，注意abstest是文件名（不含.py扩展名）\
修改一下my_abs的定义，对参数类型做检查，只允许整数和浮点数类型的参数。数据类型检查可以用内置函数isinstance()实现：
```python
def my_abs(x):
    if not isinstance(x, (int, float)):
        raise TypeError('bad operand type')
    if x >= 0:
        return x
    else:
        return -x
```
先定义一个函数，传入一个list，添加一个`END`再返回：
```python
def add_end(L=[]):
    L.append('END')
    return L
```
当你正常调用时，结果似乎不错：
```bash
>>> add_end([1, 2, 3])
[1, 2, 3, 'END']
>>> add_end(['x', 'y', 'z'])
['x', 'y', 'z', 'END']
```
当你使用默认参数调用时，一开始结果也是对的：
```bash
>>> add_end()
['END']
```
但是，再次调用`add_end()`时，结果就不对了：
```bash
>>> add_end()
['END', 'END']
>>> add_end()
['END', 'END', 'END']
```
很多初学者很疑惑，默认参数是[]，但是函数似乎每次都“记住了”上次添加了`'END'`后的list。

原因解释如下：

Python函数在定义的时候，默认参数L的值就被计算出来了，即[]，因为默认参数L也是一个变量，它指向对象[]，每次调用该函数，如果改变了L的内容，则下次调用时，默认参数的内容就变了，不再是函数定义时的[]了。

***定义默认参数要牢记一点：默认参数必须指向不变对象！***

要修改上面的例子，我们可以用`None`这个不变对象来实现：
```python
def add_end(L=None):
    if L is None:
        L = []
    L.append('END')
    return L
```
现在，无论调用多少次，都不会有问题：
```bash
>>> add_end()
['END']
>>> add_end()
['END']
```
#### 可变参数
```python
def calc(*numbers):
    sum = 0
    for n in numbers:
        sum = sum + n * n
    return sum
```
定义可变参数和定义一个list或tuple参数相比，仅仅在参数前面加了一个*号。在函数内部，参数numbers接收到的是一个tuple，因此，函数代码完全不变。但是，调用该函数时，可以传入任意个参数，包括0个参数：
```bash
>>> calc(1, 2)
5
>>> calc()
0
```
如果已经有一个list或者tuple，要调用一个可变参数怎么办？可以这样做：
```bash
>>> nums = [1, 2, 3]
>>> calc(nums[0], nums[1], nums[2])
14
```
这种写法当然是可行的，问题是太繁琐，所以Python允许你在list或tuple前面加一个*号，把list或tuple的元素变成可变参数传进去：
```bash
>>> nums = [1, 2, 3]
>>> calc(*nums)
14
```
*nums表示把nums这个list的所有元素作为可变参数传进去。这种写法相当有用，而且很常见。
#### 关键字参数
可变参数允许你传入0个或任意个参数，这些可变参数在函数调用时自动组装为一个tuple。而关键字参数允许你传入0个或任意个含参数名的参数，这些关键字参数在函数内部自动组装为一个dict。
```python
def person(name, age, **kw):
    print('name:', name, 'age:', age, 'other:', kw)
```
函数person除了必选参数name和age外，还接受关键字参数kw。在调用该函数时，可以只传入必选参数：
```bash
>>> person('Michael', 30)
name: Michael age: 30 other: {}
```
也可以传入任意个数的关键字参数：
```bash
>>> person('Bob', 35, city='Beijing')
name: Bob age: 35 other: {'city': 'Beijing'}
>>> person('Adam', 45, gender='M', job='Engineer')
name: Adam age: 45 other: {'gender': 'M', 'job': 'Engineer'}
```
关键字参数有什么用？它可以扩展函数的功能。比如，在person函数里，我们保证能接收到name和age这两个参数，但是，如果调用者愿意提供更多的参数，我们也能收到。试想你正在做一个用户注册的功能，除了用户名和年龄是必填项外，其他都是可选项，利用关键字参数来定义这个函数就能满足注册的需求。

和可变参数类似，也可以先组装出一个dict，然后，把该dict转换为关键字参数传进去：
```bash
>>> extra = {'city': 'Beijing', 'job': 'Engineer'}
>>> person('Jack', 24, city=extra['city'], job=extra['job'])
name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}
```
当然，上面复杂的调用可以用简化的写法：
```bash
>>> extra = {'city': 'Beijing', 'job': 'Engineer'}
>>> person('Jack', 24, **extra)
name: Jack age: 24 other: {'city': 'Beijing', 'job': 'Engineer'}
```
`**extra`表示把extra这个dict的所有key-value用关键字参数传入到函数的`**kw`参数，kw将获得一个dict，注意kw获得的dict是extra的一份拷贝，对kw的改动不会影响到函数外的extra。
### 递归函数
使用递归函数的优点是逻辑简单清晰，缺点是过深的调用会导致栈溢出。

f(n)=n!=1*2*3*...*(n-1)*n=(n-1)!*n=f(n-1)*n
f(n)用递归表示出来就是：
```python
def fact(n):
    if n==1:
        return 1
    return n * fact(n-1)
```
使用递归函数需要防止栈溢出。在计算机中，函数调用是通过栈(stack)这种数据结构实现的，每当进入一个函数调用，栈就会加一层栈帧，每当函数返回，栈就会减一层栈帧。由于栈的大小不是无限的，所以，递归调用的次数过多，会导致栈溢出。

解决递归调用栈溢出的方法是通过***尾递归***优化，事实上尾递归和循环的效果是一样的，所以，把循环看成是一种特殊的尾递归函数也是可以的。

尾递归是指，在函数返回的时候，调用自身本身，并且，return语句不能包含表达式。这样，编译器或者解释器就可以把尾递归做优化，使递归本身无论调用多少次，都只占用一个栈帧，不会出现栈溢出的情况。

上面的fact(n)函数由于return n * fact(n - 1)引入了乘法表达式，所以就不是尾递归了。要改成尾递归方式，需要多一点代码，主要是要把每一步的乘积传入到递归函数中：
```python
def fact(n):
    return fact_iter(n, 1)

def fact_iter(num, product):
    if num == 1:
        return product
    return fact_iter(num-1, num*product)
```
## 高级特性
### 切片
取一个list或tuple的部分元素
```bash
>>> L = ['Michael', 'Sarah', 'Tracy', 'Bob', 'Jack']
```
笨方法：
```bash
>>> [L[0], L[1], L[2]]
['Michael', 'Sarah', 'Tracy']
```
切片，从0开始，不包括3
```bash
>>> L[0:3]
['Michael', 'Sarah', 'Tracy']
```
每五个取一个
```bash
>>> L[::5]
```
### 迭代
如果给定一个list或tuple，我们可以通过`for`循环来遍历这个list或tuple，这种遍历我们称为迭代（Iteration）。

当使用for循环时，只要作用于一个可迭代对象，for循环就可以正常运行。
### 迭代生成器
### 生成器
### 迭代器
## 函数式编程
### 高阶函数
#### map/reduce
`map()`接收两个参数，一个是函数，一个是iterable。map将传入函数依次作用到序列的每个元素。
```bash
>>> def f(x):
...     return x * x
...
>>> r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
>>> list(r)
[1, 4, 9, 16, 25, 36, 49, 64, 81]
```
`reduce()`把一个函数作用在一个序列上，累积运算。
```bash
>>> from functools import reduce
>>> def add(x, y):
...     return x + y
...
>>> reduce(add, [1, 3, 5, 7, 9])
25
```
#### filter
`filter()`函数用于过滤序列，把传入的函数依次作用于序列的每个元素，由返回值是`True`还是`False`决定保留还是丢弃该元素。
```python
def is_odd(n):
    return n % 2 == 1

list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))
# 结果: [1, 5, 9, 15]
```
#### sorted
排序算法
### 返回函数
函数作为返回值
### 匿名函数
### 装饰器
`decorator`\
函数对象有一个`__name__`属性，可以拿到函数名字
```bash
>>> now.__name__
'now'
>>> f.__name__
'now'
```
### 偏函数
`int()`函数提供额外的`base`参数，默认为10。
```bash
>>> int('12345', base=8)
5349
>>> int('12345', 16)
74565
```
`functools.partial`就是帮助我们创建一个偏函数的
```bash
>>> import functools
>>> int2 = functools.partial(int, base=2)
>>> int2('1000000')
64
>>> int2('1010101')
85
```
## 模块
创建一个hello.py文件
```python
#!/usr/bin/env python3
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'Tian shu'

import sys

def test():
    args = sys.argv
    if len(args)==1:
        print('Hello, world!')
    elif len(args)==2:
        print('Hello, %s!' % args[1])
    else:
        print('Too many arguments!')

if __name__=='__main__':
    test()
```
第1行注释可以让这个hello.py文件直接在Unix/Linux/Mac上运行\
第2行注释表示.py文件本身使用标准UTF-8编码\
第4行是一个字符串，表示模块的文档注释，任何模块代码的第一个字符串都被视为模块的文档注释；\
第6行使用`__author__`变量把作者写进去，这样当你公开源代码后别人就可以瞻仰你的大名；\
`sys`模块有一个`argv`变量，用list存储了命令行的所有参数。`argv`至少有一个元素，因为第一个参数永远是该.py文件的名称，例如：

运行python3 hello.py获得的sys.argv就是['hello.py']；

运行python3 hello.py Michael获得的sys.argv就是['hello.py', 'Michael']。

当我们在命令行运行hello模块文件时，Python解释器把一个特殊变量__name__置为__main__，而如果在其他地方导入该hello模块时，if判断将失败，因此，这种if测试可以让一个模块通过命令行运行时执行一些额外的代码，最常见的就是运行测试。
## 面向对象编程
面向对象编程——Object Oriented Programming，简称OOP，是一种程序设计思想。OOP把对象作为程序的基本单元，一个对象包含了数据和操作数据的函数。
### 类和实例
类class
```python
class Student(object):
    def __init__(self, name, score):
        self.name = name
        self.score = score
```
class后面紧接着是类名，即Student，类名通常是大写开头的单词，紧接着是(object)，表示该类是从哪个类继承下来的，继承的概念我们后面再讲，通常，如果没有合适的继承类，就使用object类，这是所有类最终都会继承的类。\
定义好了Student类，就可以根据Student类创建出Student的实例，创建实例是通过类名+()实现的\

注意到__init__方法的第一个参数永远是self，表示创建的实例本身，因此，在__init__方法内部，就可以把各种属性绑定到self，因为self就指向创建的实例本身。

有了__init__方法，在创建实例的时候，就不能传入空的参数了，必须传入与__init__方法匹配的参数，但self不需要传，Python解释器自己会把实例变量传进去
### 访问限制
在Python中，实例的变量名如果以__开头，就变成了一个私有变量（private），只有内部可以访问，外部不能访问
```python
class Student(object):

    def __init__(self, name, score):
        self.__name = name
        self.__score = score

    def print_score(self):
        print('%s: %s' % (self.__name, self.__score))
```
改完后，对于外部代码来说，没什么变动，但是已经无法从外部访问实例变量.__name和实例变量.__score了
```bash
>>> bart = Student('Bart Simpson', 59)
>>> bart.__name
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
AttributeError: 'Student' object has no attribute '__name'
```
### 继承和多态
在OOP程序设计中，当我们定义一个class的时候，可以从某个现有的class继承，新的class称为子类（Subclass），而被继承的class称为基类、父类或超类（Base class、Super class）。

对于静态语言（例如Java）来说，如果需要传入Animal类型，则传入的对象必须是Animal类型或者它的子类，否则，将无法调用run()方法。\
对于Python这样的动态语言来说，则不一定需要传入Animal类型。我们只需要保证传入的对象有一个run()方法就可以了
### 获取对象信息
首先，我们来判断对象类型，使用`type()`函数
### 实例属性和类属性
## 面向对象高级编程
### 使用__slots__
### 使用@property
### 多重继承
MixIn
### 定制类
### 使用枚举类
为这样的枚举类型定义一个class类型，然后，每个常量都是class的一个唯一实例。Python提供了Enum类来实现这个功能
```python
from enum import Enum

Month = Enum('Month', ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'))
```
### 使用元类
## 错误、调试和测试
### 错误处理
try\
[常见错误类型和继承关系](https://docs.python.org/3/library/exceptions.html#exception-hierarchy)
### 调试
assert
### 单元测试
### 文档测试
## IO编程
### 文件读写
```python
f = open('/Users/michael/test.txt', 'r')
f.read()
f.close()

with open('/Users/michael/test.txt', 'w') as f:
    f.write('Hello, world!')

with open('/path/to/file', 'r') as f:
    print(f.read())

for line in f.readlines():
    print(line.strip()) # 把末尾的'\n'删掉
```
二进制文件
```bash
>>> f = open('/Users/michael/test.jpg', 'rb')
>>> f.read()
b'\xff\xd8\xff\xe1\x00\x18Exif\x00\x00...' # 十六进制表示的字节
```
### StringIO和BytesIO
StringIO顾名思义就是在内存中读写str。\
要把str写入StringIO，我们需要先创建一个StringIO，然后，像文件一样写入即可：
```bash
>>> from io import StringIO
>>> f = StringIO()
>>> f.write('hello')
5
>>> f.write(' ')
1
>>> f.write('world!')
6
>>> print(f.getvalue())
hello world!
```
`getvalue()`方法用于获得写入后的str。\
要读取StringIO，可以用一个str初始化StringIO，然后，像读文件一样读取：
```bash
>>> from io import StringIO
>>> f = StringIO('Hello!\nHi!\nGoodbye!')
>>> while True:
...     s = f.readline()
...     if s == '':
...         break
...     print(s.strip())
...
Hello!
Hi!
Goodbye!
```
StringIO操作的只能是str，如果要操作二进制数据，就需要使用BytesIO。\
BytesIO实现了在内存中读写bytes，我们创建一个BytesIO，然后写入一些bytes
```bash
>>> from io import BytesIO
>>> f = BytesIO()
>>> f.write('中文'.encode('utf-8'))
6
>>> print(f.getvalue())
b'\xe4\xb8\xad\xe6\x96\x87'
```
### 操作文件和目录
```bash
>>> import os
>>> os.name # 操作系统类型
'posix'
```
如果是`posix`，说明系统是Linux、Unix或Mac OS X，如果是`nt`，就是Windows系统。
要获取详细的系统信息，可以调用uname()函数：
```bash
>>> os.uname()
posix.uname_result(sysname='Linux', nodename='ztc-ubuntu', release='5.14.0-1057-oem', version='#64-Ubuntu SMP Mon Jan 23 17:02:19 UTC 2023', machine='x86_64')
```
注意uname()函数在Windows上不提供，也就是说，os模块的某些函数是跟操作系统相关的

环境变量\
在操作系统中定义的环境变量，全部保存在`os.environ`这个变量中，可以直接查看\
要获取某个环境变量的值，可以调用`os.environ.get('key')`\

操作文件和目录\
操作文件和目录的函数一部分放在os模块中，一部分放在os.path模块中，这一点要注意一下。查看、创建和删除目录可以这么调用
```bash
# 查看当前目录的绝对路径:
>>> os.path.abspath('.')
'/Users/michael'
# 在某个目录下创建一个新目录，首先把新目录的完整路径表示出来:
>>> os.path.join('/Users/michael', 'testdir')
'/Users/michael/testdir'
# 然后创建一个目录:
>>> os.mkdir('/Users/michael/testdir')
# 删掉一个目录:
>>> os.rmdir('/Users/michael/testdir')
```
通过`os.path.split()`函数，这样可以把一个路径拆分为两部分，后一部分总是最后级别的目录或文件名\
`os.path.splitext()`可以直接让你得到文件扩展名\
`shutil`模块提供了`copyfile()`的函数
### 序列化
把变量从内存中变成可存储或传输的过程称之为序列化，在Python中叫`pickling`，在其他语言中也被称之为serialization，marshalling，flattening等等\
序列化之后，就可以把序列化后的内容写入磁盘，或者通过网络传输到别的机器上。\
反过来，把变量内容从序列化的对象重新读到内存里称之为反序列化，即unpickling。\
Python提供了pickle模块来实现序列化
```bash
>>> import pickle
>>> d = dict(name='Bob', age=20, score=88)
>>> pickle.dumps(d)
b'\x80\x03}q\x00(X\x03\x00\x00\x00ageq\x01K\x14X\x05\x00\x00\x00scoreq\x02KXX\x04\x00\x00\x00nameq\x03X\x03\x00\x00\x00Bobq\x04u.'
```
`pickle.dumps()`方法把任意对象序列化成一个bytes，然后，就可以把这个bytes写入文件。或者用另一个方法`pickle.dump()`直接把对象序列化后写入一个file-like Object
```bash
>>> f = open('dump.txt', 'wb')
>>> pickle.dump(d, f)
>>> f.close()
```
#### JSON
```bash
>>> import json
>>> d = dict(name='Bob', age=20, score=88)
>>> json.dumps(d)
'{"age": 20, "score": 88, "name": "Bob"}'
```
dumps()方法返回一个str，内容就是标准的JSON。类似的，dump()方法可以直接把JSON写入一个file-like Object。\
要把JSON反序列化为Python对象，用loads()或者对应的load()方法，前者把JSON的字符串反序列化，后者从file-like Object中读取字符串并反序列化：\
```bash
>>> json_str = '{"age": 20, "score": 88, "name": "Bob"}'
>>> json.loads(json_str)
{'age': 20, 'score': 88, 'name': 'Bob'}
```
由于JSON标准规定JSON编码是UTF-8，所以我们总是能正确地在Python的str与JSON的字符串之间转换









