def bubbleSort(arr):
	count = len(arr)
	if count == 0:
		return None
	change_flag = count
	while change_flag > 0:
		end_position = change_flag
		change_flag = 0
		for j in range(1, end_position):
			if arr[j] < arr[j-1]:
				arr[j], arr[j-1] = arr[j-1], arr[j]
				change_flag = j
	return arr


arr = bubbleSort([73,119,55,66,88,12,15, 23,67])
print arr