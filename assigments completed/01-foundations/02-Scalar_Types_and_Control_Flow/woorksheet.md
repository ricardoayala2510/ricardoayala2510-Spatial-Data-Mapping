# Worksheet: 03 - Scalar Types and Control Flow

Use this worksheet to reinforce your understanding of variables, comparisons, and decision logic.

## 🧠 Section 1: Scalar Types

### 1. What is the output of the following code?

```python
x = 10
print(type(x))
```

**Answer:** `<class 'int'>`

### 2. What scalar type would best represent:

- **A person's name:** `str`
- **Their age:** `int`
- **Whether they passed a test:** `bool`

## ✏️ Task: Type Practice

```python
# Create a variable for each type and print its value and type

my_int = 25
my_float = 3.5
my_str = "Alisson"
my_bool = True

print(my_int, type(my_int))
print(my_float, type(my_float))
print(my_str, type(my_str))
print(my_bool, type(my_bool))
```

---

## 🔁 Section 2: Comparison Operators

### 3. What does the `!=` operator mean?

**Answer:** It means **not equal to**.

### 4. What will the following code print?

```python
a = 5
b = 3
print(a < b or b < 10)
```

**Answer:** `True`

Explanation: `a < b` is `False`, but `b < 10` is `True`, and with `or`, only one part needs to be true.

---

## 🔀 Section 3: Control Flow

### 5. Write a conditional that prints `"Pass"` if a grade is `>= 70`, and `"Fail"` otherwise.

```python
grade = 75

if grade >= 70:
    print("Pass")
else:
    print("Fail")
```

### 6. What does `elif` allow you to do?

**Answer:** `elif` lets you check another condition after an `if` statement if the first condition is false.

---

## ✏️ Task: Your Turn

Write a program that asks for the weather and prints:

- `"Bring sunscreen"` if it's sunny
- `"Take an umbrella"` if it's raining
- `"Check the forecast"` otherwise

```python
weather = input("What is the weather? ")

if weather == "sunny":
    print("Bring sunscreen")
elif weather == "raining":
    print("Take an umbrella")
else:
    print("Check the forecast")
```
