from enum import Enum
import sys 
# from resource import * 
import time
import psutil 

class Arrow(Enum):
    MATCH = 0
    SEQ1_GAP = 1
    SEQ2_GAP = 2

def process_memory(): 
    process = psutil.Process() 
    memory_info = process.memory_info() 
    memory_consumed = int(memory_info.rss/1024) 
    return memory_consumed

def time_wrapper(): 
    start_time = time.time() 
    cost, str1, str2 = basic()
    end_time = time.time() 
    time_taken = (end_time - start_time)*1000 
    process_memory_consumed = process_memory()
    return cost, str1, str2, time_taken, process_memory_consumed

def basic():
    # Create two sequences based on the input file
    seq1, seq2 = create_sequence()

    # gap deduction score
    s = 30

    # mismatch score deduction array
    mismatch_arr = [ [0, 110, 48, 94], 
                     [110, 0, 118, 48], 
                     [48, 118, 0, 110], 
                     [94, 48, 110, 0] ]

    dp = [[0 for _ in range(len(seq2)+1)] for _ in range(len(seq1)+1)]
    arrow_arr = [[0 for _ in range(len(seq2)+1)] for _ in range(len(seq1)+1)]
    
    # populate base case
    for i in range(len(seq1)+1):
        dp[i][0] = i * s
    for j in range(len(seq2)+1):
        dp[0][j] = j * s
    

    # dp population 3 cases: mismatch, gap in seq1, gap in seq2. This also adds arrows for backtracking to create the final alignment strings
    for i in range(1, len(seq1)+1):
        for j in range(1, len(seq2)+1):
            char1 = seq1[i-1]
            char2 = seq2[j-1]
            index1 = "ACGT".index(char1)
            index2 = "ACGT".index(char2)
            mismatch_score = mismatch_arr[index1][index2]
            

            mismatch = dp[i-1][j-1] + mismatch_score
            seq1_gap = dp[i-1][j] + s
            seq2_gap = dp[i][j-1] + s

            if mismatch <= seq1_gap and mismatch <= seq2_gap:
                arrow_arr[i][j] = Arrow.MATCH
            elif seq1_gap <= mismatch and seq1_gap <= seq2_gap:
                arrow_arr[i][j] = Arrow.SEQ1_GAP
            else:
                arrow_arr[i][j] = Arrow.SEQ2_GAP

            dp[i][j] = min(
                mismatch,  # mismatch
                seq1_gap,  # gap in seq1
                seq2_gap   # gap in seq2
            )

    str1, str2 = create_aligned_strings(dp, arrow_arr, seq1, seq2)

    # ACACTGACTACTGACTGGTGACTACTGACTGG
    # TATTATACGCTATTATACGCGACGCGGACGCG 
    
    
    
    
    
    return dp[len(seq1)][len(seq2)], str1, str2

def create_aligned_strings(dp, arrow_arr, seq1, seq2):
    seq1_str = ""
    seq2_str = ""

    # backtracking to create aligned strings
    i = len(seq1)
    j = len(seq2)
    

    while i > 0 or j > 0:
        # mismatch (arrow facing top left)
        if arrow_arr[i][j] == Arrow.MATCH:
            seq1_str = seq1[i-1] + seq1_str
            seq2_str = seq2[j-1] + seq2_str
            i -= 1
            j -= 1
        # gap in seq2 (arrow facing up)
        elif arrow_arr[i][j] == Arrow.SEQ1_GAP:
            seq1_str = seq1[i-1] + seq1_str
            seq2_str = "_" + seq2_str
            i -= 1
        # gap in seq1 (arrow facing left)
        else:
            seq1_str = "_" + seq1_str
            seq2_str = seq2[j-1] + seq2_str
            j -= 1
    return seq1_str, seq2_str

def create_sequence():
    # input file name
    filename = 'SampleTestCases/input3.txt'
    with open(filename, 'r') as file:
        data = file.read().strip().splitlines()
    
    second_seq_start = 0
    sequence1 = data[0]
    # make a while loop the next lines in data are integers, add a copy of sequence1 to index of the int in the current sequence1
    for line in data[1:]:
        if not line.isdigit():
            second_seq_start = data.index(line)
            break
        index = int(line) + 1
        sequence1 = sequence1[:index] + sequence1 + sequence1[index:]
    sequence2 = data[second_seq_start]
    for line in data[second_seq_start+1:]:
        index = int(line) + 1
        sequence2 = sequence2[:index] + sequence2 + sequence2[index:]
    return sequence1, sequence2

if __name__ == "__main__":
    #create an output file and write the results to it
    cost, str1, str2, time_taken, memory_consumed = time_wrapper()
    with open('output.txt', 'w') as f:
        f.write(f"{cost}\n")
        f.write(f"{str1}\n")
        f.write(f"{str2}\n")
        f.write(f"{time_taken}\n")
        f.write(f"{memory_consumed}\n")


