# Worksheet: 02 - Working with Data (Answers)

Use this worksheet to review and reinforce your understanding of Python data containers.

---

## 🧠 Section 1: Lists

**1) What method adds an item to the end of a list?**  
Answer: `append()`

**2) How can you remove an item from a list by value?**  
Answer: Use `remove(value)` (example: `my_list.remove("apple")`)

**3) What’s the result of this code?**

```python
nums = [2, 4, 6]
nums.append(8)
print(nums)
```

Answer: `[2, 4, 6, 8]`

---

## ✏️ Task: List Practice

```python
# Create a list of your top 3 favorite foods.
foods = ["pizza", "sushi", "tacos"]

# Add another food to the list.
foods.append("pasta")

# Remove one item and print the list.
foods.remove("sushi")
print(foods)
```

Example output:

```text
['pizza', 'tacos', 'pasta']
```

---

## 🔒 Section 2: Tuples

**1) What is a key difference between a list and a tuple?**  
Answer: Lists are **mutable** (you can change them), while tuples are **immutable** (you can’t change them after creation).

**2) Can you change the contents of a tuple once it is created? Why or why not?**  
Answer: No. A tuple is immutable, meaning its items cannot be reassigned, added, or removed after it’s created.

---

## ✏️ Task: Tuple Practice

```python
# Create a tuple with your favorite 3 numbers.
nums = (7, 13, 21)

# Unpack it into three variables and print each.
a, b, c = nums
print(a)
print(b)
print(c)
```

Example output:

```text
7
13
21
```

---

## 🔑 Section 3: Dictionaries

**1) What does the .get() method do differently from accessing a key directly?**  
Answer: `.get(key)` returns `None` (or a default you provide) if the key doesn’t exist, instead of throwing a `KeyError`.  
Example:
```python
d = {"a": 1}
print(d.get("b"))          # None
print(d.get("b", 0))       # 0
# print(d["b"])            # KeyError
```

**2) How do you loop through both keys and values in a dictionary?**  
Answer: Use `.items()`:
```python
for key, value in my_dict.items():
    print(key, value)
```

---

## ✏️ Task: Dictionary Practice

```python
# Create a dictionary with keys: 'name', 'age', and 'hobby'.
person = {
    "name": "Ricardo",
    "age": 21,
    "hobby": "Soccer"
}

# Print each key and value in the format "key: value".
for key, value in person.items():
    print(f"{key}: {value}")
```

Example output:

```text
name: Ricardo
age: 21
hobby: Soccer
```

---

## 🧾 Submit Checklist

- [x] I practiced creating and modifying lists.  
- [x] I understand how tuples are different from lists.  
- [x] I accessed and looped through dictionary items.  
