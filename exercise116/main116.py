import math

import numpy as np
# (1) Generating and displaying the array
print("\n(1) Generating and displaying the array: ")
arr=np.random.randint(-100,500,10)
print(arr)

# (2) Showing elements at positions 2-5
print("\n(2) Showing elements at positions 2-5: ")
arr2=arr[[2,3,4,5]]
print(arr2)
arr3=arr[2:6]
print(arr3)

# (3) Output elements with negative values
print("\n(3) Elements with negative values: ")
arr4=arr[arr < 0]
print(arr4)

# (4) Output elements with values from x to y
x = int(input("\n(4) Enter lower bound (x): "))
y = int(input("Enter upper bound (y): "))
arr5=arr[(arr >= x) & (arr <= y)]
print(arr5)

# (5) Filter out negative numbers in the array
print("\n(5) Removing negative numbers: ")
arr6= arr[arr >= 0]
print(arr6)

# (6) Sort the array in ascending order
print("\n(6) Sorting in ascending order: ")
arr7 = np.sort(arr)
print(arr7)

# (7) Sort the array in descending order
print("\n(7) Sorting in descending order: ")
arr8= np.sort(arr)[::-1]
print(arr8)

# (8) Output basic statistical values
print("\n(8) Statistical values: ")
print(f"Minimum value: {np.min(arr)}")
print(f"Maximum value: {np.max(arr)}")
print(f"Mean value: {np.mean(arr)}")
print(f"Median value: {np.median(arr)}")
print(f"Standard deviation: {np.std(arr)}")

# (9) Delete elements that are perfect squares
# Function to check if a number is a perfect square
def is_perfect_square(n):
    if n < 0:
        return False
    sqrt_n = int(math.sqrt(n))
    return sqrt_n * sqrt_n == n

# Create a mask for non-perfect squares
non_perfect_squares_mask = np.array([not is_perfect_square(num) for num in arr])
arr_no_squares = arr[non_perfect_squares_mask]
print(arr_no_squares)

# (10) Insert X into position V
X = int(input("\n(10) Enter value to insert (X): "))
V = int(input("Enter position to insert at (V): "))

# Make sure V is within valid range
if V < 0 or V > len(arr):
    print("Invalid position. Position should be between 0 and", len(arr))
else:
    # Create a new array with the inserted value
    new_arr = np.insert(arr, V, X)
    print(f"Array after inserting {X} at position {V}:")
    print(new_arr)