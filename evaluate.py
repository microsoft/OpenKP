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
    return ' '.join([white_space_fix(remove_articles(remove_punc(lower(x)))) for x in s])

def remove_empty(a_list):
    new_list = []
    for i in a_list:
        if len(i) > 0:
            if len(i[0]) >0:
                new_list.append(normalize_answer(i))   
    return new_list

def get_score(candidates, references):
    fp, tp, fn = 0,0,0
    candidate_set = set(candidates)
    reference_set = set(references)
    for i in references:
        if i in candidate_set:
            tp += 1
        else:
            fn += 1
    for i in candidates:
        if i not in reference_set:
            fp += 1
    p = tp /(tp+fp)
    r = tp /(tp+fn)
    return p, r
        
def evaluate(candidates, references, urls):
    precision_scores, recall_scores = {1:[], 3:[], 5:[]}, {1:[], 3:[], 5:[]}
    for url in urls:
        candidate = remove_empty(candidates[url]['KeyPhrases'])
        reference = remove_empty(references[url]['KeyPhrases'])
        for i in [1,3,5]:
            p, r = get_score(candidate, reference[:i]) 
            precision_scores[i].append(p)
            recall_scores[i].append(r)
    print("########################\nMetrics")
    for i in precision_scores:
        print("@{}".format(i))
        print("P:{}".format(np.mean(precision_scores[i])))
        print("R:{}".format(np.mean(recall_scores[i])))
    print("#########################")

def files_are_good(candidate, reference):
    referenceURLs = set(reference.keys())
    candidateURLs = set(candidate.keys())
    return True
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
        candidate_urls = set(candidate.keys())
        reference_urls = set(reference.keys())
        urls = reference_urls.intersection(candidate_urls)
        evaluate(candidate, reference, urls)
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
