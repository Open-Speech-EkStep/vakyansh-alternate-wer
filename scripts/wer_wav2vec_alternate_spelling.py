import pandas as pd
import numpy as np
import glob
import Levenshtein as Lev
from tqdm import tqdm
import swifter
import argparse
from components import compute_wer
import numpy
import re

def replace_index(s, index, new_word):
    
    s_list= s.split(" ")
    s_list[index] = new_word
    return " ".join(s_list)

def get_new_sentences(org_sent, index_of_alternate_splellings, word_pairs_list):
    modified_sent = re.sub("[\\[].*?[\\]]", "*", org_sent)

    sent_list = []
    for pair in  word_pairs_list:
        final_sent = modified_sent
        for ind in range(len(pair)):

            final_sent = replace_index(final_sent, index_of_alternate_splellings[ind], pair[ind])
        sent_list.append(final_sent)
    return sent_list
        
def calc_min_wer_from_multiple_sent(org, pred):
    if "[" in org:
        
        org = org.replace('[', '').replace(']', '')
        sent_words = org.split(' ')
        
        index_of_alternate_splellings = [i for i, w in enumerate(sent_words) if '/' in w]
        word_pairs = [w for i, w in enumerate(sent_words) if i in index_of_alternate_splellings]
        word_pairs_list = [[w.split('/')[0],w.split('/')[1]] for w in word_pairs]
        combinations = [list(x) for x in numpy.array(numpy.meshgrid(*word_pairs_list)).T.reshape(-1,len(word_pairs_list))]   
        new_sentences = get_new_sentences(org,index_of_alternate_splellings,combinations)
        
        wers = [wer(pred, line) for line in new_sentences ] 
#         cers = [cer(pred, line) for line in new_sentences ]
        min_wer = min(wers)
        #min WER sentence
        best_org = new_sentences[ wers.index(min_wer)]
        return best_org

    else:
        return org


def wer( s1, s2):
        """
        Computes the Word Error Rate, defined as the edit distance between the
        two provided sentences after tokenizing to words.
        Arguments:
            s1 (string): space-separated sentence
            s2 (string): space-separated sentence
        """

        # build mapping of words to integers
        b = set(s1.split() + s2.split())
        word2char = dict(zip(b, range(len(b))))

        # map the words to a char array (Levenshtein packages only accepts
        # strings)
        w1 = [chr(word2char[w]) for w in s1.split()]
        w2 = [chr(word2char[w]) for w in s2.split()]

        return Lev.distance(''.join(w1), ''.join(w2))

def cer(s1, s2):
    """
    Computes the Character Error Rate, defined as the edit distance.
    Arguments:
        s1 (string): space-separated sentence
        s2 (string): space-separated sentence
    """
    s1, s2, = s1.replace(' ', ''), s2.replace(' ', '')
    return Lev.distance(s1, s2)

def clean_text(row):
    return row[0][0:row.ind]

def preprocess(original_csv):
    original_csv['ind'] = original_csv['text'].str.index('(None')
    original_csv['cleaned_text'] = original_csv.swifter.apply(clean_text, axis = 1)
    return original_csv



def calculate_wer(row ):
    org = row['original']
    pred = row['predicted']

#     org = create_alternate_spellings(org, word_and_char_replacement_dict)


    wer_local = ''
    try:
        wer_local = wer(org,pred)
        #cer_local = cer(row['cleaned_text'], row['text_y'])
    except:
        print(row)
        return len(org.split(' '))
    return wer_local


def calculate_cer(row):
    org = row['original']
    pred = row['predicted']
#     org = create_alternate_spellings(org, word_and_char_replacement_dict,for_cer = True)

    try:
        cer_local = cer(org, pred)
    except:
        return len(org.str.replace(' ','').str.len())
    return cer_local


