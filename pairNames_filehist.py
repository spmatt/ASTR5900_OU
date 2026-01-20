import random
import itertools
import sys
import json

# Define function that will read names from a file
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

# Define a function that creates the pairs of list items
def generate_pairs(items, history, n):
    # Generate all possible unique pairs
    all_pairs = list(itertools.combinations(items, 2))
    
    # Filter out pairs that have been seen in the last N iterations
    recent_pairs = set(itertools.chain(*history[-n:]))
    available_pairs = [pair for pair in all_pairs if pair not in recent_pairs]
    
    # Check if there are enough pairs to form without repetition
    if len(available_pairs) < len(items) // 2:
        raise ValueError("Not enough new pairs can be formed. Please increase N or reset history.")
    
    # Randomly choose pairs from the available ones
    chosen_pairs = []
    while len(chosen_pairs) < len(items) // 2:
        if not available_pairs:
            print("Unable to find suitable pairs. Try again or reduce the constraint (N).")
            return []
        
        pair = random.choice(available_pairs)
        temp_pairs = [p for p in available_pairs if not (p[0] in pair or p[1] in pair)]

        # Check if there will be enough pairs left to complete the process
        if len(temp_pairs) >= (len(items) // 2) - len(chosen_pairs) - 1:
            chosen_pairs.append(pair)
            available_pairs = temp_pairs
        else:
            # Skip this pair and try another one
            available_pairs.remove(pair)

    # If odd number of items, add the last one to a random pair
    # if len(items) % 2 != 0:
    #     remaining_item = list(set(items) - set(itertools.chain(*chosen_pairs)))[0]
    #     chosen_pairs[random.randint(0, len(chosen_pairs) - 1)] += (remaining_item,)

    # If odd number of items, add the last one as a single item
    if len(items) % 2 != 0:
        remaining_item = list(set(items) - set(itertools.chain(*chosen_pairs)))[0]
        chosen_pairs.append(remaining_item)
    
    return chosen_pairs

# Function to write historical pairs to file.
def save_history(history, filename):
    with open(filename, 'w') as f:
        # Convert each set of tuples to a list of lists
        history_to_save = [[list(pair) for pair in pairs] for pairs in history]
        json.dump(history_to_save, f)

# Function to read historical pairs from file.        
def load_history(filename):
    try:
        with open(filename, 'r') as f:
            history = json.load(f)
            # Convert the inner lists back to tuples
            history = [list(tuple(pair) for pair in pairs) for pairs in history]
            return history
    except FileNotFoundError:
        print(f"History file {filename} not found. Starting with a new history.")
        return []
    except json.JSONDecodeError:
        print(f"Error decoding the history file {filename}. File might be corrupted.")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

### Start doing work

# Check if user has given the filename for the list of names.
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python script.py filename_namelist")
        sys.exit(1)
     
# Read in the list of names
filename = sys.argv[1]
names = read_names(filename)

# Load history
history_filename = 'pairing_history.json'
history = load_history(history_filename)
# Define number of iterations to remember
N = 10

# Generate pairs, write to screen and update history file.
try:
    pairs = generate_pairs(names, history, N)
    # print(f"This round's pairs: {pairs}")
    print('')
    print("Guarantees no repeats within {} rounds.\nThis round's pairs:\n".format(N))
    for pair in pairs:
        if isinstance(pair, tuple):
            print(pair[0], ',', pair[1])
        else: print(pair)
    print('')
    # history.append(set(itertools.chain(*pairs)))
    history.append([list(pair) for pair in pairs])  # Convert tuples to lists for JSON serialization
    # Keep only the last N histories
    if len(history) > N:
        history.pop(0)
    # Keep only the last N histories
    # history = history[-N:]
    # Save history
    save_history(history, history_filename)
except ValueError as e:
    print(e)

        