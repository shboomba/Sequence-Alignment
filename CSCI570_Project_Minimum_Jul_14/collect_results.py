import os

# Collect results from all datapoint outputs
results = []

for i in range(1, 16):
    basic_file = f"Datapoints/basic_out{i}.txt"
    efficient_file = f"Datapoints/efficient_out{i}.txt"

    try:
        # Read basic results
        with open(basic_file, 'r') as f:
            lines = f.readlines()
            basic_cost = lines[0].strip()
            basic_str1 = lines[1].strip()
            basic_str2 = lines[2].strip()
            basic_time = lines[3].strip()
            basic_mem = lines[4].strip()

        # Read efficient results
        with open(efficient_file, 'r') as f:
            lines = f.readlines()
            eff_cost = lines[0].strip()
            eff_str1 = lines[1].strip()
            eff_str2 = lines[2].strip()
            eff_time = lines[3].strip()
            eff_mem = lines[4].strip()

        # Calculate problem size (m+n where m and n are original sequence lengths)
        problem_size = len(basic_str1)  # aligned strings have same length = m+n

        results.append({
            'file': f'in{i}.txt',
            'problem_size': problem_size,
            'basic_cost': basic_cost,
            'basic_time': basic_time,
            'basic_mem': basic_mem,
            'eff_cost': eff_cost,
            'eff_time': eff_time,
            'eff_mem': eff_mem
        })
    except Exception as e:
        print(f"Error processing in{i}.txt: {e}")

# Print results table
print("\n" + "="*120)
print("SEQUENCE ALIGNMENT RESULTS")
print("="*120)
print(f"{'File':<12} {'Size':<8} {'Basic Cost':<12} {'Basic Time(ms)':<16} {'Basic Mem(KB)':<15} {'Eff Cost':<12} {'Eff Time(ms)':<16} {'Eff Mem(KB)':<15}")
print("-"*120)

for r in results:
    print(f"{r['file']:<12} {r['problem_size']:<8} {r['basic_cost']:<12} {r['basic_time']:<16} {r['basic_mem']:<15} {r['eff_cost']:<12} {r['eff_time']:<16} {r['eff_mem']:<15}")

print("="*120)

# Save to CSV
with open('Datapoints/results.csv', 'w') as f:
    f.write("File,Problem_Size,Basic_Cost,Basic_Time_ms,Basic_Memory_KB,Efficient_Cost,Efficient_Time_ms,Efficient_Memory_KB\n")
    for r in results:
        f.write(f"{r['file']},{r['problem_size']},{r['basic_cost']},{r['basic_time']},{r['basic_mem']},{r['eff_cost']},{r['eff_time']},{r['eff_mem']}\n")

print("\nResults saved to Datapoints/results.csv")

# Verify costs match
print("\nCost Verification:")
all_match = True
for r in results:
    if r['basic_cost'] != r['eff_cost']:
        print(f"MISMATCH {r['file']}: Basic={r['basic_cost']}, Efficient={r['eff_cost']}")
        all_match = False

if all_match:
    print("SUCCESS: All costs match between basic and efficient algorithms!")
