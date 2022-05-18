inp = int(input("Enter Numeric: "))
out_str = ''
string = str(inp)[::-1]
if len(string) > 4:
	print('Enter value in 4 digits')
	exit()

for i in range(len(string)):
	if i == 0:
		until_3 = 'I'
		forth = 'IV'
		until_8 = 'V'
		nineth = 'IX'
	elif i == 1:
		until_3 = 'X'
		forth = 'XL'
		until_8 = 'L'
		nineth = 'XC'
	elif i == 2:
		until_3 = 'C'
		forth = 'CD'
		until_8 = 'D'
		nineth = 'CM'
	else:
		until_3 = 'M'
		forth = 'MV'
		until_8 = 'V'
		nineth = 'NONE'
		
	if string[i] <= '3':
		single = int(string[i]) * until_3
	elif string[i] == '4':
		single = forth
	elif string[i] >= '5' and string[i] <= '8':
		single = until_8 + (int(string[i]) - 5) * until_3
	else: single = nineth
	
	out_str = single + out_str

print('Roman letter is:', out_str)

