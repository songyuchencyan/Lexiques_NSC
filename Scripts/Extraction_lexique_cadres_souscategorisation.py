#!/usr/bin/env python  
# -*- coding: UTF-8 -*- 

import os
import re
from conllu import *
from conllnaija import *
from collections import Counter
import time




def get_trans_content(conll_content):
    trans = conll_content.strip('\n').split('\n\n')
    trans = [x.split('\n') for x in trans]
    return trans

def get_lemmapos_list(trans):
    lemmapos_list = [re.findall('LEMMA&POS:\t(.+)', x[0])[0] for x in trans]
    lemmapos_list = Counter(lemmapos_list)
    lemmapos_list = [x+'\t'+str(lemmapos_list[x]) for x in lemmapos_list]
    lemmapos_list = [[x.split('\t')[0], x.split('\t')[1], x.split('\t')[2]] for x in lemmapos_list]
    lemmapos_list.sort(key=lambda x:x[0])
    # lemmapos_list = ['\t'.join(x) for x in lemmapos_list]
    return lemmapos_list
    print(lemmapos_list)


def get_dict_souscat_sets(trans, lemmapos_list):
    dict_souscat_sets = {}

    for lemmapos in lemmapos_list:
        one_groupe_sets = []
        for one_set in trans:
            if '\t'.join(lemmapos[0:2]) == one_set[0].replace('LEMMA&POS:\t', ''):
                one_groupe_sets.append('\n'.join(one_set[1:]))
        dict_souscat_sets['\t'.join(lemmapos)] = one_groupe_sets
    return dict_souscat_sets              
        


def get_frames_arguments(dict_souscat_sets, f_input):
    for k, v in dict_souscat_sets.items():
        lemmaposfre = k
        one_group_set = v
        
        f_input.write(lemmaposfre+'\n')
        f_input.write('----------------------------------------------------\n')

        part_frames = get_frames(lemmaposfre, one_group_set)
        part_arguments = get_arguments(lemmaposfre, one_group_set)

        f_input.write('__frames : \n')
        for x in part_frames:
            f_input.write(x+'\n')
        f_input.write('----------------------------------------------------\n')
        f_input.write('__arguments : \n')
        for y,z in part_arguments.items():
            f_input.write(y+'\t'+z[0]+'\n')
            f_input.write(y+'\t'+z[1]+'\n')
        f_input.write('----------------------------------------------------\n')
        f_input.write('\n')


        
        
def get_arguments(lemmaposfre, one_group_set):
    list_arguments = [] ##### GET ALL ARGUMENTS : [[argument, fre], ...] #####
    list_pos = []   ##### GET ALL POS : [[argument\tpos, fre], ...] #####
    list_lemme = [] ##### GET ALL LEMME : [[argument\tlemme, fre], ...] #####
    for one_set in one_group_set:
        one_set = one_set.split('\n')
        part_gov = one_set[0]
        part_subj = one_set[1]
        part_comp = one_set[2:-1]
    
    
        args = []
        arg_gov = part_gov.split('\t')[1]
        arg_subj = part_subj.split('\t')[1]
        arg_comp = [x.split('\t')[1] for x in part_comp]
        args.extend([arg_gov, arg_subj])
        args.extend(arg_comp)
        list_arguments.extend(args)
        
        pos = []
        pos_gov = part_gov.split('\t')[1]+'\t'+part_gov.split('\t')[2]
        pos_subj = part_subj.split('\t')[1]+'\t'+part_subj.split('\t')[2]
        pos_comp = [x.split('\t')[1]+'\t'+x.split('\t')[2] if '<' not in x else x.split('\t')[1]+'\t'+x.split('\t')[2]+' '+re.findall('\<.+\\t(.+)\\t.+\>', x)[0] for x in part_comp]
        pos.extend([pos_gov, pos_subj])
        pos.extend(pos_comp)
        list_pos.extend(pos)

        lemme = []
        lemme_gov = part_gov.split('\t')[1]+'\t'+part_gov.split('\t')[3]
        lemme_subj = part_subj.split('\t')[1]+'\t'+part_subj.split('\t')[3]
        lemme_comp = [x.split('\t')[1]+'\t'+x.split('\t')[3] if '<' not in x else x.split('\t')[1]+'\t'+x.split('\t')[3]+' '+re.findall('\<.+\\t.+\\t(.+)\>', x)[0] for x in part_comp]
        lemme.extend([lemme_gov, lemme_subj])
        lemme.extend(lemme_comp)
        list_lemme.extend(lemme)

    while '_' in list_arguments:
        list_arguments.remove('_')
    while 'gov=root' in list_arguments:
        list_arguments.remove('gov=root')
    list_arguments = [[x[0], str(x[1])] for x in list(Counter(list_arguments).items())]

    while '_\t_' in list_pos:
        list_pos.remove('_\t_')
    while 'gov=root\t_' in list_pos:
        list_pos.remove('gov=root\t_')
    list_pos = [[x[0], str(x[1])] for x in list(Counter(list_pos).items())]

    while '_\t_' in list_lemme:
        list_lemme.remove('_\t_')
    while 'gov=root\t_' in list_lemme:
        list_lemme.remove('gov=root\t_')
    list_lemme = [[x[0], str(x[1])] for x in list(Counter(list_lemme).items())]


    dict_arguments = {}
    for one_argument in list_arguments:
        argument = one_argument[0]
        argument_fre = one_argument[1]
        argument_pos_list = []
        argument_lemme_list = []

        for one_pos in list_pos:
            pos_arg = one_pos[0].split('\t')[0]
            pos = one_pos[0].split('\t')[1]
            pos_fre = one_pos[1]
            if argument == pos_arg:
                posfre = [pos, pos_fre]
                argument_pos_list.insert(0, posfre)
        argument_pos_list.sort(key=lambda x:int(x[1]))
        argument_pos_list.reverse()
        argument_pos_list = '['+' '.join(['('+':'.join(x)+')' for x in argument_pos_list])+']'


        for one_lemme in list_lemme:
            lemme_arg = one_lemme[0].split('\t')[0]
            lemme = one_lemme[0].split('\t')[1]
            lemme_fre = one_lemme[1]
            if argument == lemme_arg:
                lemmefre = [lemme, lemme_fre]
                argument_lemme_list.insert(0, lemmefre)
        argument_lemme_list.sort(key=lambda x:int(x[1]))
        argument_lemme_list.reverse()
        argument_lemme_list = '['+' '.join(['('+':'.join(x)+')' for x in argument_lemme_list[0:10]])+']'
        dict_arguments[argument+'\t'+argument_fre] = [argument_pos_list, argument_lemme_list]
    return dict_arguments
        

