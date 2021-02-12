nucleotides = ['A', 'T', 'G', 'C', 'U']

originalSequence = filter(lambda character: character in nucleotides, open("input.fasta", "r").read())
resultSequence = filter(lambda character: character in nucleotides, open("output.fasta", "r").read())

if originalSequence == resultSequence:
	print "OK"
else:
	print "Error"