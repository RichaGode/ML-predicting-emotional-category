import csv
from nltk.tokenize import RegexpTokenizer


vocab = dict()
def main():


	file = open('dysfluencytest.csv')
	reader = csv.DictReader(file)
	for row in reader:
		cleaned_text = row['cleaned text']
		vocab_generator(cleaned_text) 

	with open('bowtest.csv', mode='w') as bog_file:
		bog_file_writer = csv.writer(bog_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
		header = ['swda_filename', 'transcript index', 'act_tag', 'original text', 'cleaned text']
		thresholded_vocab_list = [x for x in vocab.keys() if vocab[x] > 200]
		print(len(thresholded_vocab_list))
		# max_key = max(vocab, key=lambda k: vocab[k])
		# print(vocab[max_key])

		header.extend(thresholded_vocab_list)
		bog_file_writer.writerow(header)

		file = open('dysfluencytest.csv')
		reader = csv.DictReader(file)
		for row in reader:
			cleaned_text = row['cleaned text']
			updated_tokenized_utterance = vocab_per_utterance(cleaned_text)
			bog_model = list()
			for elem in thresholded_vocab_list:
				if elem in updated_tokenized_utterance:
					bog_model.append('1')
				else:
					bog_model.append('0')
			values = [row['swda_filename'], row['transcript index'], row['act_tag'], row['original text'], row['cleaned text']]
			values.extend(bog_model)
			bog_file_writer.writerow(values)


def vocab_per_utterance(cleaned_text):
	updated_tokenized_utterance = set()
	tokenizer = RegexpTokenizer(r'\w+') #strip punctuation
	tokenized_utterance = tokenizer.tokenize(cleaned_text)
	for elem in tokenized_utterance:
		updated_tokenized_utterance.add(elem.lower())
	return updated_tokenized_utterance

def vocab_generator(cleaned_text): 
		updated_tokenized_utterance = set()
		tokenizer = RegexpTokenizer(r'\w+') #strip punctuation
		tokenized_utterance = tokenizer.tokenize(cleaned_text)
		for elem in tokenized_utterance:
			if elem.lower() not in vocab.keys():
				vocab[elem.lower()] = 1
			else:
				vocab[elem.lower()] +=1

main()