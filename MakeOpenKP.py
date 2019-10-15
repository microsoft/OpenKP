from random import shuffle
import json
testUrls = []
preds = 'preds'
docs = 'OpenKPDocs.tsv'
with open(preds,'r') as f:
    for l in f:
        l = l.strip().split('\t')
        testUrls.append(l[0])

allUrls = []
with open(docs,'r') as f:
    for l in f:
        l = l.strip().split('\t')
        allUrls.append(l[0])

testSet = set(testUrls)
allSet = set(allUrls)
excludeTest = testSet - allSet
testUrls = list(testSet - excludeTest)
trainUrls = list(allSet - testSet)
print("There are {} unique urls with {} in the dev set".format(len(allSet), len(testSet)))
shuffle(trainUrls)
shuffle(testUrls)
index = int(len(testUrls)/2) -1
devUrls = testUrls[:index]
evalUrls = testUrls[index:]

with open('trainURLs.tsv','w') as w:
    for url in trainUrls:
        w.write("{}\n".format(url))

with open('devURLs.tsv','w') as w:
    for url in devUrls:
        w.write("{}\n".format(url))

with open('evalURLs.tsv','w') as w:
    for url in evalUrls:
        w.write("{}\n".format(url))

#URL\tCleanBody Tokes\tVDOM\tAllPropertyIDX\tQueries that clicked\tKP_DL
with open(docs,'r') as f:
    with open('OpenKPFull.jsonl','w') as w:
        with open('OpenKPTrain.jsonl','w') as train:
            with open('OpenKPDev.jsonl','w') as dev:
                with open('OpenKPEval.jsonl','w') as test:
                    for l in f:
                        l = l.strip().split('\t')
                        url = l[0]
                        text = l[1]
                        visual = l[2]
                        kp = json.loads(l[4])
                        for i in kp:
                            if len(i) == 0:
                                kp.pop
                        data = {}
                        data['url'] = url
                        data['text'] = text 
                        data['VDOM'] = visual
                        data['KeyPhrases'] = kp
                        output = "{}\n".format(json.dumps(data))
                        if url in allUrls:
                            w.write(output)
                        if url in trainUrls:
                            train.write(output)
                        if url in devUrls:
                            dev.write(output)
                        if url in evalUrls:
                            test.write(output)                       



