import sys
import time
import psutil

def process_memory():
    process = psutil.Process()
    memory_info = process.memory_info()
    memory_consumed = int(memory_info.rss/1024)
    return memory_consumed

def time_wrapper(input_file):
    start_time = time.time()
    cost, str1, str2 = efficient(input_file)
    end_time = time.time()
    time_taken = (end_time - start_time)*1000
    process_memory_consumed = process_memory()
    return cost, str1, str2, time_taken, process_memory_consumed

def efficient(input_file):
    # Create two sequences based on the input file
    seq1, seq2 = create_sequence(input_file)

    # gap penalty
    gap = 30

    # mismatch penalty matrix
    mismatch_arr = [[0, 110, 48, 94],
                    [110, 0, 118, 48],
                    [48, 118, 0, 110],
                    [94, 48, 110, 0]]

    # Use divide and conquer approach
    aligned_str1, aligned_str2 = hirschberg(seq1, seq2, gap, mismatch_arr)

    # Calculate final cost
    cost = calculate_cost(aligned_str1, aligned_str2, gap, mismatch_arr)

    return cost, aligned_str1, aligned_str2

def get_mismatch_cost(char1, char2, mismatch_arr):
    """Get mismatch cost between two characters"""
    if char1 == '_' or char2 == '_':
        return 0
    index1 = "ACGT".index(char1)
    index2 = "ACGT".index(char2)
    return mismatch_arr[index1][index2]

def calculate_cost(str1, str2, gap, mismatch_arr):
    """Calculate the total alignment cost"""
    cost = 0
    for i in range(len(str1)):
        if str1[i] == '_' or str2[i] == '_':
            cost += gap
        else:
            cost += get_mismatch_cost(str1[i], str2[i], mismatch_arr)
    return cost

def compute_last_row(seq1, seq2, gap, mismatch_arr):
    """
    Compute the last row of DP table using only O(n) space.
    Returns array where dp[j] = minimum cost to align seq1 with seq2[0:j]
    """
    m = len(seq1)
    n = len(seq2)

    # We only need current and previous row
    prev = [j * gap for j in range(n + 1)]

    for i in range(1, m + 1):
        curr = [i * gap]  # First column

        for j in range(1, n + 1):
            # Three choices: match/mismatch, gap in seq1, gap in seq2
            mismatch_cost = get_mismatch_cost(seq1[i-1], seq2[j-1], mismatch_arr)
            match = prev[j-1] + mismatch_cost
            gap_seq1 = prev[j] + gap
            gap_seq2 = curr[j-1] + gap

            curr.append(min(match, gap_seq1, gap_seq2))

        prev = curr

    return prev

def hirschberg(seq1, seq2, gap, mismatch_arr):
    """
    Memory-efficient sequence alignment using Hirschberg's algorithm.
    Uses divide and conquer with O(n) space complexity.
    """
    m = len(seq1)
    n = len(seq2)

    # Base cases
    if m == 0:
        return '_' * n, seq2

    if n == 0:
        return seq1, '_' * m

    if m == 1:
        # Simple alignment for single character
        return align_single_char(seq1[0], seq2, gap, mismatch_arr)

    if n == 1:
        # Simple alignment for single character
        str2, str1 = align_single_char(seq2[0], seq1, gap, mismatch_arr)
        return str1, str2

    # Divide seq1 into two halves
    mid = m // 2

    # Compute costs for left half
    left_costs = compute_last_row(seq1[:mid], seq2, gap, mismatch_arr)

    # Compute costs for right half (reversed)
    right_costs = compute_last_row(seq1[mid:][::-1], seq2[::-1], gap, mismatch_arr)
    right_costs = right_costs[::-1]

    # Find optimal split point in seq2
    min_cost = float('inf')
    split = 0

    for j in range(n + 1):
        total_cost = left_costs[j] + right_costs[j]
        if total_cost < min_cost:
            min_cost = total_cost
            split = j

    # Recursively solve left and right parts
    left_str1, left_str2 = hirschberg(seq1[:mid], seq2[:split], gap, mismatch_arr)
    right_str1, right_str2 = hirschberg(seq1[mid:], seq2[split:], gap, mismatch_arr)

    # Combine results
    return left_str1 + right_str1, left_str2 + right_str2

def align_single_char(char, seq, gap, mismatch_arr):
    """
    Align a single character with a sequence.
    Returns the alignment that gives minimum cost.
    Position i means char is matched/mismatched with seq[i]
    """
    n = len(seq)

    # Try aligning char with each position in seq
    min_cost = float('inf')
    best_str1 = ""
    best_str2 = ""

    for i in range(n + 1):
        # Build alignment strings
        if i == n:
            # char after entire sequence (gaps before char, seq followed by gap)
            str1 = '_' * n + char
            str2 = seq + '_'
            cost = n * gap + gap  # all seq chars are gaps in str1, char is gap in str2
        else:
            # char matched/mismatched with seq[i]
            str1 = '_' * i + char + '_' * (n - i)
            str2 = seq[:i] + seq[i] + seq[i+1:]  # keep full sequence
            # Insert gap in str2 for the char position
            str2 = seq

            # Actually need gaps in str2 for unmatched parts
            str1 = ''
            str2 = ''
            for j in range(n + 1):
                if j == i:
                    str1 += char
                    if j < n:
                        str2 += seq[j]
                else:
                    if j < n:
                        str1 += '_'
                        str2 += seq[j]

            cost = 0
            for j in range(len(str1)):
                if str1[j] == '_' or str2[j] == '_':
                    cost += gap
                else:
                    cost += get_mismatch_cost(str1[j], str2[j], mismatch_arr)

        if cost < min_cost:
            min_cost = cost
            best_str1 = str1
            best_str2 = str2

    return best_str1, best_str2

def create_sequence(filename):
    with open(filename, 'r') as file:
        data = file.read().strip().splitlines()

    second_seq_start = -1
    sequence1 = data[0]

    # Generate first sequence
    i = 1
    while i < len(data) and data[i].isdigit():
        index = int(data[i]) + 1
        sequence1 = sequence1[:index] + sequence1 + sequence1[index:]
        i += 1

    # Find second base string
    if i < len(data):
        second_seq_start = i
        sequence2 = data[second_seq_start]

        # Generate second sequence
        for line in data[second_seq_start+1:]:
            index = int(line) + 1
            sequence2 = sequence2[:index] + sequence2 + sequence2[index:]
    else:
        # No second sequence found
        sequence2 = ""

    return sequence1, sequence2

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python efficient.py <input_file> <output_file>")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    cost, str1, str2, time_taken, memory_consumed = time_wrapper(input_file)

    with open(output_file, 'w') as f:
        f.write(f"{cost}\n")
        f.write(f"{str1}\n")
        f.write(f"{str2}\n")
        f.write(f"{time_taken}\n")
        f.write(f"{memory_consumed}\n")
