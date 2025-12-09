
import sys

def solve():
    filename = 'input.txt'
    if len(sys.argv) > 1:
        filename = sys.argv[1]

    try:
        with open(filename, 'r') as f:
            line = f.read().strip()
    except FileNotFoundError:
        print(f"Please create '{filename}' with your puzzle input.")
        return

    if not line:
        return

    # Parse map
    # 2333133121414131402
    # Digits alternate: length of file, length of free space
    
    blocks = []
    file_id = 0
    is_file = True
    
    for char in line:
        length = int(char)
        if is_file:
            blocks.extend([file_id] * length)
            file_id += 1
        else:
            blocks.extend([-1] * length) # -1 for free space
        is_file = not is_file
        
    # Compact
    # Move file blocks from end to leftmost free space
    
    # Using a list of blocks is simple enough if total length isn't massive.
    # Input is single line, so likely manageable.
    
    # Two pointers?
    # Or just find first free space from left, first file from right.
    
    # Part 1 implementation preserved but using list copy
    blocks_part1 = list(blocks)
    left = 0
    right = len(blocks_part1) - 1
    
    while True:
        while left < len(blocks_part1) and blocks_part1[left] != -1:
            left += 1
        while right >= 0 and blocks_part1[right] == -1:
            right -= 1
        if left >= right:
            break
        blocks_part1[left] = blocks_part1[right]
        blocks_part1[right] = -1

    checksum1 = 0
    for i, file_id in enumerate(blocks_part1):
        if file_id != -1:
            checksum1 += i * file_id
    print(f"Result (Part 1): {checksum1}")

    # Part 2: Move whole files (Dense approach for correctness)
    # Re-parse line into dense array blocks
    
    disk = []
    file_id = 0
    is_file = True
    for char in line:
        length = int(char)
        if is_file:
            disk.extend([file_id] * length)
            file_id += 1
        else:
            disk.extend([-1] * length)
        is_file = not is_file

    max_file_id = file_id - 1
    
    # Pre-calculate file positions and lengths
    # Since we strictly move files to empty space, files never shift or resize until we move them.
    # And we iterate strictly max_id down to 0, so when we look at file K, it is still at its original position
    # (because we never move logical files other than the current one, and we only overwrite free space).
    
    file_info = {} # id -> (start, length)
    
    # Scan disk to find files? Or just compute during parse?
    # Computing during parse is O(1).
    # Let's re-parse to be clean.
    
    curr_file_id = 0
    is_file = True
    pos = 0
    disk_len = len(disk)
    
    for char in line:
        length = int(char)
        if is_file:
            if length > 0: # Only record actual files
                file_info[curr_file_id] = (pos, length)
            curr_file_id += 1
        pos += length
        is_file = not is_file
        
    # Process files
    for fid in range(max_file_id, -1, -1):
        if fid not in file_info:
            continue
            
        start_pos, length = file_info[fid]
        
        # Find leftmost free span of 'length' strictly to left of 'start_pos'
        # Linear scan of 'disk'
        
        best_spot = -1
        free_count = 0
        
        for i in range(start_pos):
            if disk[i] == -1:
                free_count += 1
                if free_count >= length:
                    best_spot = i - length + 1
                    break
            else:
                free_count = 0
        
        if best_spot != -1:
            # Move file
            # Update disk
            for k in range(length):
                disk[best_spot + k] = fid
                disk[start_pos + k] = -1
                
    # Checksum
    checksum2 = 0
    for i, val in enumerate(disk):
        if val != -1:
            checksum2 += i * val
            
    print(f"Result (Part 2): {checksum2}")

if __name__ == '__main__':
    solve()
