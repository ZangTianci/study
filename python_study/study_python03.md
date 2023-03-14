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
### ThreadLocal
### 进程vs线程
### 分布式进程
