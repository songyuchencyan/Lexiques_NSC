import os
import re
from conllu import *
import pandas as pd
import numpy as np
from collections import Counter


def get_lexique_maju_mini(lexique): 
    ''' Standardize the capitalization of words, with only PROPN capitalized '''
    lexique_maju_mini = list()
    for terme in lexique:
        if terme[1]=='PROPN':
            terme[0] = terme[0].capitalize()
            lexique_maju_mini.append(terme)
        else:
            terme[0] = terme[0].lower()
            lexique_maju_mini.append(terme)
    return lexique_maju_mini

###### Read lexique file and get word list with standardized capitalization ######
with open('Final_Complete_Gold_Lexicon_BC_for_Yuchen_26.02.2020.txt', 'r') as f:
    lexique = f.readlines()
lexique = [x.strip('\n').split('\t') for x in lexique]
lexique = get_lexique_maju_mini(lexique)
###### Read lexique file and get word list with standardized capitalization ######

###### Get different morph info combination lists ######
lexique_form = [x[0].lower() for x in lexique]
lexique_form_pos = [[x[0].lower(), x[1]] for x in lexique]
lexique_form_pos_trait = [[x[0].lower(), x[1], sorted(x[2].split('|'))] for x in lexique]
lexique_form_pos_trait_lemme_glose = [[x[0].lower(), x[1], sorted(x[2].split('|')), x[3], x[4]] for x in lexique]
###### Get different morph info combination lists ######

def get_lexique_ambigu(lexique_form, lexique_form_pos):
    ''' List of words with multiple POS '''
    count = dict(Counter(lexique_form))
    form_ambigu = [key for key, value in count.items() if value>1]
    lexique_ambigu = list()
    for form in form_ambigu:
        for form_pos in lexique_form_pos:
            if form in form_pos:
                lexique_ambigu.append(form_pos)
    return form_ambigu
lexique_ambigu = get_lexique_ambigu(lexique_form, lexique_form_pos)

###### Read conll file and get list of sentences with conll format ######
with open('Correction_80_conll_ref_add.conllu', 'r', encoding='UTF-8') as f:
    conll = f.read()
conll = parse(conll)
###### Read conll file and get list of sentences with conll format ######

###### Files to write ######
f = open('GLOSE_LEMME_Correction_80_conll_ref_add.conllu', 'w', encoding='UTF-8')
###### Files to write ######

###### Start writing lemma and gloss ######
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
                    lemme = token[3]
                    glose = line[9]+'|'+token[4]
                    line[2] = lemme
                    line[9] = glose
            one_line = '\t'.join(line)
            f.write(one_line+'\n')
    f.write('\n')
###### Start writing lemma and gloss ######
f.close()
