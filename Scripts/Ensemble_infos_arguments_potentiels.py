#!/usr/bin/env python  
# -*- coding: UTF-8 -*- 

import os
import re
from conllu import *
from conllnaija import *

# {'id': 16, 't': 'sure', 'lemma': 'sure', 'tag': 'ADJ', 'xpos': '_', 'gov': {0: 'root'}, 'egov': {}, 'misc': 'AlignBegin=384370|AlignEnd=384490|Gloss=sure', 'kids': {1: 'mod:periph', 4: 'punct', 6: 'dislocated', 13: 'punct', 14: 'subj', 15: 'mod', 17: 'comp:obj', 30: 'punct'}}


def find_subj(tree, index):
    node = tree[index]
    while True:
        if 'subj' in node['kids'].values() or 'subj@expl' in node['kids'].values():
            subj = [i for i,f in node['kids'].items() if f=='subj@expl' or f=='subj'][0]
            return subj
            break
        elif 'comp:aux' in node['gov'].values():
            index = [i for i,deprel in node['gov'].items() if deprel=='comp:aux'][0]
            subj = find_subj(tree, index)
            return subj
            break
        else:
            return "None"

def find_gov(token):
    gov_id = list(token['gov'].keys())[0]
    if gov_id==0:
        gov='gov=root\t_\t_'
    else:
        gov='gov='+list(token['gov'].values())[0]+'\t'+tree[gov_id]['tag']+'\t'+tree[gov_id]['lemma']
    return gov


f = open('dic_souscat_fullinfo.tsv', 'w') # Insérer le chemin absolu du fichier qui enregistre des ensembles d'informations extraits
trees = conllFile2trees('80_corpus_old.conllu')  # Insérer le chemin absolu du fichier CONLL-U, la fonction "conllFile2trees" permet de convertit un arbre CONLL-U des chaîne de caractères en dictionnaire 
for tree in trees:
    exemple = re.findall('text: (.+)\n', str(tree))[0]
    tree.addkids()  # 把子关系添加到tree / add kid relation to tree
    for i in tree:
        token = tree[i] 
        index = token['id']
        form = token['t']
        pos = token['tag']
        lemma = token['lemma']  
        gov = find_gov(token)

        ##### FIND SUBJ ##### 
        if pos=='VERB' or pos=='AUX' or pos=='ADJ':   
            subj_id = find_subj(tree, index)
            if subj_id!='None':
                subj = 'subj'+'\t'+tree[subj_id]['tag']+'\t'+tree[subj_id]['lemma']
            else:
                subj='_\t_\t_'
        else:
                subj='_\t_\t_'
        ##### FIND SUBJ #####

        ##### WRITE INFOS IN DICT #####
        f.write('LEMMA&POS:\t'+lemma+'\t'+pos+'\n')
        f.write('GOV:\t'+gov+'\n')
        f.write('SUBJ:\t'+subj+'\n')    

        ##### FIND COMP #####
        if 'comp' in '-'.join(list(token['kids'].values())): 
            n_comp=0
            for id, dep in token['kids'].items():  
                if 'comp' in dep: 
                    n_comp +=1   # 锁定子关系含comp关系的词 / count the number of comp
                    comp_temps = dep+'\t'+tree[id]['tag']+'\t'+tree[id]['lemma']   # [comp, upos=NOUN, lemma=hair]
                    token_children = tree[id]
                    if token_children['tag']=='ADP' or token_children['tag']=='SCONJ':  # 如果子关系的词为ADP或SCONJ，再看一层comp / if dependant is ADP or SCONJ, look it's dependant (obl)
                        for id, dep in token_children['kids'].items():
                            if 'comp' in dep:
                                # form_children = token_children['t']
                                # lemma_children = token_children['lemma']
                                comp = comp_temps+'\t<'+dep+'\t'+tree[id]['tag']+'\t'+tree[id]['lemma']+'>'
                    else:
                        comp = comp_temps
                    f.write('COMP'+str(n_comp)+':\t'+comp+'\n')
        else:
            f.write('COMP_NO:\t_\t_\t_\n')

        ##### FIND COMP #####

        f.write('EXEMPLE:\t'+exemple+'\n')
        f.write('\n')
