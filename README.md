# ML-predicting-emotional-category


Generating the feature files:
	Trigram/POS Feature Set: python nltk_parsing.py
        NOTE: have to change the input csv from test to train and the output file from test to train depending on what you’re trying to generate
	Vectorized Unigram Feature Set: python bog_generator.py
	NOTE: have to change the input csv from test to train and the output file from test to train depending on what you’re trying to generate
	Dysfluency Feature Set: python dysfluency.py
	NOTE: have to change the input csv from test to train and the output file from test to train depending on what you’re trying to generate

Aligning Features for Train and Test (i.e. column matching)
	Train Alignment: python train_merger.py
	NOTE: have to change the input csvs in main and the output csv depending on how many input training files there are
	Test Alignment: python test_merger.py
	NOTE: have to change the input csvs in main and the output csv depending on how many input testing files there are

Classifiers
	1. MLP Classifier: python classifier.py, reports overall accuracy and confusion matrix
	2. 	RandomForest Classifier: python classifer_randomforest.py, reports overall accuracy

Feature Analysis and Hypothesis
	1. Dysfluency Analysis: python dysfluency_analysis.py
	2.	Trigram/POS Analysis: python trigram_analysis.py
        3. Vectorized Unigram Analysis: python bow_analysis.py
NOTE: These values were then pasted into an excel spreadsheet, saved as hypothesis_analysis.xlsx with the bar charts and values for each of the above sets
