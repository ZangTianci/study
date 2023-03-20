## 进程和线程
多任务\
线程是最小的执行单元，而进程由至少一个线程组成。
### 多进程
Linux操作系统提供了一个`fork()`系统调用，子进程返回0，父进程返回子进程的ID。\
调用`getpid()`可以拿到进程的ID。\
调用`getppid()`可以拿到父进程的ID。\
python的`os`模块封装了常见的系统调用，其中包括`fork()`。\
```python
import os

print('Process (%s) start...' % os.getpid())
# Only works on Unix/Linux/Mac:
pid = os.fork()
if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
```
window没有`fork`调用
#### multiprocessing
`multiprocessing`模块是跨平台版本的多进程模块。
```python
from multiprocessing import Process
import os

def run_proc(name):
    print("run child process %s(%s)"%(name, os.getpid()))

if __name__ == '__main__':
    print("parent process %s" % os.getpgid())
    p = Process(target=run_proc, args=("test", ))
    print("child process will start")
    p.start()
    p.join()
    print("child process end")
```
执行结果如下
```bash
parent process 500984
child process will start
run child process test(501006)
child process end
```
创建子进程时候，只需要传入一个执行函数和函数的参数\
创建一个process实例，用`start()`方法启动\
`join()`方法可以等待子进程结束后继续，通常用于进程间同步
#### Pool
对Pool对象调用`join()`方法会等待所有子进程执行完毕，调用`join()`之前必须先调用`close()`，调用`close()`之后就不能继续添加新的Process了。
#### 子进程
#### 进程间通信
`Queue()`
### 多线程
`_thread`和`threading`\
启动一个线程就是把一个函数传入并创建Thread实例，然后调用`start()`开始执行\
任何进程默认启动一个线程，该线程就是主线程，主线程又可以启动新的线程，Python的threading模块有个`current_thread()`函数，它永远返回当前线程的实例。主线程实例的名字叫`MainThread`，子线程的名字在创建时指定
#### Lock
锁只有一个，无论多少线程，同一时刻最多只有一个线程持有该锁，所以，不会造成修改的冲突。创建一个锁就是通过threading.Lock()来实现\
### ThreadLocal
### 进程vs线程
### 分布式进程
## 正则表达式
## 网络编程
互联网协议包含了上百种协议标准，但是最重要的两个协议是TCP和IP协议，所以，大家把互联网的协议简称TCP/IP协议。\
IP协议负责把数据从一台计算机通过网络发送到另一台计算机。数据被分割成一小块一小块，然后通过IP包发送出去。由于互联网链路复杂，两台计算机之间经常有多条线路，因此，路由器就负责决定如何把一个IP包转发出去。IP包的特点是按块发送，途径多个路由，但不保证能到达，也不保证顺序到达。\
TCP协议则是建立在IP协议之上的。TCP协议负责在两台计算机之间建立可靠连接，保证数据包按顺序到达。TCP协议会通过握手建立连接，然后，对每个IP包编号，确保对方按顺序收到，如果包丢掉了，就自动重发。
### TCP编程
Socket是网络编程的一个抽象概念。通常我们用一个Socket表示“打开了一个网络链接”，而打开一个Socket需要知道目标计算机的IP地址和端口号，再指定协议类型即可。\
### UDP编程
