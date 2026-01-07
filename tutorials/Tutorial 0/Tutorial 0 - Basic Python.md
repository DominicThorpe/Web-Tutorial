# Tutorial 1.1: Basic Coding Concepts

Python is a general-purpose programming language, which means we can use it for almost anything. It is designed to be easy to learn and use, and be quick to write code in so we can create prototypes quickly.

## Variables and Data Types

Data in python can be one of many datatypes:
 - Integers: 1, 2, or -3
 - Floats: 1.1, 15.7, -2.4
 - Booleans: `True` or `False`
 - Strings: "Hello world" or "Dom Thorpe"

We can assign data to variables and see what they contain like this:
```python
my_string = "Hello!"
print("I say " + my_string)
```

We can assign input like this:
```python
number = int(input("Guess a number: "))
```

Here `int` is used to convert the string output of `input()` to an integer.

## Basic Operations

The basic operations in python are:
 - `+`, `-`, `*`, `/` which represent addition, subtraction, multiplication, and division
 - `>`, `<`, `>=`, `<=` which represent greater than, less than, greater or equal, and less or equal
 - `==` and `!=` which represent equality and inequality
 - `and`, `or`, and `not` which are used in boolean expressions 

Find out what happens when we do:
```python
a = 15
b = 10
c = 5

print(a + b + c)
print(a == b)
print(a - c == b)
```

## If-Else Statements

Try running this code and see what happens:

```python
number = int(input("Enter a number: "))
correct = 25
if (number > correct):
    print("Too high!")
elif (number < correct):
    print("Too low!")
else:
    print("Correct!")
```

See how we can use *if, elif, else* to make decisions based on our code. You have have as many `elif` clauses as you like, and `elif` and `else` are both optional. 

## Repeating Code With Loops

### For Loops

For loops are used when you know how many times you want to repeat something, or if you want to iterate over a list.

```python
for i in range(0, 10):
    print(i)
```

```python
for name in ["Dom", "Tim", "Kat", "Jeff", "Alice"]:
    print("Name: " + name)
```

### While Loops

While loops are used when you want the loop to continue until a condition is met:

```python
number = -1
correct = 25
while (number != correct):
    number = int(input("Enter a number: "))
    if (number > correct):
        print("Too high!")
    elif (number < correct):
        print("Too low!")

print("Correct!")
```

## Lists and Dictionaries

### Lists

Lists are used to store collections of values:

```python
my_names = ["Alice", "Bob", "Carrie", "Dan", "Ellie"]
my_matrix = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
my_mix = ["Hello", 23, True]
```

We access values in lists using 0-indexing, which means that the first item in a list is the 0th, not the 1st:

```python
numbers = [1, 4, 9, 16, 25, 36]
first_item = numbers[0]
second_item = numbers[1]
last_item = numbers[-1]
```

We can access the length of a list with the `len()` function, and append items to a list with `<list>.append(<item>)`
```python
length = len(numbers)
print(length) # prints 6

numbers.append(49)
print(len(numbers)) # prints 7
```

### Dictionaries

Dictionaries are used to store pairs of *keys* and *values* so you can access the value when you know a key:
```python
person = {
    "name": "Dominic",
    "age": 22,
    "hair colour": "brown",
    "alive": True
}

name = person["name"]
print(name)
```

## Functions

A function is a unit of reusable code we can use to avoid repetition and keep things organised and readable:

```python
def greet(name):
    print(f"Hello {name}")

greet("Sam")
greet("Beth")
```

As we can see, programs have parameters which make them more versatile.

## Classes and Attributes

A class is a blueprint for creating *objects* which group together functions and variables.

```python
class Field:
    name = "North Field"
    area = 3.2

field = Field()
print(field.name)
print(field.area)
```

A method is a function inside a class which can use the data inside the object. There is a special method `__init__(self)` which describes what to do when an object is created from a class and may take arguments which are used when the object is created from the class:

```python
class Field:
    crop = "Wheat"

    def __init__(self, name, area):
        self.name = name
        self.area = area

    def describe(self):
        print(f"{self.name} is {self.area} hectares and contains {self.crop}!")

# arguments passed to the __init__ function
field = Field("Main Field", 5.1)
field.describe()
```

`self` refers to the object the method is inside of.
