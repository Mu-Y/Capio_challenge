
import requests
import sys
import json





def formatText(input_text, endpoint):
	"""
	Call API, according to endpoint argument
	"""
	data = {"text": input_text}
	print 'Waiting for return ...'
	req = requests.post(str(endpoint), json = data)

	output_text = req.json()['result']
	return output_text


def textfileFormat(input_file_path, output_file_path, endpoint):
	"""
	Call API
	Take input text file and api endpoint, generate output text file to a path 

	"""
	file_in = open(input_file_path,'r')
	file_out = open(output_file_path, 'w')
	i = 0;

	for line in file_in:
		input_text = line
		output_text = formatText(input_text, endpoint)     
		file_out.write(output_text + '\n')      # the returned output_text has no eol '\n'
		i = i+1
		print ("Now processed %d lines." % i)

	print 'Done!'

	file_out.close()	
	file_in.close()





def main():

	################# Check args #############################################
	if len(sys.argv) != 7:
		print "Argument Error. Wrong arguments number."
		return 
	else:
		if sys.argv[1] != '--input-file' or sys.argv[3] != '--output-file' or sys.argv[5] != '--api-endpoint':
			print "Argument Error. Use format as: --input-file <INPUT_TEXT_FILE> --output-file <OUTPUT_FILE_NAME> --api-endpoint <API_ENDPOINT> ."
			return 
		else:
			input_file_path = sys.argv[2]
			output_file_path = sys.argv[4]
			endpoint = sys.argv[6]
	print '=============Processing input file. Generating output file============'
	textfileFormat(input_file_path, output_file_path, endpoint)
	print '=============Successfully generated output file===================='


if __name__ == "__main__":
	main()