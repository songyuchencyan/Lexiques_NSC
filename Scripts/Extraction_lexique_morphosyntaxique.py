#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import re
import os
import time
time_start=time.time()

##### 提取完拿excel去一遍重，把大小写不一样的去了，Basic和basic。 #####

##### 读取目录里的文件 Lire tous les fichiers du répertoire #####
# folder_path = "E:/TAL/Stage/arborator/projects/Scripts/test"  # 目标文件目录
# file_list = os.listdir(folder_path)
# 读取该目录里所有文件
liste_noms_fichiers = ["80_corpus_concat.conllu"]
folder_path = "."
# for files in file_list:
for fichier in liste_noms_fichiers:
    fichier_conll = open(folder_path + "/" + fichier,"r", encoding="UTF-8")
    # Lire le fichier conll ligne par ligne
    for ligne in fichier_conll:
        if ligne[0]!="#" and ligne!="\n" and ligne!="":
            ligne = ligne.split("\t")
            mot = ligne[1].replace(' ','')
            lemme = ligne[2].replace(' ','')
            cat = ligne[3].replace(' ','')
            trait = ligne[5].replace(' ','')
            glose = re.sub('AlignBegin.+Gloss=', '', ligne[9]).replace(' ','').replace('\n','')
            terme = mot + "\t" + cat + "\t" + trait + "\t" + lemme + "\t" + glose + "\n"
            lexique = open("Lexique.txt","a", encoding="UTF-8")
            voir_lexique = open("Lexique.txt","r", encoding="UTF-8")
            contenu = voir_lexique.readlines()    
            if terme not in contenu:
                lexique.write(terme)
                lexique.close()




time_end=time.time()
print('totally cost',time_end-time_start)
            
        
