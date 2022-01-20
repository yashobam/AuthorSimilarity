import math
def clean_text(txt):
	wd=""
	for i in range(len(txt)):
		if txt[i]!="." and txt[i]!="?" and txt[i]!="," and txt[i]!="!" and txt[i]!=":" and txt[i]!=";" and txt[i]!="\"":
			wd+=txt[i].lower()
	return wd
def stem(wrd):
	sw=wrd
	if len(wrd)>=4:
		if len(wrd)>3 and wrd[-3:]=="ing":
			sw=wrd[:-3]
			sw=stem(sw)
		elif wrd[-2:]=="er":
			sw=wrd[:-2]
			sw=stem(sw)
		elif wrd[-1:]=="s":
			sw=wrd[:-1]
			sw=stem(sw)
		elif wrd[-1:]=="y":
			sw=wrd[:-1]+"i"
			sw=stem(sw)
		elif wrd[-1:]=="e":
			sw=wrd[:-1]
			sw=stem(sw)
		elif wrd[len(wrd)-1] == wrd[len(wrd)-2]: 
			sw = wrd[:-1] 
			sw=stem(sw)
		elif wrd[-2:]=="ed":
			sw=wrd[:-2]
			sw=stem(sw)
		elif wrd[-2:]=="ed":
			sw=wrd[:-2]
			sw=stem(sw)
		elif wrd[-2:]=="ly":
			sw=wrd[:-2]
			sw=stem(sw)
		elif len(wrd)>4 and wrd[-4:]=="hood":
			sw=wrd[:-4]
			sw=stem(sw)
		elif wrd[-2:]=="er":
			sw=wrd[:-2]
			sw=stem(sw)
		elif len(wrd)>3 and wrd[-3:]=="ism":
			sw=wrd[:-3]
			sw=stem(sw)
		if len(wrd)>3 and wrd[-3:]=="ist":
			sw=wrd[:-3]
			sw=stem(sw)
		if len(wrd)>3 and wrd[-3:]=="ate":
			sw=wrd[:-3]
			sw=stem(sw)
	return sw
def compare_dictionaries(d1,d2):
	sc=0
	totald1=0
	for i in d1:
		totald1+=d1[i]
	for k in d2:
		if k in d1:
			sc+=d2[k]*math.log(d1[k]/totald1)
		else:
			sc+=d2[k]*math.log(0.5/totald1)
	return sc
class TextModel():

	def __init__(self,model_name):
		self.name=model_name
		self.words={}
		self.word_lengths={}
		self.stems={}
		self.sentence_lengths={}
		self.first_words={}
	def __repr__(self):
		s="text model name: "+self.name
		s+="\n"+"  number of words: "+str(len(self.words))
		s+="\n"+'  number of word lengths: ' + str(len(self.word_lengths))
		s+="\n"+"  number of stems: "+str(len(self.stems))
		s+="\n"+'  number of sentence lengths: ' + str(len(self.sentence_lengths))
		s+="\n"+"  number of first words: "+str(len(self.first_words))
		return s
	def similarity_scores(self,other):
		s=[0]*5
		s[0]=compare_dictionaries(other.words,self.words)
		s[1]=compare_dictionaries(other.word_lengths,self.word_lengths)
		s[2]=compare_dictionaries(other.stems,self.stems)
		s[3]=compare_dictionaries(other.sentence_lengths,self.sentence_lengths)
		s[4]=compare_dictionaries(other.first_words,self.first_words)
		return s
	def classify(self,source1,source2):
		sc1=self.similarity_scores(source1)
		print(sc1)
		sc2=self.similarity_scores(source2)
		print(sc2)
		wsc1=sc1[0]*10+sc1[1]*5+sc1[2]*10+sc1[3]*2+sc1[4]*3
		wsc2=sc2[0]*10+sc2[1]*5+sc2[2]*10+sc2[3]*2+sc2[4]*3
		if wsc1>=wsc2:
			print(self.name+" is more likely to be from "+source1.name)
		else:
			print(self.name+" is more likely to be from "+source2.name)
	def add_string(self, s):
		ss=0

		for i in s.split():
			if i[-1]=="." or i[-1]=="?" or i[-1]=="!":
				ss+=1

				if ss in self.sentence_lengths:
					self.sentence_lengths[ss]+=1
				else:
					self.sentence_lengths[ss]=1
				ss=0
			else:
				ss+=1
		sad=[]
		word_list = clean_text(s).split()
		for w in word_list:
			sad+=w.split("\n")
		word_list=sad
		wl =s.split()
		
		for i in range(len(wl)):
			if i+1<len(wl) and wl[i][-1]=="." or wl[i][-1]=="?" or wl[i][-1]=="!":
				if wl[i+1] in self.first_words:
					self.first_words[wl[i+1]]+=1
				else:
					self.first_words[wl[i+1]]=1	
		for w in word_list:
			if w in self.words:
				self.words[w]+=1
				if len(w) in self.word_lengths:
					self.word_lengths[len(w)]+=1
				else:
					self.word_lengths[len(w)]=1
			else:
				self.words[w]=1
				if len(w) in self.word_lengths:
					self.word_lengths[len(w)]+=1
				else:
					self.word_lengths[len(w)]=1
		for w in word_list:
			w=stem(w)
			if w in self.stems:
				self.stems[w]+=1
			else:
				self.stems[w]=1
	def save_model(self):   
		q = open(self.name+"_words", 'w')      
		q.write(str(self.words))              
		q.close()

		q = open(self.name+"_word_lengths", 'w')      
		q.write(str(self.word_lengths))              
		q.close()

		q = open(self.name+"_stems", 'w')      
		q.write(str(self.stems))              
		q.close()

		q = open(self.name+"_sen_lengths", 'w')      
		q.write(str(self.sentence_lengths))              
		q.close()

		q = open(self.name+"_first_words", 'w')      
		q.write(str(self.first_words))              
		q.close()
	def read_model(self):
		q=open(self.name+"_words", 'r')
		wd=q.read()
		q.close()
		self.words=dict(eval(wd))
		q=open(self.name+"_word_lengths", 'r')
		wdl=q.read()
		q.close()
		self.word_lengths=dict(eval(wdl))
		q=open(self.name+"_sen_lengths", 'r')
		wd=q.read()
		q.close()
		self.sentence_lengths=dict(eval(wd))
		q=open(self.name+"_stems", 'r')
		wd=q.read()
		q.close()
		self.stems=dict(eval(wd))
		q=open(self.name+"_first_words", 'r')
		wd=q.read()
		q.close()
		self.first_words=dict(eval(wd))
	def add_file(self,filename):
		f = open(filename, 'r', encoding='utf8', errors='ignore')
		txt=f.read()
		self.add_string(txt)

def run_tests():
    source1 = TextModel('Twain')
    #source1.add_file('Twain.txt')
    source1.read_model()
    source2 = TextModel('JaneAustin')
    #source2.add_file('JaneAustin.txt')
    source2.read_model()

    new1 = TextModel('VirginaWoolf')
    new1.add_file('VirginaWoolf.txt')
    new1.save_model()
    new1.classify(source1, source2)


run_tests()