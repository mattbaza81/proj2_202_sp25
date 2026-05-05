## 🌿 CSC 202 – Assignment 2: Linked Lists and Filtering CO₂ Emissions

### Submission

You will make your own fork of this repository and submit that public URL as your Project 2 submission.


---

### 📦 Overview

In this assignment, you’ll build a linked list of structured data rows based on real-world climate data — specifically, CO₂-equivalent emissions from around the world. You’ll practice:

- Using `@dataclass(frozen=True)` to define structured records  
- Recursively building and filtering linked lists using `Node` and `None`  
- Reading and parsing multi-line CSV files  

> ✅ **All functions in this assignment must be external functions** — do not define methods inside classes.

---

## ✅ Task 1: Define Your Linked List Structure

You will be building a custom linked list of **rows**, where each **node** holds one row from the CO₂ emissions dataset.

### 🧩 Create the following:

- A `Row` class to store one line of emissions data  
- A `Node` class, where each node has:
  - `value`: a `Row` object
  - `next`: either another `Node` or `None`  

Each row of the CSV file includes the following fields:

```plaintext
"country"
"year"
"electricity_and_heat_co2_emissions"
"electricity_and_heat_co2_emissions_per_capita"
"energy_co2_emissions"
"energy_co2_emissions_per_capita"
"total_co2_emissions_excluding_lucf"
"total_co2_emissions_excluding_lucf_per_capita"
```

You will need to convert string values into appropriate types (e.g., float or int), and use `None` for missing data (`""` in the CSV).

> You must use `@dataclass(frozen=True)` for all class definitions.  
> ❗ **Reminder**: All logic must be implemented as external functions.

---

## ✅ Task 2: Reading the CSV File

### 🔧 Write the following function:

```python
read_csv_lines(filename: str) -> Optional[Node]
```

- Uses the `csv.reader` class to load rows  
- Validates the header row  
- Converts each row into a `Row` object  
- Recursively builds and returns a linked list (`Node` → `Node` → `...` → `None`)

> 💡 We suggest writing a **helper function**:  
> `def parse_row(fields: list[str]) -> Row`  
> to handle data conversion.

> ❗ All functionality must be implemented in **external functions** — not inside any class.

Set the recursion limit at the top of your file:
```python
import sys
sys.setrecursionlimit(10_000)
```

---

## ✅ Task 3: Count Rows

### ✍️ Write:

```python
listlen(data: Optional[Node]) -> int
```

This recursively returns the number of rows in the linked list.

> ❗ Use external functions only — do not define `.length()` as a method.

---

## ✅ Task 4: General Filtering

You will build a generic recursive filter that supports multiple types of queries.

### ✍️ Write:

```python
filter_rows(
    data: Optional[Node],
    field_name: str,
    comparison: str,
    value: Union[str, float, int]
) -> Optional[Node]
```

- `field_name`: one of the CSV column names  
- `comparison`: `"less_than"`, `"greater_than"`, or `"equal"`  
- `value`: the value to compare against  

### ⚠️ Rules:
- Only `"equal"` is allowed for the `"country"` field  
- All numeric fields support `"less_than"` and `"greater_than"`  
- Missing data (i.e., `None`) should be skipped  

> ❗ Must be implemented as a standalone external function.

---

## 🧪 Task 6: Tests and Design Recipe

For each function:
- Write a **purpose statement**  
- Include **type hints**  
- Create **tests** using `unittest` in a file called `test_student.py`

You should define your own small CSV file with 5–10 rows for testing.  
Missing values (`""`) should be handled using `None`.

> ❗ No methods inside your data classes — write only **external functions**.

---

## 🔧 Setup and Restrictions

Your file should include the following at the top:

```python
from __future__ import annotations
import sys
import csv
from typing import *
from dataclasses import dataclass
import unittest
import math

sys.setrecursionlimit(10_000)
```

Do **not** import any other libraries. Your submission must be compatible with **Python 3.12.3**.

---

## 📤 Handin Instructions

Push the following files to your GitHub Classroom repo:

- `proj2.py` – your main implementation  
- `test_student.py` – your test suite  
- `sample.csv` – a small file for testing (optional but recommended)

---


## 📎 Appendix: Working with CSV Files in Python

### 🔢 What’s a CSV File?

A **CSV file** ("Comma-Separated Values") is a simple text file where:

- Each **line** is one row in a table  
- Each **value** in a line is separated by a comma (`,`)  
- The **first line** usually contains **column names**

#### 📦 Example

A CSV for a magic shop's inventory might look like:

```csv
item,price,number in stock
cauldron,47000,16
broom,7899,10
wand,1426,150
```

This means:
- The price of a broom is $78.99  
- There are 10 brooms in stock  
- Each row represents one item

---

### 🧠 Reading CSV Files in Python

Python has a built-in `csv` module that makes reading CSVs easy.  
The `csv.reader` class acts as an **iterator**, giving you one row at a time as a list of strings.

#### 🧪 Example

```python
import csv

def total_item_count(filename: str) -> int:
    with open(filename, newline="") as csvfile:
        iter = csv.reader(csvfile)
        topline = next(iter)
        if not (topline == expected_labels):
            raise ValueError("unexpected first line: got: {}".format(topline))
        item_count = 0
        for line in iter:
            item_count = item_count + float(line[2])
        return item_count
```

---

### 🧰 Code Explanation

#### 4.1 `with`
The `with` block **automatically closes** the file after you're done — this is safer and cleaner than using `open()` without it.

#### 4.2 `iter`
The CSV reader is an **iterator**. That means:
- It returns the next line every time you loop over it
- You don’t get all lines at once — just one at a time
- This works great with `for line in iter: ...`

In this assignment, you’ll use this to **build a linked list**, where each row becomes a node.

> ⚠️ Your list might come out "backward" (most recent row first). That’s fine!

#### 4.3 `raise`
If the CSV is missing its header or in the wrong format, we use `raise ValueError(...)` to halt the program and print a helpful message.

#### 4.4 `format`
Python lets you insert values into strings:

```python
print("Adding {} and {} gives {}".format(3, 4, 7))
```

This prints: `Adding 3 and 4 gives 7`.

---

### 🌍 About Your Input Data

We’ve extracted a subset of real climate data from **Our World in Data**.

This dataset contains:
- Greenhouse gas emissions by country
- Year-by-year data from 1990 to 2020
- Three sectors:  
  - `"electricity and heat"`  
  - `"energy"`  
  - `"total CO2 excluding LUCF"` (Land Use Change and Forestry)

Each sector has:
- **Total emissions**
- **Per-capita emissions**

#### ⚠️ Missing data
Some rows are incomplete! For example:

```csv
Andorra,2010,,,,,,,
```

If a value is missing, the CSV line will just have empty fields (like `,,,,`), which appear as empty strings (`""`). You must convert these to `None`.

