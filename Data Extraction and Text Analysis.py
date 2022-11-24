#!/usr/bin/env python
# coding: utf-8

# ** IMPORTING LIBRARIES **

# In[2]:


import bs4
import urllib
import pandas as pd
import html5lib
import requests
import urllib.request
from bs4 import BeautifulSoup


# DATA EXTRACTION

# READING DATA

data="Input.xlsx"


df=pd.read_excel(data)


print(df.head())



l=df.values.tolist()


#storing data, uid as file name
for i in l:
    url=i[1]
    print(url)
    r=requests.get(url,headers={"User-Agent":"XY"})
    soup=BeautifulSoup(r.content,'html.parser')
    uid=int(i[0])
    path="C:/Users/JAY/OneDrive/Desktop/"+str(uid)+".txt"
    f = open(path, "w",encoding='utf-8')
    soup.encode("utf-8")
    # traverse paragraphs from soup
    for data in soup.find_all("p"):
        s = data.get_text()
        f.writelines(s)
  
    f.close()

# TEXT ANALYSIS

import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.tokenize import sent_tokenize
import re




import nltk
nltk.download('stopwords')




nltk.download('punkt')


# Creating a list of Positive and Negative words from positive and negative dicitionaries



path1="C:/Users/JAY/OneDrive/Desktop/positive.txt"
pos=open(path1,'r',encoding='utf-8')
l=pos.read()
positive=l.split()

path2="C:/Users/JAY/OneDrive/Desktop/negative.txt"
neg=open(path2,'r',encoding='utf-8')
l1=neg.read()
negative=l1.split()




def count_complex_words(words_list):
    c = 0
    for word in words_list:
        l = re.findall('(?!e$)[aeiou]+', word, re.I)+re.findall('^[aeiouy]*e$', word, re.I)
        if len(l) > 2:
            c += 1
    return c





def count_syllables(word):
    c = 0
    vowels = 'aeiou'
    l = re.findall(f'(?!e$)(?!es$)(?!ed$)[{vowels}]', word, re.I)
    return len(l)





def count_personal_pronouns(text):
    pronoun_count = re.compile(r'\b(I|we|ours|my|mine|(?-i:us))\b', re.I)
    pronouns = pronoun_count.findall(text)
    return len(pronouns)




ans=[]
stop_words = set(stopwords.words('english')) 
for i in l:
    b=[]
    url=i[1]
    #print(url)
    uid=int(i[0])
    b.append(uid)
    b.append(url)
    path="C:/Users/JAY/OneDrive/Desktop/Data Extraction/"+str(uid)+".txt"
    
    #Reading file
    file1 = open(path,'r',encoding='utf-8') 
    line = file1.read()
    words = line.split()
    
    #filtering using stop words
    filtered=[]
    for r in words: 
        if not r in stop_words: 
            filtered.append(r)
    #print(filtered[:5])
    
    # Calculating positive and negative score
    positive_score=0
    negative_score=0
    for i in filtered:
        if(i in positive):
            positive_score+=1
        elif(i in negative):
            negative_score+=-1
    negative_score=negative_score*(-1)
    #print(positive_score)
    #print(negative_score)
    
    b.append(positive_score)
    b.append(negative_score)
    
    #polarity score
    polarity_score=(positive_score - negative_score)/ ((positive_score + negative_score) + 0.000001)
    
    #subjectivity score
    subject_score=(positive_score+negative_score)/(len(filtered)+0.000001)
    
    b.append(polarity_score)
    b.append(subject_score)
    
    #Joining all cleaned words
    filterstr= ' '.join([str(elem) for elem in filtered])
    punc = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
    res=" "
    # Removing punctuations in string Using loop + punctuation string
    for ele in filterstr:
        if ele not in punc:
            res+=ele
            
    #word count        
    word_tokens = word_tokenize(res)
    word_count=len(word_tokens)
    #print(word_count)
    
    # average no of words per sentence
    sent_token=sent_tokenize(filterstr)
    if(len(sent_token)!=0 ):
        avg_no_of_words_per_sentence= int(word_count/len(sent_token))
    else:
        avg_no_of_words_per_sentence= 0
        
    #print(int(avg_no_of_words_per_sentence))
    
    s=0
    syllables=[]
    for i in word_tokens:
        list1=[]
        list1.append(i)
        y=count_syllables(i)
        list1.append(y)
        syllables.append(list1)
        s+=y
    
    
    #pronouns    
    pronouns=count_personal_pronouns(res)
    
    
    #average word length
    c=0
    for word in word_tokens:
        c+=len(word)
    if(len(word_tokens)!=0):    
        avg_word_length= round(c/len(word_tokens))
    else:
        avg_word_length= 0
         
    #complex word count
    complex_words=count_complex_words(word_tokens)
    
    
    #percentage of complex words
    if(word_count!=0):
        percentage_of_complex= complex_words/word_count
    else:
        percentage_of_complex=0
    
    
    #average sentence length
    if(len(sent_token)!=0):
        avg_sentence_length=round(len(word_tokens)/len(sent_token))
    else:
        avg_sentence_length=0
    
    
    #fog index
    fog_index= (0.4)*(avg_sentence_length+percentage_of_complex)
    
    #appending in a list
    b.append(avg_sentence_length)
    b.append(percentage_of_complex)
    b.append(fog_index)
    b.append(avg_no_of_words_per_sentence)
    b.append(complex_words)
    b.append(word_count)
    b.append(s)
    b.append(pronouns)   
    b.append(avg_word_length) 
    
    #print(b)
    ans.append(b)    
print(ans[:5])


df = pd.DataFrame(ans, columns =['URL_ID', 'URL','POSITIVE SCORE','NEGATIVE SCORE','POLARITY SCORE','SUBJECTIVITY SCORE','AVG SENTENCE LENGTH','PERCENTAGE OF COMPLEX WORDS','FOG INDEX','AVG NUMBER OF WORDS PER SENTENCE','COMPLEX WORD COUNT','WORD COUNT','SYLLABLE PER WORD','PERSONAL PRONOUNS','AVG WORD LENGTH'])



print(df)



df.to_excel("output.xlsx")








