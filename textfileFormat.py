from api_test import formatText
import requests
import sys

# './dataset/unformatted/000.txt'
# './dataset/unformatted/000_out.txt'


def textfileFormat(input_file_path, output_file_path):
	file_in = open(input_file_path,'r')
	file_out = open(output_file_path, 'w')
	i = 0;

# input_text = file_in.read()
# output_text = formatText(input_text)
# print output_text
	for line in file_in:
		input_text = line
		output_text = formatText(input_text)
		# print output_text
		file_out.write(output_text + '\n')
		i = i+1
		# print ('now processed' + str(i))
		print ("Now processed %d lines." % i)

	print 'Done!'

	file_out.close()	
	file_in.close()

# def wholeFormat():


def main():
	if len(sys.argv) != 5:
		print "Argument Error. Wrong arguments number."
		return 
	else:
		if sys.argv[1] != '--input-file' or sys.argv[3] != '--output-file':
			print "Argument Error. Use format as: --input-file <INPUT_TEXT_FILE> --output-file <OUTPUT_FILE_NAME> ."
			return 
		else:
			input_file_path = sys.argv[2]
			output_file_path = sys.argv[4]
	textfileFormat(input_file_path, output_file_path)

if __name__ == "__main__":
	main()