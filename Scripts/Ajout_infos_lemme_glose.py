import os
import re
from conllu import *
import pandas as pd
import numpy as np
from collections import Counter


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
lexique_form_pos_trait_lemme_glose = [[x[0].lower(), x[1], sorted(x[2].split('|')), x[3], x[4]] for x in lexique]

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






# with open('80_conll_ref_add.conllu', 'r', encoding='UTF-8') as f:
#     conll = f.read()
conll = parse(conll)

f = open('80_conll_ref_add.conllu', 'w', encoding='UTF-8')
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
            for token in lexique_form_pos_trait_lemme_glose:
                if token[0:3] == conll_form_pos_trait:
                    lemme = token[4]
                    glose = line[9].split('|')[0]+'|'+line[9].split('|')[1]+'|'+token[5]
                    line[2] = lemme
                    line[9] = glose
            one_line = '\t'.join(line)
            f.write(one_line+'\n')
    f.write('\n')
f.close()
