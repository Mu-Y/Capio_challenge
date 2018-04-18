import re
import sys
from sklearn.metrics import confusion_matrix

def shiftSinglePunctuation(ref_words):  
	""" 
	Append some isolated special characters(comma, period, question mark)to its previous character
	Return the new words list
	E.g. To tansform text like "abc , def" to "abc, def"
	"""
	i = 0
	while i<len(ref_words)-1:
		if ref_words[i+1] == ',' or ref_words[i+1] == '.' or ref_words[i+1] == '?' :
			ref_words[i] = ref_words[i] + ref_words[i+1]
			del ref_words[i+1]
		else:
			i = i + 1 
	return ref_words 

def divideAcronyms(ref_words):   
	""" 
	Divide Acronyms with multiple periods, to get ref_words with same length as output_words
	Return the new words list
	E.g. To transform text like "U.S. N.A." to "U. S. N. A."

	"""    
	i = 0
	ref_words_temp = []
	while i<len(ref_words):
		# get multiple index of period
		period_index = [pos for pos, char in enumerate(ref_words[i]) if char == '.']
		# store divided words into a new list ref_words_temp 
		if len(period_index)>1:
			period_index = [-1] + period_index 
			for j in range(len(period_index)-1):
				ref_words_temp.append(ref_words[i][period_index[j]+1:period_index[j+1]+1])
			if period_index[-1] != len(ref_words[i])-1:
				ref_words_temp.append(ref_words[i][period_index[-1]+1:])
		else:
			ref_words_temp.append(ref_words[i])
		i=i+1
	ref_words = ref_words_temp 
	return ref_words

def preprocessingRef(ref_text):     
	""" 
	Preprocess ref_text to get ref_words which align with output_words
	Return the new words list and preprosess error
	"""
	# replace special characters with space, to transform text like "june/july" to "june july"
	# will subtract the #replacement in accuracy calculation
	ref_text, prepros_err = re.subn(r'[^a-zA-Z0-9\,\.\?\' ]',' ', ref_text) 
	# from text to words
	ref_words = ref_text.split()
	ref_words = divideAcronyms(ref_words)
	ref_words = shiftSinglePunctuation(ref_words) 

	return (ref_words, prepros_err )

def getLabel(words):              
	""" 
	Return predicted label(from output_words) or GT label(from ref_words)

	"""
	label = []
            
	for word in words:
		if (word[-1]>='a' and word[-1]<='z') or (word[-1]>='A' and word[-1]<='Z'):
			label.append(' ')       # The label is "Add nothing"
		else:
			label.append(word[-1])   # The label is "Add comma, period, or question mark"

	return label

def evalFormatting(ref_text, output_text):
	""" 
	Get confusion matrix and calculate Accuracy from the matrix

	"""
	ref_words, prepros_err = preprocessingRef(ref_text)
	output_words = output_text.split()
	ref_label = getLabel(ref_words)
	output_label = getLabel(output_words)

	

	if len(ref_label) == len(output_label):
		con_matrix = confusion_matrix(ref_label, output_label, [' ', ',', '.', '?'])
		# exclude the cases where characters other than {, . ? space} should be added
		con_matrix[0,0] = con_matrix[0,0] - prepros_err        

		Acc = float((con_matrix[0,0] + con_matrix[1,1] + con_matrix[2,2] + con_matrix[3,3]) / float(len(ref_label)))
		print 'Accuracy = ', Acc
		print 'Confusion Matrix = \n', con_matrix
	else:
		print 'Different label length. Cannot get confusion matrix.'   

def main():
	############# check args ###############
	if len(sys.argv) != 5:
		print "Argument Error. Wrong arguments number."
		return 
	else:
		if sys.argv[1] != '--output-file' or sys.argv[3] != '--reference-file':
			print "Argument Error. Use format as: --output-file <OUTPUT_TEXT_FILE> --reference-file <REFERENCE_TEXT_FILE> ."
			return 
		else:
			output_file_path = sys.argv[2]
			reference_file_path = sys.argv[4]
	################# read files and evaluate ##############
	reference_file = open(reference_file_path,'r')
	output_file = open(output_file_path, 'r')

	i = 0
	while True:
		output_line = output_file.readline()
		ref_line = reference_file.readline()
		if len(output_line) == 0 or len(ref_line) == 0:
			break
		else:
			print ('This is the result of %dth line' % (i+1))
			evalFormatting(ref_line, output_line)
			i = i + 1

	############## close files ################
	reference_file.close()	
	output_file.close()	


if __name__ == "__main__":
	main()














