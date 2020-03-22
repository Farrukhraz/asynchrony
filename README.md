# asynchrony

Thanks a bunch for [Molchanov tutors](https://www.youtube.com/playlist?list=PLlWXhlUMyooawilqK4lPXRvxtbYiw34S8)!
### 4_Generators

__Генератор__ - это функция.
   

> ### Пример с перебором букв в слове

```
>>> def gen(name):
        for i in name:
            yield i
        
>>> g = gen('Bob')
>>> next(g)
B
>>> next(g)
o
>>> next(g)
b
>>> next(g)
Error ... StopIteration
```
Как только генератор "истощается/заканчивается" он выбрасывает ошибку.  
     
> ### Пример с созданием папок

```
>>> from time import time

>>> def gen_file_name():
        while True:
            pattern = 'file-{}.jpg'
            t = int(time() * 1000)
            file_name = pattern.format(str(t))
            yield file_name

>>> g = gen_file_name()
>>> next(g)
file-1584695786887.jpg
>>> next(g)
file-1584695786759.jpg
```
В этом примере генератор не закончиться потому, что внутри него крутиться бесконечный цикл _while True_.  
     
> ### Инструкции yield в одной функции-генераторе может быть несколько.

В то время как у _функции_ весь код, который идет после _**return**_ не выполняется. У _генератора_ всё совсем ___не так___.
```
>>> def gen_file_name():
        while True:
            pattern = 'file-{}.jpg'
            t = int(time() * 1000)
            file_name = pattern.format(str(t))
            yield file_name                     # точка остановки

            sum = 123 + 321
            print(sum)
        
>>> g = gen_file_name()
>>> next(g)
file-1584695786887.jpg
>>> next(g)
444                                     # вот это важный момент
file-1584695786759.jpg
```
Т.е. что получается? При вызове функции next(), генератор отрабатывает до yield (точка остановки) и засыпает. 
После повторного вызова функции next(), оставщаяся часть генератора выполняется, т.е. печатает нам сумму и 
начинается новая итерация цикла.  
   
В одной функции-генераторе может быть сколь угодно ___yield___.
```
def some_yields():
    n = 10
    while True:
        yield n
        yield (n // 10)
        yield (n / 2)
        n += 10

>>> g = some_yields()
>>> next(g)
10
>>> next(g)
1
>>> next(g)
5.0
>>> next(g)             # Вышли из 1-ой итерации цикла и поехали по новой
20
>>> next(g)
2
>>> next(g)
10.0
.
.
.
```
     
     
### Событийный цикл _Round Robin_

Мы построили бассейн и в нём нету воды, в то время как у наших соседей в бассейне есть вода. Мы собрали всех друзей, дали каждому
по ведру и построили их в очередь. Первый в очереди зачерпывает воду в ведро, несёт воду к нам в бассейн, вылевает её и встаёт в 
конец очереди. Тот кто был вторым в очереди, становится первым и проделывает тоже самое. И цикличность продолжается пока работа не 
будет выполнена. Вот это и есть _Round Robin, карусель._ 

```
>>> from collections import deque

>>> def gen1(n):
        for i in range(n):
            yield print(i)

>>> def gen2(string):
        for el in string:
            yield print(el)

>>> g1 = gen1(3)
>>> g2 = gen2('Bob')

>>> tasks = deque([g1, g2])                 # deque; Создание новой очереди

>>> while tasks:
        try:
            task = tasks.popleft()
            next(task)
            tasks.append(task)
        except StopIteration:
            pass

0
B
1
o
2
b
```
Суть в том что генераторы выполнялись строго по очереди, каждый раз передавая конкроль туда где вызывалась функция _next_.
После каждого полученного результата мы получили контроль обратно и в этот момент мы могли сделать, что то ещё.
     
     
### Корутины
     
___Корутины___ - это по сути генираторы, которые во время своей работы могут принимать из-вне какие либо данные. Делается это при помощи метода __send()__
```
from inspect import getgeneratorstate

def gen():
    send_msg = "Hello from generator"
    while True:
        # yield send_msg                # вернёт нам это. И продолжит испольнение
        get_msg = yield print(send_msg) # тут программа приостановится, до тех пор пока не будет вызвана из вне, методом send() или функцией next()
        print("Got this msg:", get_msg) # переданное методом send('smth') присваевается get_msg, и далее принтуется

>>> g = gen()                           # создаём объект гениратор
>>> print(getgeneratorstate(g))         # проверяем статус гениратора 
GEN_CREATED                             # генератор создан
>>> g.send(None)                        # метод send() с аргументом None "активирует" генератор. Также можно сделать ф-цей next() с >>> аргументом g
Hello from generator                    # так как он активирован. Он выполнил команды и остановился на get_msg
>>> print(getgeneratorstate(g))         # проверяем статус гениратора; 
GEN_SUSPENDED                           # генератор преостановлен
>>> g.send("Outside")                   # посылаем строку генератору
Got this msg: Outside                   # генератор получит данные из-вне и продолжил своё исполнение до следующего get_msg = yield ...
Hello from generator
>>> next(g)                             # просим генератор совершить ищё одну итерацию
Got this msg: None                      # вернул None, потому что нечего не было переданно ему
Hello from generator
```
     
    
Кроме данных в корутину можно ___послать "заглушку" (исключение)___, чтобы прервать цикл. Также можно передать
исключение созданное самостоятельно.   
    
Создадим _своё исключение_:
```
class MyException(Exception):
    pass
```
       
Считаем среднее арифметическое преданных чисел:
```
>>> def gen():
        sum = 0
        count = 0
        average = None          # None для того чтобы "x = yield average" при первом вызове нечего не возвращал
        while True:
            try:
                num = yield average
            except StopIteration:
                print("couritine stopped!")
            except MyException:
                print("Stopped by your exception!")
            else:
                sum += num
                count += 1
                average = round(sum / count, 2)

>>> g = gen()
>>> g.send(None)
>>> g.send(10)
10.0
>>> g.send(8)
9.0
>>> g.send(20)
12.67
>>> g.throw(MyException)                # Сюда можно кинуть любое (созданное/существующее) исключение
Stopped by your exception!
12.67
```
     
    
Чтобы каждый раз не инициализировать (g.send(None)) гениратор-корутину. Можно создать обёртку для него, т.е. _декоратор_.
   
```
>>> def coroutine(func):
        def inner(*args, **kwargs):
            g = func(*args, **kwargs)
            g.send(None)
            return g
        return inner

>>> @coroutine
>>> def gen():
        sum = 0
        count = 0
        average = None          # None для того чтобы "x = yield average" при первом вызове нечего не возвращал
        while True:
            try:
                num = yield average
            except StopIteration:
                print("couritine stopped!")
            except MyException:
                print("Stopped by your exception!")
            else:
                sum += num
                count += 1
                average = round(sum / count, 2)

>>> g = gen()
# g.send(None)         # это больше не нужно!
>>> g.send(10)
10.0
.
.
.
```




