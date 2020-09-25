#!/usr/bin/env python  
# -*- coding: utf-8 -*-
import re
import os
import time
time_start=time.time()

##### 提取完拿excel去一遍重，把大小写不一样的去了，Basic和basic。 #####

##### 读取目录里的文件 Lire tous les fichiers du répertoire #####
# folder_path = "E:/TAL/Stage/arborator/projects/Scripts/test"  # Insérez le chemin absolu qui contient des fichiers CONLL-U 
# file_list = os.listdir(folder_path) # Liste qui contient les noms des fichiers CONLL-U
# 读取该目录里所有文件
liste_noms_fichiers = ["80_corpus_concat.conllu"] # Insérez les noms des fichiers CONLL-U dans cette liste
folder_path = "." # Insérez le chemin absolu qui contient des fichiers CONLL-U de la liste "liste_noms_fichiers"
# for files in file_list: # Parcourir tous les fichiers CONLL-U de la liste
    # fichier_conll = open(folder_path + "/" + files,"r", encoding="UTF-8") # Lire chaque fichier CONLL-U de la liste
for fichier in liste_noms_fichiers: # Parcourir tous les fichiers CONLL-U de la liste
    fichier_conll = open(folder_path + "/" + fichier,"r", encoding="UTF-8") # Lire chaque fichier CONLL-U de la liste
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
            lexique = open("Lexique.txt","a", encoding="UTF-8") # Insérez le chemin absolu du fichier de lexique morphosyntaxique
            voir_lexique = open("Lexique.txt","r", encoding="UTF-8") # Insérez le chemin absolu du fichier de lexique morphosyntaxique, cette étape vise à vérifier si c'est une nouvelle entrée
            contenu = voir_lexique.readlines()    
            if terme not in contenu:
                lexique.write(terme)
                lexique.close()
time_end=time.time()
print('totally cost',time_end-time_start)
            
        
