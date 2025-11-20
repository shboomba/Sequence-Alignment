import matplotlib.pyplot as plt
import csv

# Read results from CSV
problem_sizes = []
basic_times = []
basic_memory = []
efficient_times = []
efficient_memory = []

with open('Datapoints/results.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        problem_sizes.append(int(row['Problem_Size']))
        basic_times.append(float(row['Basic_Time_ms']))
        basic_memory.append(float(row['Basic_Memory_KB']))
        efficient_times.append(float(row['Efficient_Time_ms']))
        efficient_memory.append(float(row['Efficient_Memory_KB']))

# Create figure with 2 subplots
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: CPU Time vs Problem Size
ax1.plot(problem_sizes, basic_times, marker='o', label='Basic Algorithm', linewidth=2, markersize=8)
ax1.plot(problem_sizes, efficient_times, marker='s', label='Efficient Algorithm', linewidth=2, markersize=8)
ax1.set_xlabel('Problem Size (m+n)', fontsize=12)
ax1.set_ylabel('Time (milliseconds)', fontsize=12)
ax1.set_title('CPU Time vs Problem Size', fontsize=14, fontweight='bold')
ax1.legend(fontsize=10)
ax1.grid(True, alpha=0.3)

# Plot 2: Memory Usage vs Problem Size
ax2.plot(problem_sizes, basic_memory, marker='o', label='Basic Algorithm', linewidth=2, markersize=8)
ax2.plot(problem_sizes, efficient_memory, marker='s', label='Efficient Algorithm', linewidth=2, markersize=8)
ax2.set_xlabel('Problem Size (m+n)', fontsize=12)
ax2.set_ylabel('Memory (KB)', fontsize=12)
ax2.set_title('Memory Usage vs Problem Size', fontsize=14, fontweight='bold')
ax2.legend(fontsize=10)
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('Datapoints/performance_plots.png', dpi=300, bbox_inches='tight')
print("Plots saved to Datapoints/performance_plots.png")

# Print insights
print("\n" + "="*80)
print("PERFORMANCE INSIGHTS")
print("="*80)

print("\n1. TIME COMPLEXITY:")
print(f"   - Basic Algorithm: Shows quadratic growth O(n*m)")
print(f"   - Efficient Algorithm: Also O(n*m) time but with higher overhead from recursion")
print(f"   - For small inputs, basic is faster due to lower constant factors")
print(f"   - For large inputs (problem size > 1000), efficient takes longer due to")
print(f"     recursive overhead despite same theoretical complexity")

print("\n2. SPACE COMPLEXITY:")
print(f"   - Basic Algorithm: Memory grows with problem size O(n*m)")
print(f"     - Smallest: {min(basic_memory):.0f} KB at size {problem_sizes[basic_memory.index(min(basic_memory))]}")
print(f"     - Largest: {max(basic_memory):.0f} KB at size {problem_sizes[basic_memory.index(max(basic_memory))]}")
print(f"     - Growth: {max(basic_memory) - min(basic_memory):.0f} KB increase")

print(f"\n   - Efficient Algorithm: Nearly constant memory O(n)")
print(f"     - Smallest: {min(efficient_memory):.0f} KB at size {problem_sizes[efficient_memory.index(min(efficient_memory))]}")
print(f"     - Largest: {max(efficient_memory):.0f} KB at size {problem_sizes[efficient_memory.index(max(efficient_memory))]}")
print(f"     - Growth: {max(efficient_memory) - min(efficient_memory):.0f} KB increase")

print(f"\n   - Memory Savings at largest problem size:")
print(f"     - Basic: {max(basic_memory):.0f} KB")
print(f"     - Efficient: {max(efficient_memory):.0f} KB")
print(f"     - Savings: {max(basic_memory) - max(efficient_memory):.0f} KB ({((max(basic_memory) - max(efficient_memory))/max(basic_memory)*100):.1f}% reduction)")

print("\n3. TRADE-OFFS:")
print("   - Basic Algorithm:")
print("     + Faster execution time")
print("     + Simpler implementation")
print("     - High memory usage for large inputs")
print("     - Cannot handle very large sequences due to memory constraints")

print("\n   - Efficient Algorithm:")
print("     + Much lower memory usage (nearly constant)")
print("     + Can handle larger sequences")
print("     - Slower due to recursive overhead")
print("     - More complex implementation")

print("\n4. RECOMMENDATION:")
print("   - Use Basic Algorithm: Small to medium inputs (< 2000 chars)")
print("   - Use Efficient Algorithm: Large inputs or memory-constrained systems")

print("="*80)

plt.show()
