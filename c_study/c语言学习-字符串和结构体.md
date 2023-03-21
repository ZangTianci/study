## 字符串
是数组，结尾多一个`"\0"`，是字符串的结束标志
```c
char ch[] = "helo";
char *pchar = "helo";
```
`sizeof`和`strlen`区别
```c
char cdaat[128] = "hello";
sizeof(cdaat);// 128
strlen(cdaat);// 5
```
### 动态开辟字符串
`malloc`分配所需的内存空间，并返回一个指向它的指针
```c
void *malloc(size_t size)
```
## 结构体
```c
struct Student
{
    char name;
    int age;
}

int main(){

    struct Student stu1;
    // 结构体指针
    struct Student *ps = &stu1;
    stu1.age = 21;
    ps->age = 22;
}
```
### 联合体
`union`
### 枚举
`enum`
### typedef

