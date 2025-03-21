# Advanced Algorithms Coursework - README

## Design and Justification for Tasks 1.1 – 1.4

### Task 1.1: Degree Calculation
#### **Design Choices**
**Data Structure:**
- **Dictionary (HashMap):** Used to store student IDs and their corresponding module marks, providing **O(1) lookup time** for retrieving data.
- **Pandas DataFrame:** Used for reading, processing, and analyzing large CSV files efficiently.

#### **Algorithm Logic**
1. Read `task1_1_marks.csv` and `cs_modules.csv` into Pandas DataFrames.
2. Handle potential column naming inconsistencies.
3. Merge datasets to associate module names with their respective marks.
4. Calculate degree classification based on predefined thresholds.
5. Output the processed results.

#### **Justification**
- **Effectiveness:** Ensures each student’s grades are mapped correctly to their degree classification.
- **Efficiency:** Uses vectorized Pandas operations instead of loops, making processing **O(n)** instead of **O(n²)**.
- **Memory Usage:** Optimized for large datasets using Pandas’ efficient memory management.

---

### Task 1.2: Password Generator
#### **Design Choices**
**Data Structure:**
- **List:** Stores all valid password combinations.
- **Set:** Used to check uniqueness efficiently.

#### **Algorithm Logic**
1. Generate all possible password combinations using `itertools.product()`.
2. Apply validation rules:
   - Must contain **at least one uppercase letter, lowercase letter, number, and special symbol**.
   - Must **start with a letter**.
   - Cannot contain **more than two capital letters or more than two special characters**.
3. Shuffle results before saving to **prevent deterministic outputs**.
4. Save passwords to a file.

#### **Justification**
- **Effectiveness:** Ensures all passwords meet the constraints.
- **Efficiency:** `itertools.product()` is optimized for generating permutations, reducing redundant computations.
- **Memory Usage:**
  - The use of `itertools` minimizes memory overhead compared to naive nested loops.
  - Writing to a file prevents excessive RAM usage.

---

### Task 1.3: Train Ticket Search
#### **Design Choices**
**Data Structure:**
- **Graph (Adjacency List - Dictionary of Lists):** Used to represent train stations and connections efficiently.
- **Dictionary (for station name corrections):** Implements a simple **Levenshtein distance function** to suggest correct station names.

#### **Algorithm Logic**
1. Parse input stations and check for corrections.
2. Represent the network as a **bidirectional graph**.
3. Use **Dijkstra’s algorithm** to find the **shortest path**.
4. Handle errors like **missing routes and invalid inputs**.
5. Offer enhancements like **alternative routes, exporting results, and round-trip searches**.

#### **Justification**
- **Effectiveness:**
  - Ensures **correct route calculation**.
  - Provides **user-friendly corrections** and alternative suggestions.
- **Efficiency:**
  - **Dijkstra’s algorithm** runs in **O((V + E) log V)** using a priority queue.
  - Graph adjacency list storage is **space-efficient**.
- **Memory Usage:** The adjacency list representation minimizes memory use compared to an adjacency matrix.

---

### Task 1.4: Parallel Image Processing
#### **Design Choices**
**Data Structure:**
- **List:** Stores image filenames for comparison.
- **Multiprocessing Pool:** Distributes work across **multiple CPU cores**.

#### **Algorithm Logic**
1. Read all image files into a list.
2. In **serial processing**, loop through images **one by one**.
3. In **parallel processing**, use `multiprocessing.Pool()` to distribute tasks **across 4 CPU cores**.
4. Compare each image with a **reference image**.
5. Return the **best match**.

#### **Justification**
- **Effectiveness:**
  - The approach is **scalable** for large datasets.
  - The correct match is **identified with high accuracy**.
- **Efficiency:**
  - **Serial execution takes 11.04 seconds**.
  - **Parallel execution reduces time to 3.95 seconds**, achieving a **2.8x speedup**.
- **Memory Usage:**
  - **Multiprocessing avoids GIL limitations** and **maximizes CPU usage**.

---

## **Conclusion**
This mini-report summarizes the **design and efficiency considerations** for **Tasks 1.1 – 1.4**. Each task is optimized in terms of:
- **Correctness**
- **Computational efficiency**
- **Memory usage**
- **Scalability**

All external sources (e.g., **Python libraries like Pandas, itertools, and multiprocessing**) are properly cited in the implementation.  
Additional enhancements like **alternative routes (Task 1.3) and random shuffling (Task 1.2)** ensure a robust and user-friendly system.

---
📌 **Prepared for Advanced Algorithms Coursework - UWE Bristol**  
🚀 **Efficient, Scalable, and Optimized Solutions!**  
