import gensim
import os

dir = os.getcwd() + "word2vec_skill.bin"
#loading the model
model = gensim.models.Word2Vec.load("C:/Users/Amrut/Desktop/askIt2021/finalYrRawFiles/askIt/Forum/word2vec_skill.bin")
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize 
import nltk
from nltk.stem import WordNetLemmatizer
import re

def test(sentence):
  text =sentence
  text=text.lower()
  stop_words = set(stopwords.words('english')) 
  word_tokens = word_tokenize(text)
  wh=['how','who','whom','where','what','which','why']
  filtered_sentence=[]
  for w in word_tokens:
    if w not in stop_words:
      if w not in wh:
        filtered_sentence.append(w) 

  tagged_text=nltk.pos_tag(filtered_sentence)
  l=len(tagged_text)
  #print("tagged text",tagged_text)
  final=[]
  for i in range(0,l):
    for j in range(0,1):
      if tagged_text[i][1]=="NN" or tagged_text[i][1]=="NNP" or tagged_text[i][1]=="NNS":
        final.append(tagged_text[i][0])
  #vocab_len=len(model.wv)          
  if (len(final)!=0):
  #print(skills['skill.name'])
    all_related_list=[]
    skill_set=[]
    for i in final:
      i=i.lower() #convert the given string into lower case
      i = re.sub('[()]', '', i)
      k=i.split(" ")
      for s in k:
        for j in model.wv.key_to_index:
          if j==s and j!='language':
            skill_set.append(j)
            all_related_list.append(model.wv.similar_by_word(j))


  #print(all_related_list)
      
    for i in all_related_list:
      for j in i:
        for k in range(0,len(j),2):
          skill_set.append(j[k])
      
    return (skill_set)


  else:
    return("No a relevant skills found")