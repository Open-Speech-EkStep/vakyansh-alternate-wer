from operator import sub
import untangle
import collections
import pandas as pd

folder_name = ""

def substitutions_deletions(sgml_file):
    obj = untangle.parse(sgml_file)
    substitutions = collections.defaultdict(int) 
    deletions = collections.defaultdict(int)
    insertions = collections.defaultdict(int)

    for sent in obj.SYSTEM.SPEAKER.PATH:
        report = sent.cdata.strip().split(':')
        for tag in report:
            if tag[0]=="S":
                substitutions[tag.split(',')[1]] += 1
            elif tag[0]=="I":
                insertions[tag.split(',')[2]] += 1
            elif tag[0]=="D":
                deletions[tag.split(',')[1]] += 1
            
    print(f'Total number of substtutions: {sum(substitutions.values())}')
    print(f'Total number of insertions: {sum(insertions.values())}')
    print(f'Total number of deletions: {sum(deletions.values())}')

    subs_df = pd.DataFrame(data = {'words': list(substitutions.keys()), 'frequency': list(substitutions.values())})
    del_df = pd.DataFrame(data = {'words': list(deletions.keys()), 'frequency': list(deletions.values())})
    ins_df = pd.DataFrame(data = {'words': list(insertions.keys()), 'frequency': list(insertions.values())})

    subs_df.to_csv(folder+'substitutions.csv', index=None)
    del_df.to_csv(folder+'deletions.csv', index=None)
    ins_df.to_csv(folder+'insertions.csv', index=None)

if __name__ == "__main__":
    substitutions_deletions(folder+'hypo.word-checkpoint_best.pt-test.txt.sgml')