def run_pipeline(ground_truth, predicted, alt_spelling = False):



    with open(ground_truth, encoding='utf-8') as file:
        original_csv = file.readlines()

    original_csv = [line.strip() for line in original_csv]
    original_csv = pd.DataFrame(original_csv, columns=['text'])

    with open(predicted) as file:
        predicted_csv = file.readlines()

    print(len(original_csv)," ", len(predicted_csv))
    predicted_csv = [line.strip() for line in predicted_csv]
    predicted_csv = pd.DataFrame(predicted_csv, columns=['text'])

    original_csv['ix'] = original_csv['text'].str.split(' \(None-').str[-1].str[0:-1].astype('int')
    predicted_csv['ix'] = predicted_csv['text'].str.split('\(None').str[-1].str[1:-1].astype('int')
    original_csv = preprocess(original_csv)
    predicted_csv = preprocess(predicted_csv)


    #df_merged = pd.DataFrame(data = [original_csv.cleaned_text.values, predicted_csv.cleaned_text.values],index=None)
    #df_merged = df_merged.transpose()

    df_merged = pd.merge(original_csv,predicted_csv, on='ix')
    df_merged = df_merged[['cleaned_text_x', 'cleaned_text_y', 'ix']]
    df_merged.columns = ['original', 'predicted','ix']
    if alt_spelling is True:
        new_org = []
        for o,p in zip(df_merged['original'], df_merged['predicted']):
            new_org.append(calc_min_wer_from_multiple_sent(o,p))
        df_merged["original"] = new_org


    df_merged['wer'] = df_merged.apply(calculate_wer,  axis = 1)
    df_merged['cer'] = df_merged.swifter.apply(calculate_cer, axis = 1)
    df_merged['num_tokens'] = df_merged['original'].str.split().str.len()
    df_merged['num_chars'] = df_merged['original'].str.replace(' ','').str.len()

    df_merged.sort_values(by = 'wer', ascending=False)
    fwer = df_merged.wer.sum() / df_merged.num_tokens.sum()
    fcer = df_merged.cer.sum() / df_merged.num_chars.sum()
    print('WER: ', fwer*100)
    print('CER: ', fcer*100)
    return df_merged

def merge_with_tsv(df, tsv):
    tsv_file = pd.read_csv(tsv, delimiter='\t',header=None, skiprows=1)
    tsv_file_2 = pd.read_csv(tsv)
    header = tsv_file_2.columns[0] + '/'
    tsv = tsv_file#.iloc[1:]
    df['path'] = df['ix'].apply(lambda x: tsv.iloc[x,0])
    df['path'] = header + df['path'].astype('str')
    return df

def calculate_errors(row):
    ret_object = compute_wer(predictions=[row['predicted']], references=[row['original']])
    return [ret_object['substitutions'], ret_object['insertions'], ret_object['deletions']]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process CER pipeline')
    parser.add_argument('-o', '--original', required=True, help='Original File')
    parser.add_argument('-p', '--predicted', required=True, help='Predicted File')
    parser.add_argument('-s', '--save-output', help='save output file', type=bool)
    parser.add_argument('-n', '--name', help='save output file name', type=str)
    parser.add_argument('-t','--tsv', type=str)
    parser.add_argument('-e', '--sid', type=bool)
    parser.add_argument('-a', '--alt-spelling',default=False,type=bool, help = "Alternane spelling T or F")


    args_local = parser.parse_args()

    df = run_pipeline(args_local.original, args_local.predicted, args_local.alt_spelling)
    
    if args_local.tsv:
        df=merge_with_tsv(df, args_local.tsv)

    if args_local.sid:
        ret_object= df.swifter.apply(calculate_errors, axis=1)
        df['errors'] = ret_object
        df_errors = pd.DataFrame(df['errors'].to_list(), columns=['substitutions','insertions', 'deletions'])
        df = pd.concat([df, df_errors], axis=1)
        df = df.drop(columns=['errors'])

    
    if args_local.save_output:
        df.to_csv(args_local.name, index=False)



