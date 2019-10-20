import csv
import nltk
from nltk.util import ngrams
from nltk.tokenize import RegexpTokenizer

master_trigram_count = dict() #dictionary of the count of every trigram seen in the whole set
master_num = set()
def main(): 
	file = open('dysfluency.csv')
	reader = csv.DictReader(file)
	for row in reader:
		cleaned_text = row['cleaned text']
		val1, val2 = pos_trigram_generator(cleaned_text)
		master_num_2 = list(master_num)[:]
	thresholded_trigram_list = [x for x in master_trigram_count.keys() if master_trigram_count[x] > 1000]
	print("completed round 1 generation")
	##### write the header to the file with all of the unique POS and unique trigrams above a certain threshold ##### 
	with open('trigram_pos_train.csv', mode='w') as trigram_pos_file:
		trigram_pos_writer = csv.writer(trigram_pos_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		header = ['swda_filename', 'transcript index', 'act_tag', 'original text', 'cleaned text']
		header.extend(list(master_num))
		header.extend(thresholded_trigram_list)
		trigram_pos_writer.writerow(header)
		file = open('dysfluencytrain.csv')
		new_reader = csv.DictReader(file)
		for row in new_reader:
			act_tag = row['act_tag']
			swda_filename = row['swda_filename']
			swda_transcript_index = row['transcript index']
			original_text = row['original text']
			cleaned_text = row['cleaned text']
			val1, val2 = pos_trigram_generator(cleaned_text)
			pos_values = list()
			for elem in master_num_2: #iterate through all of the unique POS tags in the whole set
				print(elem)
				if elem in val1.keys(): #iterate through the POS tags found in this particular utterance
					pos_values.append(str(val1[elem])) #count appended if found
				else:
					pos_values.append('0') #append 0 otherwise
			print("finished generating POS values")
			trigram_values = list()
			for elem in thresholded_trigram_list:
				if elem in val2:
					trigram_values.append('1')
				else:
					trigram_values.append('0')
			print("finished generating trigram binary values")
			original_header = [swda_filename, swda_transcript_index, act_tag, original_text, cleaned_text]
			original_header.extend(pos_values)
			original_header.extend(trigram_values)
			trigram_pos_writer.writerow(original_header)


def pos_trigram_generator(cleaned_text):
		tokenizer = RegexpTokenizer(r'\w+')
		tokenized_utterance = tokenizer.tokenize(cleaned_text)
		pos_utterance = nltk.pos_tag(tokenized_utterance) #list of POS for each utterance
		pos_count = dict()
		for elem in pos_utterance:
			if elem[1] not in pos_count.keys():
				pos_count[elem[1]] = 1
			else:
				pos_count[elem[1]] +=1

		##### generate trigrams #####
		trigrams=ngrams(pos_utterance,3, pad_left=True, pad_right=True, left_pad_symbol='START', right_pad_symbol='STOP')
		trigrams_updated = list()
		for tup in trigrams:
			current_trigram = list()
			for item in tup:
				if type(item) == str:
					current_trigram.append(item)
				else:
					current_trigram.append(item[1])
			current_trigram = tuple(current_trigram)
			trigrams_updated.append(current_trigram)
		#master trigram count, which we will compare to later
		for elem in trigrams_updated:
			if elem not in master_trigram_count.keys():
				master_trigram_count[elem] = 1
			else:
				master_trigram_count[elem] += 1 
		for elem in pos_utterance: #the total number of unique POS tags 
			if elem[1] not in master_num:
				master_num.add(elem[1])
			else:
				continue
		return pos_count, trigrams_updated
main()