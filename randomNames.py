import numpy as np
import sys

def read_names(filename):
    try:
        with open(filename, 'r') as file:
            names = file.readlines()
            # Strip whitespace and newlines
            names = [name.strip() for name in names if name.strip()]
            return names
    except FileNotFoundError:
        print(f"The file {filename} was not found.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python randomNames.py filename")
        sys.exit(1)
    
filename = sys.argv[1]
names = read_names(filename)
# print("Names:")
# for name in names: print(name)

np.random.shuffle(names)
print('')
print('Random Ordered Names:')
print('')    
for name in names: print(name)
print('')