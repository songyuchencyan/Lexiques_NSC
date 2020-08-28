import os
import re
from conllu import *
import pandas as pd
import numpy as np
from collections import Counter

# rep = 'E:/TAL/Stage/M2_S1/not-to-release'
# file_name = list()
# for file in os.listdir(rep):
#     file = file.replace('.conllu', '')
#     file_name.append(file)
# file_name.sort()

# f = open('corpus_concat_conllu_CorrigéBC_2019.12.01.txt', 'r')
# content = f.read()
# f.close()

# content = content.split('\n\n')
# for filename in file_name:
#     print(filename)
#     f = open('Corpus/'+filename+'.conllu', 'w')
#     all_sentences = ''
#     for sentence in content:
#         if filename in sentence:
#             all_sentences = all_sentences + sentence + '\n\n'
#     all_sentences = all_sentences.strip('\n')
#     all_sentences = all_sentences + '\n'
#     f.write(all_sentences)
#     f.close()


# df = pd.read_table('Complete_lexique_leipzig_BC_2019.12.01.txt', sep="\t", encoding="utf-8", names=['NUMBER', 'FORM', 'POS', 'TRAIT', 'LEMMA', 'GLOSE'])
# df_form = df['FORM'].tolist()
# df_pos = df['POS'].tolist()

# form_pos = list(zip(df_form, df_pos))
# # print(df[(df['NUMBER']=='_')&(df['FORM']=='nan')])

# f = open('corpus_concat_conllu_CorrigéBC_2019.12.01.txt', 'r')
# content = f.read()
# f.close()

# conll = parse(content)
# n=0
# l=[]
# for sentence in conll:
#     for word in sentence:
#         # if word['form'] not in df_form:
#         #     print(word['form'])
#         word_form_pos = (word['form'], word['upostag'])
#         if word_form_pos not in form_pos:
#             df_w = df[df['FORM']==word['form']]['FORM'].tolist()
#             if len(df_w) != 1:
#                 if df_w not in l:
#                     l.append(df_w)
#                 n=n+1

def get_lexique_maju_mini(lexique): # 整理词典大小写，仅PROPN保留大写
    lexique_maju_mini = list()
    for terme in lexique:
        if terme[1]=='PROPN':
            terme[0] = terme[0].capitalize()
            lexique_maju_mini.append(terme)
        else:
            terme[0] = terme[0].lower()
            lexique_maju_mini.append(terme)
    return lexique_maju_mini

with open('Final_Complete_Gold_Lexicon_BC_for_Yuchen_26.02.2020.txt', 'r') as f:
    lexique = f.readlines()
lexique = [x.strip('\n').split('\t') for x in lexique]
lexique = get_lexique_maju_mini(lexique)

lexique_form = [x[0].lower() for x in lexique]
lexique_form_pos = [[x[0].lower(), x[1]] for x in lexique]
lexique_form_pos_trait = [[x[0].lower(), x[1], sorted(x[2].split('|'))] for x in lexique]

def get_lexique_ambigu(lexique_form, lexique_form_pos):
    count = dict(Counter(lexique_form))
    form_ambigu = [key for key, value in count.items() if value>1]
    lexique_ambigu = list()
    for form in form_ambigu:
        for form_pos in lexique_form_pos:
            if form in form_pos:
                lexique_ambigu.append(form_pos)
    return form_ambigu
lexique_ambigu = get_lexique_ambigu(lexique_form, lexique_form_pos)






with open('80_conll_ref_add.conllu', 'r', encoding='UTF-8') as f:
    conll = f.read()
conll = parse(conll)

f = open('80_conll_ref_add.conllu', 'w', encoding='UTF-8')
f_ambigu = open('cas_ambigu.txt', 'a')
for sentence in conll:
    sentence = sentence.serialize().strip('\n').split('\n')
    for one_line in sentence:
        if one_line[0]=='#':
            f.write(one_line+'\n')
        else:
            line = one_line.split('\t') # ['23', '>+', '_', 'PUNCT', '_', '_', '26', 'punct', '_', 'startali=283829|endali=283859']
            conll_form = line[1].lower()
            conll_form_pos = [line[1].lower(), line[3]]
            conll_form_pos_trait = [line[1].lower(), line[3], sorted(line[5].split('|'))]
            if conll_form in lexique_form:
                if conll_form_pos in lexique_form_pos:
                    if conll_form_pos_trait in lexique_form_pos_trait:
                        f.write(one_line+'\n')
                    else:
                        for x in lexique_form_pos_trait:
                            if conll_form_pos==[x[0],x[1]]:
                                line[5] = '|'.join(x[2])
                        one_line = '\t'.join(line)
                        f.write(one_line+'\n')
                else:
                    if conll_form not in lexique_ambigu:
                        for x in lexique_form_pos_trait:
                            if conll_form==x[0]:
                                line[3] = x[1]
                                line[5] = '|'.join(x[2])
                        one_line = '\t'.join(line)
                        f.write(one_line+'\n')
                    else:
                        f.write(one_line+'\n')
                        f_ambigu.write('# erreur_ambigu = '+one_line+'\n'+'\n'.join(sentence)+'\n\n')
            else:
                print(one_line)
                f.write(one_line+'\n')
    f.write('\n')
f.close()
f_ambigu.close()