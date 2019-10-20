import csv
import nltk

def main():
    #read from train
    file = open('train_merged.csv') 
    reader = csv.DictReader(file)
    master_dict = dict()
    #write to dysfluencies csv
    with open('dysfluencytrain.csv', mode='w') as dysfluency_file:
        dysfluency_writer = csv.writer(dysfluency_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        print("file opened")
        for row in reader:
            if row['act_tag'] not in ['sd', 'b', 'sv', 'aa', '%', 'ba', 'qy', 'x', 'ny', 'fc']:  #checks for top 10 tags
                continue
            old_text = row['text']
            text, nonsen_count, restart_counts, complete = parse(old_text)
            text, bg_noise_count = detect_bg_noise(text)
            for elem in bg_noise_count.keys():
                if elem not in master_dict.keys():
                    master_dict[elem] = 1
                else:
                    master_dict[elem] += 1
        original_headers = ['swda_filename', 'transcript index', 'act_tag', 'original text', 'cleaned text', 'A', 'C', 'D', 'E', 'F', 'restarts w/ repair', 'restarts w/repair and non-sentence elements', 'restarts w/o repairs', 'complete', 'incomplete', 'overlap']
        thresholded_master_list = [x for x in master_dict.keys() if master_dict[x] > 6]
        original_headers.extend(thresholded_master_list)
        dysfluency_writer.writerow(original_headers)

        print("headers written")
        file = open('train_merged.csv') 
        new_reader = csv.DictReader(file)
        for row in new_reader:
            if row['act_tag'] not in ['sd', 'b', 'sv', 'aa', '%', 'ba', 'qy', 'x', 'ny', 'fc']:  #checks for top 10 tags
                continue

            old_text = row['text']
            text, nonsen_count, restart_counts, complete, bg_noise_count = parse(old_text)
            act_tag = row['act_tag']
            swda_filename = row['swda_filename']
            swda_transcript_index = row['transcript_index']
            A = str(nonsen_count[0])
            C = str(nonsen_count[1])
            D = str(nonsen_count[2])
            E = str(nonsen_count[3])
            F = str(nonsen_count[4])
            restarts_0 = str(restart_counts[0])
            restarts_1 = str(restart_counts[1])
            restarts_2 = str(restart_counts[2])
            if complete == True:
                complete_true = '1'
                complete_false = '0'
                overlap = '0'
            elif complete == False:
                complete_true = '0'
                complete_false = '1'
                overlap = '0'
            else:
                complete_true = '0'
                complete_false = '1'
                overlap = '1'
            sound_per_row = list()
            for sound in thresholded_master_list:
                if sound in bg_noise_count.keys():
                    sound_per_row.append('1')
                else:
                    sound_per_row.append('0') 
            current_row = [swda_filename, swda_transcript_index, act_tag, old_text, text, A, C, D, E, F, restarts_0, restarts_1, restarts_2, complete_true, complete_false, overlap]
            current_row.extend(sound_per_row)

            dysfluency_writer.writerow(current_row)

        print("file generated")

def parse(text):
    output = list()
    strip_garbage(text)
    text, rcount = r(text) #saved in other file
    text, complete = completeness(text)
    text.strip()
    output = list()
    for elem in ['A', 'C', 'D', 'E', 'F']: 
        text, count = clean_alphabet(text, elem)
        output.append(count)
    return text, output, rcount, complete, bg_noise_count


def strip_garbage(text):
    if '#' in text:
        text = text.replace('#', '')
    if '((' in text:
        text = text.replace('((', '')
    if '))' in text:
        text = text.replace('))', '')
    if '<<' in text:
        text = text.replace('<<', '<')
    if '>>' in text:
        text = text.replace('>>', '>')

    return text

def clean_alphabet(text, alphabet):
    char_starter = '{' + alphabet + ' '
    count = 0
    while char_starter in text:
        if text.find(char_starter) == -1:
            begin = text.find(char_starter)
            end = text.index(' }', begin)
            text = text[:begin] + text[end+2:]
        else:
            text = text[:begin]
        count += 1
    return text, count

def detect_bg_noise(text):
    bg_noise_count = dict()
    while '<' in text: 
        begin = text.find('<')
        if text.find('>', begin) == -1:
            text = text.replace('<', '')
        else:
            end = text.find('>',begin)
            background_noise = text[begin+1:end]
            if background_noise.lower() not in bg_noise_count.keys():
                bg_noise_count[background_noise.lower()] = 1
            else:
                bg_noise_count[background_noise.lower()] += 1

            text = text[:begin] + text[end+1:]
    return text, bg_noise_count 

def completeness(text):
    if text[-2:] == '-/':
        output = text[:-2]
        return output, False
    elif text[-3:] == '- /':
        output = text[:-3]
        return output, False
    elif text[-1:] == '/':
        output = text[:-1]
        return output, True
    return text, None

main()