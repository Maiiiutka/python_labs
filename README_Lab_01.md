# python_labs

## Lab_01

### Задания

**Задание 1** — Привет и возраст
    Файл: src/01_greeting.py
    Ввод: имя (строка), возраст (целое).
    Вывод: Привет, <имя>! Через год тебе будет <возраст+1>.

Пример:

Имя: Алиса
Возраст: 19
Привет, Алиса! Через год тебе будет 20.

*Code*

```
name = input("Имя: ")
age = int(input("Возраст: "))

#Вводим имя и возраст#

next_year_age = age + 1

print(f"Привет, {name}! Через год тебе будет {next_year_age}.")
```

*Screen*

<img width="904" height="435" alt="01_greeting" src="https://github.com/user-attachments/assets/f51d371a-6d54-4a61-bff9-84bf7618e808" />

**Задание 2** — Сумма и среднее
Файл: src/02_sum_avg.py
Ввод: два числа (вещественные), допускаются точка или запятая.
Вывод: sum=<...>; avg=<...> — значения печатать с 2 знаками.

Пример:

a: 3,5
b: 4.25
sum=7.75; avg=3.88

*Code*

```
a = float(input("a: "))
b = float(input("b: "))
sum = a+b
avg = sum / 2
print(f"sum={sum};avg={avg}")
```

*Screen*

<img width="918" height="443" alt="02_sum_avg" src="https://github.com/user-attachments/assets/62dc0252-021c-4739-aa37-16c2ca31f5da" />

**Задание 3** — Чек: скидка и НДС
Файл: src/03_discount_vat.py
Ввод: price (₽), discount (%), vat (%) — вещественные.
Формулы:
base = price * (1 - discount/100)
vat_amount = base * (vat/100)
total = base + vat_amount
Вывод: по строкам, 2 знака после запятой.

База после скидки: 900.00 ₽
НДС:               180.00 ₽
Итого к оплате:    1080.00 ₽
(пример входных: price=1000, discount=10, vat=20)

*Code*

```
price = float(input("price (₽): "))
discount = float(input("discount (%): "))
vat = float(input("vat (%): "))

base = price * (1 - discount/100)
vat_amount = base * (vat/100)
total = base + vat_amount

print(f"База после скидки: {base:.2f} ₽")
print(f"НДС:               {vat_amount:.2f} ₽")
print(f"Итого к оплате:    {total:.2f} ₽")
```

*Screen*

<img width="918" height="448" alt="03_discount_vat" src="https://github.com/user-attachments/assets/485825ee-0c66-4917-b561-cbaec007be6b" />

**Задание 4** — Минуты → ЧЧ:ММ
Файл: src/04_minutes_to_hhmm.py
Ввод: m — целые минуты.
Вывод: ЧЧ:ММ минуты вывести как {min:02d}.

Пример:

Минуты: 135
2:15

*Code*

```
m = int(input("min:"))
h = m // 60
rm = m % 60
print(f"{h}:{rm:02d}")
```

*Screen*

<img width="709" height="437" alt="04_minutes_to_hhmm" src="https://github.com/user-attachments/assets/0902d699-d0ad-4653-97e5-7ad39eab9113" />

**Задание 5** — Инициалы и длина строки
Файл: src/05_initials_and_len.py
Ввод: ФИО одной строкой (могут быть лишние пробелы).
Вывод: инициалы (верхний регистр) и длина исходной строки без лишних пробелов.

Пример:

ФИО:   Иванов   Иван   Иванович  
Инициалы: ИИИ.
Длина (символов): 20

*Code*

```
full_name = input("ФИО: ")
cleaned_name = ' '.join(full_name.split())
words = cleaned_name.split()
initials = ''.join(word[0].upper() for word in words)
print(f"Инициалы: {initials}.")
print(f"Длина (символов): {len(cleaned_name)}")
```

*Screen*

<img width="663" height="402" alt="05_initials_and_len" src="https://github.com/user-attachments/assets/1dc30c56-6398-4659-87c7-8e64c319369e" />

**Задание 6**
На лабораторную работу по проге согласилось прийти много людей. Помогите сосчитать всех участников.

На вход подаётся число N, после которой идёт N строк, каждая формата

Фамилия Имя Возраст Формат_участия
Фамилия и Имя представляют из себя строки, когда Возраст представляет из себя целое число. Формат_участия представляются в виде булевой переменной, где True означает очный формат обучения, а False - заочный. Вам необходимо посчитать, сколько человек записалось на очный формат и сколько на заочный и вывести два числа через пробел. Пример:

in_1: 1337
in_2: Максимов Максим 18 True
in_3: Геннадьев Геннадий 17 False
in_4: Алексеев Алексей 17 True
out: 2 1

*Code*

```
N = int(input())
m = []
for i in range(N):
    m.append(input())
k1 = 0
k2 = 0
for i in range(len(m)):
    if m[i].count("True") > 0:
        k1 += 1
    elif m[i].count("False") > 0:
        k2 += 1
print(k1,k2)
```

*Screen*

<img width="735" height="402" alt="06_sem" src="https://github.com/user-attachments/assets/e65ffd8e-fd4f-44e5-8618-f284dfc57d0e" />

**Задание 7**

При подготовке к лекции кто-то зашифровал все мои материалы. Помогите вернуть исходники.

На вход подаётся строка, состоящая из различных символов без пробелов. Известно, что можно восстановить данные следующим алгоритмом:

Первая заглавная буква в строке является первой буквой в оригинальной строке;
Символы оригинальной строки расположены в фиксированном шаге друг от друга;
Второй символ стоит сразу после цифры;
Последним символом оригинальной строки является точка .
Напишите алгоритм, по которому можно восстановить оригинальную строку. Пример:

in: thisisabracadabraHt1eadljjl12ojh.
out: Hello.

*Code*

```
cif = "0123456789"
buk = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
spec = "."
shifr = str(input())
shifr = list(shifr)
fin = ""
k = 0
s = True
first = 0 
second = 0 
stop = False

for i in range (len(shifr)):
    ind = i 
    if shifr[ind] in buk:
        fin += shifr[ind]
        first = i
    if shifr[i] in cif and s == True:
        fin += shifr[i+1]
        s = False 
        second = i + 1
    shag = second - first  
    ostalos = len(shifr[:second])
    if shag > 0 and ostalos != len(shifr):
        for j in range(ostalos+shag,len(shifr),shag):
            fin += shifr[j]
            if shifr[j] == ".":
                stop = True
    if stop == True:
        break
print(fin)
```

*Screen*

<img width="786" height="465" alt="07_code" src="https://github.com/user-attachments/assets/8a7d8313-d55c-416b-9b9c-624bc84a8acc" />

**Вывод:** В процессе лабораторной работы я изучила базовые принципы программирования на языке Python. Освоила работу с пользовательским вводом, выполнение математических операций, обработку текстовых данных и форматирование вывода. Также я научилась использовать GitHub для управления версиями кода и ведения проектов.
