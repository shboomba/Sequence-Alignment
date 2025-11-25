# CSCI 570 Fall 2025 - Final Project
# Sequence Alignment: Basic vs Memory-Efficient Algorithm

---

## 1. Performance Results - Datapoints Output Table

| File | Problem Size (m+n) | Basic Cost | Basic Time (ms) | Basic Memory (KB) | Efficient Cost | Efficient Time (ms) | Efficient Memory (KB) |
|------|-------------------|------------|-----------------|-------------------|----------------|---------------------|----------------------|
| in1.txt | 14 | 168 | 0.0 | 27,680 | 168 | 0.0 | 28,068 |
| in2.txt | 48 | 960 | 0.0 | 27,712 | 960 | 0.0 | 27,932 |
| in3.txt | 90 | 1,848 | 4.78 | 27,972 | 1,848 | 3.73 | 27,848 |
| in4.txt | 233 | 5,760 | 13.66 | 28,580 | 5,760 | 17.26 | 28,020 |
| in5.txt | 320 | 7,680 | 29.26 | 29,576 | 7,680 | 168.30 | 28,044 |
| in6.txt | 337 | 5,244 | 54.68 | 30,004 | 5,244 | 66.74 | 27,888 |
| in7.txt | 465 | 7,728 | 144.96 | 31,876 | 7,728 | 180.29 | 28,060 |
| in8.txt | 648 | 11,136 | 231.24 | 33,452 | 11,136 | 323.52 | 28,128 |
| in9.txt | 909 | 19,116 | 323.23 | 36,512 | 19,116 | 532.70 | 27,964 |
| in10.txt | 1,024 | 27,648 | 519.85 | 39,736 | 27,648 | 741.30 | 28,272 |
| in11.txt | 1,253 | 32,748 | 978.33 | 47,476 | 32,748 | 1,433.53 | 27,748 |
| in12.txt | 1,812 | 32,352 | 1,595.46 | 57,764 | 32,352 | 2,161.75 | 27,748 |
| in13.txt | 2,560 | 61,440 | 1,967.93 | 68,700 | 61,440 | 3,060.81 | 27,704 |
| in14.txt | 2,150 | 29,532 | 2,785.57 | 90,752 | 29,532 | 4,115.51 | 27,720 |
| in15.txt | 2,524 | 46,320 | 3,494.54 | 96,648 | 46,320 | 5,501.56 | 27,884 |

**Note:** All alignment costs match perfectly between basic and efficient algorithms, confirming correctness.

---

## 2. Performance Graphs

### Graph 1: CPU Time vs Problem Size
### Graph 2: Memory Usage vs Problem Size

**[INSERT: Datapoints/performance_plots.png HERE]**

The graphs clearly demonstrate:
- **Left Graph (CPU Time):** Both algorithms show quadratic time complexity O(n×m). The efficient algorithm has higher execution time due to recursive overhead from the divide-and-conquer approach.
- **Right Graph (Memory Usage):** The basic algorithm shows clear quadratic memory growth O(n×m), while the efficient algorithm maintains nearly constant memory usage O(n), demonstrating the key advantage of Hirschberg's algorithm.

---

## 3. Analysis and Insights

### 3.1 Time Complexity Analysis

**Basic Algorithm:**
- **Complexity:** O(n × m) where n and m are sequence lengths
- **Behavior:** Smooth quadratic growth as problem size increases
- **Performance:** Faster execution times across all test cases
- **Example:** For problem size 2,524 → 3,494 ms

**Efficient Algorithm:**
- **Complexity:** O(n × m) - same theoretical complexity
- **Behavior:** Quadratic growth with higher constant factors
- **Performance:** Slower due to recursive function call overhead
- **Example:** For problem size 2,524 → 5,502 ms (1.57× slower)

**Key Insight:** While both have the same asymptotic time complexity, the efficient algorithm is slower in practice due to:
1. Recursive function call overhead
2. Computing DP rows multiple times (forward and backward)
3. Additional array operations for divide-and-conquer

---

### 3.2 Space Complexity Analysis

