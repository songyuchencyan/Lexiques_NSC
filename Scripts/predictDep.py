import os, re, tqdm
import conll



langNames={}
langcodef=open("languageCodes.tsv")
langcodef.readline()
for li in langcodef:
	lis = li.strip().split('\t')
	langNames[lis[0]]=lis[-1]
	
mylangNames={'ca': 'Catalan',
			 'cu': 'OldChurchSlavonic',
			 'nl': 'Dutch',
			 'el': 'Greek',
			 'ro': 'Romanian',
			 'es': 'Spanish',
			 'gd':'Gaelic',
			 'ug': 'Uyghur', 
			 'aii':'Assyrian',
			 'bxr':'Buryat', 
			 'fro':'OldFrench', 
			 'grc': 'AncientGreek',  
			 'gsw':'SwissGerman',
			 'gun': 'MbyáGuaraní',
			 'hsb':'UpperSorbian',
			 'kmr':'Kurmanji',
			 'kpv':'Komi', 
			 'lzh':'ClassicalChinese',
			 'orv':'OldEastSlavic',
			 'pcm':'Naija',
			 'qhe':'HindiEnglish',
			 'sms':'SkoltSami',
			 'sme':'NorthSami', 
			 'swl':'SwedishSign',   
			 'yue':'Cantonese'
				 }


langNames = dict(langNames, **mylangNames)

langnameGroup={li.split('\t')[0]:li.split('\t')[1] for li in open('languageGroups.txt').read().strip().split('\n')  }

def allfiles(folder="ud-treebanks-v2.5", filter="*.conllu"):
	filelist=[]
	for root, dirnames, filenames in os.walk(folder):
		for filename in fnmatch.filter(filenames, filter):
			filelist+=[os.path.join(root, filename)] 
	return filelist

def getAllConllFiles(basefolder, groupByLanguage=True):
	"""
	for a given basefolder, 
	gives back a dictionary code -> list of files under the code
	{"en":["/dqsdf/en.partut.conllu", ...] }
	"""
	langConllFiles={}
	for dirpath, dirnames, files in os.walk(basefolder):
		for f in files:
			if f.endswith(".conllu") and "not-to-release" not in dirpath:
				if groupByLanguage:	lcode=re.split(r"\W|_",f)[0] # now all different treebanks for iso-639-3english are under 'en'
				else:			lcode=re.split(r"\-",f)[0] # now the codes are for example 'en', 'en_partut', 'en_lines'				
				#if lcode in langConllFiles: print lcode,f
				langConllFiles[lcode]=langConllFiles.get(lcode,[])+[os.path.join(dirpath,f)]
	#print langConllFiles
	return langConllFiles
 
conllfiles=getAllConllFiles("../sud-treebanks-v2.4")

#print()
unigrams={}
bigrams={}
bigtype={}
for fi in tqdm.tqdm(conllfiles['ja']):
	if "FTB" in fi: continue
	print('analyzing',fi)
	trees = conll.conllFile2trees(fi)
	
	
	
	for tree in trees:
		toks = [tree[i]['t'] for i in sorted(tree.keys()) if tree[i]['tag']!="PUNCT"]
		for t in toks:
			unigrams[t]=unigrams.get(t,0)+1
		maxtree = max(tree.keys())
		for i in sorted(tree):
			if i==maxtree: continue
			na = tree[i]
			nb = tree[i+1]
			a = na['t']
			b = nb['t']
			if na['tag']=="PUNCT" or nb['tag']=="PUNCT": continue
			bigrams[(a,b)]=bigrams.get((a,b),0)+1
			#print(i,i+1,na['gov'],type([-1]),bigrams.get((a,b),[]))
			if (i+1) in na['gov']: bigtype[(a,b)]=bigtype.get((a,b),[])+[-1]
			elif i in nb['gov']: bigtype[(a,b)]=bigtype.get((a,b),[])+[1]
			else: bigtype[(a,b)]=bigtype.get((a,b),[])+[0]

bigvect={}
bigramsrel={}
unigramsrel={}
nbbigs=sum(bigrams.values())
nbunigs=sum(unigrams.values())

for big,li in bigtype.items():
	tot = len(li)
	bigvect[big]=(li.count(1)/tot,li.count(-1)/tot,li.count(0)/tot)
	bigramsrel[big]=bigrams[big]/nbbigs

unigramsrel={u:unigrams[u]/nbunigs for u in unigrams}
	



			
thresh=5	
goodbigrams = {big:bigrams[big] for big in bigrams if bigrams[big]>thresh}
print(goodbigrams)	
print(len(goodbigrams))

outf=open("jadep.tsv","w")
outf.write('\t'.join(['a','b','freqa','freqb','freqab','agov','bgov','nogov'])+'\n')
for (a,b) in sorted(goodbigrams):
	outf.write('\t'.join([a,b]+['%f' % x for x in [unigramsrel[a],unigramsrel[b],bigramsrel[(a,b)], bigvect[(a,b)][0], bigvect[(a,b)][1], bigvect[(a,b)][2]]])+'\n')


	
	
	
		
