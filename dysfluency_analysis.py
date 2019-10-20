import csv


def main():
	act_tag_count = dict()
	file = open('dysfluencytrain.csv')
	reader = csv.DictReader(file)
	feature_analysis = dict()
	for dialogue_act in ['sd', 'b', 'sv', 'aa', '%', 'ba', 'qy', 'x', 'ny', 'fc']:
			feature_analysis[dialogue_act] = 0
	for row in reader:
		if row['act_tag'] not in act_tag_count:
			act_tag_count[row['act_tag']] = 0
		else:
			act_tag_count[row['act_tag']] += 1
	file = open('dysfluencytrain.csv')
	reader = csv.DictReader(file)
	for row in reader: 
		for dialogue_act in ['sd', 'b', 'sv', 'aa', '%', 'ba', 'qy', 'x', 'ny', 'fc']:
			if row['act_tag'] == dialogue_act:
				feature_analysis[dialogue_act] += int(row['incomplete'])/act_tag_count[row['act_tag']]*100
			else:
				continue
	print(feature_analysis)


main()