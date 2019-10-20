import csv
import pandas as pd
master_features = set()

def main(file1, file2, file3, file4):
	# training_features_1 = list(pd.read_csv(file1, nrows=1).columns)
	# training_features_2 = list(pd.read_csv(file2, nrows=1).columns)
	# training_features_3 = list(pd.read_csv(file3, nrows=1).columns)

	# #now you want to add each of these to a master set:

	# for elem in training_features_1:
	# 	master_features.add(elem)
	# for elem in training_features_2:
	# 	master_features.add(elem)
	# for elem in training_features_3:
	# 	master_features.add(elem)

	# #master features now contains every single unique feature across all 3 training files
	# #we now want to make a csv that contains the values from all of these files

	# #set of features that are not in each of the different files
	# file_1_columns_added = master_features - set(training_features_1) #all of the values from files 2 and 3
	# file_2_columns_added = master_features - set(training_features_2) #all of the values from files 1 and 3
	# file_3_columns_added = master_features - set(training_features_3) #all of the values from files 1 and 2 

	li = []
	f1 = open(file1)
	df1 = pd.read_csv(f1, index_col=None, header=0)
	updated_file_1 = df1.drop(['swda_filename', 'transcript_index', 'act_tag', 'ptb_basename', 'conversation_no', "caller", "utterance_index", "subutterance_index", "text","pos","trees","ptb_treenumbers"], axis=1)
	li.append(updated_file_1)
	f2 = open(file2)
	df2 = pd.read_csv(f2, index_col=None, header=0)
	li.append(df2)
	f3 = open(file3)
	df3 = pd.read_csv(f3, index_col=None, header=0)
	updated_file_3 = df3.drop(['swda_filename', 'transcript index', 'act_tag','cleaned text', 'original text'], axis=1)
	li.append(updated_file_3)
	f4 = open(file4)
	df4 = pd.read_csv(f4, index_col=None, header=0)
	updated_file_4 = df4.drop(['swda_filename', 'transcript index', 'act_tag','cleaned text', 'original text'], axis=1)
	li.append(updated_file_4)

	frame = pd.concat(li, axis=1)
	
	frame.to_csv('test_merged_FEATURES123LIWC.csv', index=False)

main('test_merged_3.csv','dysfluencytest.csv', 'trigram_pos_test.csv', 'bowtest.csv')