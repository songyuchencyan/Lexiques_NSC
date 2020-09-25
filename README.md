# Lexiques_NSC
# 

## Introduction

Le travail vise à extraire deux lexiques à partir du treebank SUD du naija dans le cadre du projet NaijaSynCor : <br>
  * Un lexique morphosyntaxique dont chaque entrée est associée à ses traits morphologiques <br> 
  * Un lexique syntaxique dont chaque entrée est associée à ses cadres de sous-catégorisation <br>

Ces lexiques servent à étudier le vocabulaire et l'usage du mot en naija, et à rechercher les erreurs d'annotation pour rendre le treebank propre. <br>

## 
## Catalogue
### 
### Lexiques
  * **Lexique morphosyntaxique.xlsx** : le lexique morphosyntaxique comporte 6 colonnes, les cinq premières colonnes contiennent les informations sur la forme, la partie du discours, les traits morphologiques, le lemme et la glose du token. La sixième est la colonne de commentaire où nous pouvons partager nos diverses opinions pour obtenir le meilleur résultat.
  * **Ensemble_infos_arguments_potentiels.tsv** : chaque entrée est un ensemble d'informations qui indique des arguments potentiels avec toutes ses informations syntaxiques et morphologiques pour chaque token du treebank.
  * **Lexique de cadres de sous-catégorisation** : le lexique de cadres de sous-catégorisation est produit automatiquement à partir du fichier
  * **Ensemble_infos_arguments_potentiels.tsv**, il regroupe des informations de sous-catégorisations identiques du même lemme d'une catégorie en une seule entrée.

### 
### Scripts
  * **Extraction_lexique_morphosyntaxique.py** : le script prend une liste des fichiers CONLL-U et extrait des infos nécessaires pour construire un lexique morphosyntaxique.
    * Mode 1.
      ```Python
      liste_noms_fichiers = ["80_corpus_concat.conllu"] //Insérez les noms des fichiers CONLL-U dans cette liste
      ```
      ```Python
      folder_path = "." //Insérez le chemin absolu qui contient des fichiers CONLL-U de la liste "liste_noms_fichiers"
      ```
      ```Python
      for fichier in liste_noms_fichiers: //Parcourir tous les fichiers CONLL-U de la liste
        fichier_conll = open(folder_path + "/" + fichier,"r", encoding="UTF-8") //Lire chaque fichier CONLL-U de la liste
      ```
      ```Python
      lexique = open("Lexique.txt","a", encoding="UTF-8") //Insérez le chemin absolu du fichier de lexique morphosyntaxique
      voir_lexique = open("Lexique.txt","r", encoding="UTF-8") //Insérez le chemin absolu du fichier de lexique morphosyntaxique
      ```
     
### Erreurs

