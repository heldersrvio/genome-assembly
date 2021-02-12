def kdMer(sequence, k, d):
	return sorted([sequence[i : i + k] + "|" + sequence[i + k + d : i + 2 * k + d] for i in range(len(sequence) - 2 * k - d + 1)])

def readInput():
	digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
	nucleotides = ['A', 'T', 'C', 'G', 'U']
	kVerified = False
	dVerified = False
	k = ''
	d = ''
	sequence = ''
	input = open("input.fasta", "r")
	for line in input:
		for character in line:
			if character == "k":
				kVerified = True
			if character == "d":
				dVerified = True
			if character in digits and kVerified and not dVerified:
				k += character
			elif character in digits and kVerified and dVerified:
				d += character
			elif character in nucleotides and kVerified and dVerified:
				sequence += character
	input.close()
	if not kVerified or not dVerified:
		raise NameError("Um ou os dois valores de k e d nao foram encontrados")
	else:
		return [sequence, int(k), int(d)]

def saveOutput(outputList):
	output = open("output.txt", "w")
	output.write("\n".join(outputList))
	output.close()

input = readInput()
saveOutput(kdMer(input[0], input[1], input[2]))