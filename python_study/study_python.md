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