import csv
import pandas as pd
master_features = set()
def main(training_file, testing_file):
	train_file = open(training_file) 
	pd_train_file = pd.read_csv(training_file)
	train_reader = csv.DictReader(train_file)
	test_file = open(testing_file)
	pd_test_file = pd.read_csv(testing_file)
	test_reader = csv.DictReader(test_file)

	training_features = list(pd.read_csv(training_file, nrows=1).columns)
	testing_features = list(pd.read_csv(testing_file, nrows=1).columns)

	for elem in training_features:
		master_features.add(elem)
	
	for elem in testing_features:
		master_features.add(elem)

	train_columns_added = master_features - set(training_features)
	test_columns_added = master_features - set(testing_features)


	for elem in train_columns_added:
		pd_train_file[elem] = '0'
	pd_train_file.to_csv('train_merged_2.csv', index=False)


	for elem in test_columns_added:
		pd_test_file[elem] = '0'
	pd_test_file.to_csv('test_merged_2.csv', index=False)

	# updated_train_file = open('train_merged_2.csv')
	# updated_train_reader = csv.DictReader(updated_train_file)
	# updated_test_file = open('test_merged_2.csv')
	# updated_test_reader = csv.DictReader(updated_test_file)


	# with open('train_merged_3.csv', mode='w') as train:
	# 	train_writer = csv.writer(train, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	# 	train_writer.writerow(training_features)
	# 	for row in updated_train_reader:
	# 		if row['act_tag'] in ['sd', 'b', 'sv', 'aa', '%', 'ba', 'qy', 'x', 'ny', 'fc']:
	# 			new_row = list()
	# 			for elem in row:
	# 				new_row.append(row[elem])
	# 			train_writer.writerow(new_row)


	# with open('test_merged_3.csv', mode='w') as test:
	# 	test_writer = csv.writer(test, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
	# 	test_writer.writerow(testing_features)
	# 	for row in updated_test_reader:
	# 		if row['act_tag'] in ['sd', 'b', 'sv', 'aa', '%', 'ba', 'qy', 'x', 'ny', 'fc']:
	# 			new_row = list()
	# 			for elem in row:
	# 				new_row.append(row[elem])
	# 			test_writer.writerow(new_row)

main('train_merged.csv', 'test_merged.csv')