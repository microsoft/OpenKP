import sys
import json
import re
import string
import numpy as np

def normalize_answer(s):
    def remove_articles(text):
        return re.sub(r'\b(a|an|the)\b', ' ', text)
    def white_space_fix(text):
        return ' '.join(text.split())
    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)
    def lower(text):
        return text.lower()
    return [white_space_fix(remove_articles(remove_punc(lower(x)))) for x in s]
    
def get_precision_score(candidate, reference):
    scoring, best_match = {}, {}
    max_score, max_label =  0,''
    set_candidate, set_reference = [], []
    for candidate_label in candidate:
        set_candidate.append(set(candidate_label))
    for reference_label in reference:
        set_reference.append(set(reference_label))
    for reference_label in set_reference:
        reference_key = str(reference_label)
        scoring[reference_key] = {}
        for candidate_label in set_candidate:
            candidate_key = str(candidate_label)
            scoring[reference_key][candidate_key] = (len(reference_label) - len(reference_label-candidate_label))/len(reference_label)
    while len(scoring) > 0:
        max_score = 0
        max_label = ''
        for reference_label in scoring:
            reference_key = str(reference_label)
            for candidate_label in scoring[reference_key]:
                candidate_key = str(candidate_label)
                score = scoring[reference_key][candidate_key]
                if score >= max_score:
                    max_score = score
                    max_label = (reference_key, candidate_key)
        best_match[max_label] = scoring[max_label[0]][max_label[1]]
        scoring.pop(max_label[0])
    return sum(best_match.values())/len(reference)     
     
def get_recall_score(candidate, reference):
    scoring, best_match = {}, {}
    max_score, max_label =  0,''
    set_candidate, set_reference = [], []
    for candidate_label in candidate:
        set_candidate.append(set(candidate_label))
    for reference_label in reference:
        set_reference.append(set(reference_label))
    for reference_label in set_reference:
        reference_key = str(reference_label)
        scoring[reference_key] = {}
        for candidate_label in set_candidate:
            candidate_key = str(candidate_label)
            scoring[reference_key][candidate_key] = (len(reference_label) - len(reference_label-candidate_label))/len(candidate_label)
    while len(scoring) > 0:
        max_score = 0
        max_label = ''
        for reference_label in scoring:
            reference_key = str(reference_label)
            for candidate_label in scoring[reference_key]:
                candidate_key = str(candidate_label)
                score = scoring[reference_key][candidate_key]
                if score >= max_score:
                    max_score = score
                    max_label = (reference_key, candidate_key)
        best_match[max_label] = scoring[max_label[0]][max_label[1]]
        scoring.pop(max_label[0])
    return sum(best_match.values())/len(reference)

def getScoreEM(candidate, reference):
    scoring, best_match = {}, {}
    max_score, max_label = 0 , ''
    for reference_label in reference:
        reference_key = str(reference_label)
        scoring[reference_key] = {}
        for candidate_label in candidate:
            candidate_key = str(candidate_label)
            if reference_label == candidate_label:
                scoring[reference_key][candidate_key] = 1
            else:
                scoring[reference_key][candidate_key] = 0
    while len(scoring) > 0:
        max_score = -1
        max_label = ''
        for reference_label in scoring:
            reference_key = str(reference_label)
            for candidate_label in scoring[reference_key]:
                candidate_key = str(candidate_label)
                score = scoring[reference_key][candidate_key]
                if score >= max_score:
                    max_score = score
                    max_label = (reference_key, candidate_key)
        best_match[max_label] = scoring[max_label[0]][max_label[1]]
        scoring.pop(max_label[0])
    return sum(best_match.values())/len(reference) 

def remove_empty(a_list):
    new_list = []
    for i in a_list:
        if len(i) > 0:
            if len(i[0]) >0:
                new_list.append(i)   
    return new_list

def evaluate(candidate, reference):
    em_scores = []
    f1_scores = []
    for url in reference:
        candidate_KP = remove_empty(candidate[url]['KeyPhrases'])
        reference_KP = remove_empty(reference[url]['KeyPhrases'])
        em = getScoreEM(candidate_KP, reference_KP)
        em_scores.append(em)
        recall =  get_recall_score(candidate_KP, reference_KP)
        precision = get_precision_score(candidate_KP, reference_KP)
        if precision == 0 or recall == 0:
            f1= 0
        else:
            f1 = 2 * ((precision * recall) / (precision + recall))
        f1_scores.append(f1)
    print("########################\nMetrics\nExact Match Score:{}\nF1 Score:{}\n##################".format(np.mean(em_scores),np.mean(f1_scores)))    

def files_are_good(candidate, reference):
    referenceURLs = set(reference.keys())
    candidateURLs = set(candidate.keys())
    if len((referenceURLs - candidateURLs)) > 0:
        print("ERROR:Candidate File is missing URLS present in reference file\nMissing urls:{}".format(referenceURLs-candidateURLs))
        return False 
    if len((candidateURLs - referenceURLs)) > 0:
        print("ERROR:Candidate File includes URLS not present in reference file\nUnexpected urls:{}".format(candidateURLs-referenceURLs))
        return False 
    return True

def load_file(filename):
    data = {}
    with open(filename,'r') as f:
        for l in f:
            item = json.loads(l)
            data[item['url']] = item
    return data 

def main(candidate_filename, reference_filename):
    candidate = load_file(candidate_filename)
    reference = load_file(reference_filename)
    if files_are_good(candidate, reference) == True:
        print(evaluate(candidate, reference))
        exit(0)
    else:
        print("Candidate file and Reference are not comparable. Please verify your candidate file.")
        exit(-1)
        
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage:evaluate.py <candidate file> <reference file>")
        exit(-1)
    else:
        main(sys.argv[1], sys.argv[2])