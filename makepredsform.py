import json
with open('data/kp80k_blingkpe.tsv','r') as f:
    with open('data/kp80k_blingkpe.json','w') as w:
        for l in f:
            l = l.strip().split('\t')
            data = {}
            data['url'] = l[0]
            kp = []
            for i in l[6:9]:
                kp.append(i.split(' '))
            data['KeyPhrases'] = kp
            w.write("{}\n".format(json.dumps(data)))

with open('data/kp80k_blingkpe_finetune.tsv','r') as f:
    with open('data/kp80k_blingkpe_finetune.json','w') as w:
        for l in f:
            l = l.strip().split('\t')
            data = {}
            data['url'] = l[0]
            kp = []
            for i in l[6:9]:
                kp.append(i.split(' '))
            data['KeyPhrases'] = kp
            w.write("{}\n".format(json.dumps(data)))