def get_frames(lemmaposfre, one_group_set):
    dict_frame_exemple = {}
    list_frames = []    
    for one_set in one_group_set:
        one_set = one_set.split('\n')
        part_gov = one_set[0]
        part_subj = one_set[1]
        part_comp = one_set[2:-1]
        part_exemple = one_set[-1].replace('EXEMPLE:\t', '')

        #################################################### __frames ####################################################
        frame = [part_gov.split('\t')[1], part_subj.split('\t')[1], ','.join([x.split('\t')[1] for x in part_comp])]
        while '_' in frame:
            frame.remove('_')
        frame = '<'+', '.join(frame)+'>'
        list_frames.append(frame)

        ##### __frames => GET SHORTEST EXEXPLE #####
        '''
        key: frame, value: exemple
        '''
        if frame in list(dict_frame_exemple.keys()):
            if len(dict_frame_exemple[frame]) > len(part_exemple):
                dict_frame_exemple[frame] = part_exemple
        else:
            dict_frame_exemple[frame] = part_exemple
        ##### __frames => GET SHORTEST EXEXPLE #####

    ##### __frames => GET FREQUENCY LIST OF FRAMES : [[frame, fre], ...] #####
    list_frame_fre = [[x[0], str(x[1])] for x in list(Counter(list_frames).items())]
    ##### __frames => GET FREQUENCY LIST OF FRAMES : [[frame, fre], ...] #####
    
    ##### __frames => GET ALL __frames ELEMENTS #####
    list_framefreexemple = []
    for framefre in list_frame_fre:
        framefreexemple = '\t'.join(framefre) + '\t' + dict_frame_exemple[framefre[0]]
        list_framefreexemple.append(framefreexemple)
    ##### __frames => GET ALL __frames ELEMENTS #####
    #################################################### __frames ####################################################
    return list_framefreexemple
        





if __name__ == "__main__":
    time_start=time.time()

    f = open('Ensemble_infos_arguments_potentiels.tsv', 'r', encoding='UTF-8')
    f_input = open('Lexique de sous-catégorisation.tsv', 'w', encoding='UTF-8')
    conll_content = f.read()
    trans = get_trans_content(conll_content)
    lemmapos_list = get_lemmapos_list(trans)
    dict_souscat_sets = get_dict_souscat_sets(trans, lemmapos_list)
    get_frames_arguments(dict_souscat_sets, f_input)



    

    time_end=time.time()
    print('totally cost',time_end-time_start)
