misses = input("Enter L1-dcache-load-misses: ")
misses = int(misses.replace(",", ""))

instr = input("Enter instructions: ")
instr = int(instr.replace(",", ""))

print(f"L1 Cache Miss rate PTI: {misses / (instr / 1000):.4f}")
