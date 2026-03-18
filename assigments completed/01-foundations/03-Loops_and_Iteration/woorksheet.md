# Worksheet: 04 - Loops and Iteration

Practice and reflect on how loops work in Python.

## 🔁 Section 1: For Loops

### 1. What does `range(5)` produce?

**Answer:** It produces the numbers `0, 1, 2, 3, 4`.

### 2. Write a `for` loop that prints numbers 1 to 10, but skips 5.

```python
for i in range(1, 11):
    if i == 5:
        continue
    print(i)
```

---

## 🔁 Section 2: While Loops

### 3. What’s the difference between a `for` loop and a `while` loop?

**Answer:**  
A `for` loop is usually used when you want to loop over a sequence or a known range of values.  
A `while` loop is used when you want to keep looping as long as a condition stays true.

### 4. What happens if a `while` loop's condition never becomes `False`?

**Answer:** It creates an infinite loop.

### ✏️ Task: Countdown with `while`

```python
count = 5
while count >= 1:
    print(count)
    count -= 1
```

---

## 📁 Section 3: File Reading and `with`

### 5. What does the `with` statement do when opening a file?

**Answer:** It opens the file and automatically closes it when the block is done.

### 6. How do you loop over each line in a file?

**Answer:**

```python
with open("data.txt", "r") as file:
    for line in file:
        print(line)
```

### ✏️ Task: File Filter

Write code that prints only the lines in a file that contain the word `"error"`.

```python
with open("data.txt", "r") as file:
    for line in file:
        if "error" in line:
            print(line.strip())
```