**Basic Algorithm:**
- **Complexity:** O(n × m) - stores full DP table
- **Behavior:** Linear growth with problem size squared
- **Memory Range:** 27,680 KB → 96,648 KB
- **Memory Growth:** 68,968 KB increase (3.5× growth)
- **Limitation:** Cannot handle very large sequences due to memory constraints

**Efficient Algorithm:**
- **Complexity:** O(n) - stores only two rows at a time
- **Behavior:** Nearly constant memory usage
- **Memory Range:** 27,704 KB → 28,272 KB
- **Memory Growth:** Only 568 KB variation (essentially constant)
- **Advantage:** Can handle sequences that would cause memory overflow in basic algorithm

**Key Insight:** At the largest problem size (2,524):
- Basic uses: 96,648 KB
- Efficient uses: 27,884 KB
- **Memory savings: 68,764 KB (71.1% reduction)**

This demonstrates the practical value of Hirschberg's algorithm for memory-constrained environments.

---

### 3.3 Trade-offs and Recommendations

| Aspect | Basic Algorithm | Efficient Algorithm |
|--------|----------------|---------------------|
| **Time** |  Faster (lower constants) |  Slower (recursive overhead) |
| **Memory** |  High O(n×m) |  Low O(n) |
| **Implementation** |  Simpler |  More complex |
| **Scalability** |  Limited by memory |  Handles large inputs |

**When to use Basic Algorithm:**
- Small to medium sequences (< 2,000 characters)
- When execution speed is critical
- When memory is not a constraint
- For quick prototyping and testing

**When to use Efficient Algorithm:**
- Large sequences (> 2,000 characters)
- Memory-constrained systems
- When memory usage is critical
- Production systems handling variable-length inputs

---

## 4. Implementation Details

### 4.1 Basic Algorithm Approach
- **Method:** Standard Dynamic Programming with backtracking
- **Data Structures:**
  - 2D DP table for costs: `dp[i][j]`
  - 2D arrow table for path reconstruction: `arrow[i][j]`
- **Steps:**
  1. Initialize base cases (gaps along edges)
  2. Fill DP table using recurrence relation
  3. Backtrack from `dp[m][n]` to reconstruct alignment

### 4.2 Efficient Algorithm Approach
- **Method:** Hirschberg's Divide-and-Conquer Algorithm
- **Data Structures:**
  - Two 1D arrays (forward and backward costs)
  - Recursive call stack
- **Steps:**
  1. Divide sequence 1 at midpoint
  2. Compute forward costs: `align(seq1[:mid], seq2)`
  3. Compute backward costs: `align(seq1[mid:][::-1], seq2[::-1])`
  4. Find optimal split point in sequence 2
  5. Recursively solve left and right subproblems
  6. Combine results

### 4.3 Key Parameters
- **Gap Penalty (δ):** 30
- **Mismatch Costs (α):**
  ```
       A    C    G    T
  A    0   110   48   94
  C   110   0   118   48
  G    48  118   0   110
  T    94   48  110   0
  ```

---

## 5. Correctness Verification

All 15 test cases show matching alignment costs between both algorithms:
-  Costs match perfectly (168, 960, 1848, 5760, 7680, 5244, 7728, 11136, 19116, 27648, 32748, 32352, 61440, 29532, 46320)
-  All alignments are valid (proper gap insertion)
-  No violations of alignment rules

**Note:** Different algorithms may produce different alignments with the same minimum cost (as stated in project requirements), which is acceptable.

---

## 6. Conclusion

This project successfully implemented both versions of the sequence alignment algorithm:

1. **Basic Algorithm:** Provides optimal alignments with fast execution but high memory usage
2. **Efficient Algorithm:** Achieves 71% memory reduction while maintaining correctness, at the cost of slower execution

The results clearly demonstrate the classic **time-space trade-off** in algorithm design. The efficient algorithm (Hirschberg's) is a practical example of how divide-and-conquer techniques can dramatically reduce space complexity from O(n×m) to O(n) while maintaining the same time complexity.
