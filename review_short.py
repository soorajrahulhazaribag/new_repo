import requests
from bs4 import BeautifulSoup
import nltk
import ast
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet



##-------------------------------------------------------------------------------------





file = open("Review.txt","w",encoding="utf-8")



url = "https://www.wired.com/story/aquaman-trailer-physics/"
html_text = requests.get(url)
soup = BeautifulSoup(html_text.text, "lxml")
containers = soup.find_all("article",{"class": "article-body-component article-body-component--science"} ,True,None,None)
for container in containers:
    file.write(container.get_text())    
    
file.close()

##########################################################################################
def preProcessing (inputFileStr, outputFileStr, printResult): #preprocessing the text file
    inputFile = open(inputFileStr,"r").read()
    outputFile = open(outputFileStr,"w+")
    cachedStopWords = nltk.corpus.stopwords.words("english")
    cachedStopWords.append('OMG')
    cachedStopWords.append(':-')
    cachedStopWords.append('Oh')

    result = (' '.join([word for word in inputFile.split() if word not in cachedStopWords]))
    if(printResult):
        #print('Following are the stopwords')
        #print(cachedStopWords)
        outputFile.write(str(result))
    outputFile.close()

preProcessing("Review.txt", "preProcessing.txt", "new1.txt")

############################################################################################
def tokenizeArticle(inputFileStr, outputFileStr, printResult): #Tokenizing by sentence
    tokenizedArticle = {}
    inputFile = open(inputFileStr,"r").read()
    outputFile = open(outputFileStr,"w")
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    tokenNo = 1;
    for sentence in tokenizer.tokenize(inputFile):
        tokenizedArticle[tokenNo] = sentence
        tokenNo+= 1
    outputFile.write(str(tokenizedArticle))
    if(printResult):
        for key,value in tokenizedArticle.items():
            #print(key,' ',value)
            pass
    outputFile.close()

tokenizeArticle("preProcessing.txt", "tokenizeArticle.txt", "new1.txt")


##############################################################################################
def posTagging(inputFileStr,outputFileStr,printResult): #Tagging each word
    inputFile = open(inputFileStr,"r").read()
    outputFile=open (outputFileStr,"w")
    inputTupples=ast.literal_eval(inputFile)
    outputPost={}
    for key,value in inputTupples.items():
        outputPost[key]=nltk.pos_tag(nltk.word_tokenize(value))
    if(printResult):
        for key,value in outputPost.items():
            #print(key,' ',value)
            pass
    outputFile.write(str(outputPost))
    outputFile.close()

posTagging("tokenizeArticle.txt", "posTagging.txt", "new1.txt")


#################################################################################################
def keywordExtraction(inputFileStr,outputFileStr,printResult): #Finding list of aspectation words
    inputFile = open(inputFileStr,"r").read()
    outputFile = open(outputFileStr,"w")
    inputTupples=ast.literal_eval(inputFile)
    prevWord=''
    prevTag=''
    currWord=''
    keywordList=[]
    outputDict={}
    for key,value in inputTupples.items():
        for word,tag in value:
            if(tag=='NN' or tag=='NNP'):
                if(prevTag=='NN' or prevTag=='NNP'):
                    currWord=prevWord +' '+word

                else:
                    keywordList.append(prevWord)
                    currWord= word
            prevWord=currWord
            prevTag=tag

    print(outputDict)
    for keyword in keywordList:
        if(keywordList.count(keyword)>1):
            outputDict[keyword]=keywordList.count(keyword)
    print(outputDict)
    outputFile.write(str(outputDict))
    outputFile.close()

keywordExtraction("posTagging.txt", "keywordExtraction.txt", "new1.txt")




####################################################################################

"""
def identifyOpinionWords(inputArticleListStr, inputKeywordListStr, outputKeywordOpinionListStr,printResult):  #identifying opinion words     
    inputArticleList = open(inputArticleListStr,"r").read()
    inputKeywordList = open(inputKeywordListStr,"r").read()
    outputKeywordOpinionList=open(outputKeywordOpinionListStr,"w")
    inputArticleTuples=ast.literal_eval(inputArticleList)
    inputKeywordTuples=ast.literal_eval(inputKeywordList)
    print(inputKeywordTuples)
    outputKeywordOpinionTuples={}
    orientationCache={}
    negativeWordSet = {"don't","never", "nothing", "nowhere", "noone", "none", "not",
                  "hasn't","hadn't","can't","couldn't","shouldn't","won't",
                  "wouldn't","don't","doesn't","didn't","isn't","aren't","ain't"}
    for keyword,no in inputKeywordTuples:
        keywordTokens= word_tokenize(keyword)
        count=0
        for key,value in inputArticleTuples.items():
            condition=True
            isNegativeSen=False
            for subWord in keywordTokens:
                if(subWord in str(value).upper()):
                    condition = condition and True
                else:
                    condition = condition and False
            if(condition):
                for negWord in negativeWordSet:
                    if(not isNegativeSen):#once senetence is negative no need to check this condition again and again
                        if negWord.upper() in str(value).upper():
                            isNegativeSen=isNegativeSen or True
                outputKeywordOpinionTuples.setdefault(aspect,[0,0,0])
                for word,tag in value:
                     if(tag=='JJ' or tag=='JJR' or tag=='JJS'or tag== 'RB' or tag== 'RBR'or tag== 'RBS'):
                         count+=1
                         if(word not in orientationCache):
                             orien=orientation(word)
                             orientationCache[word]=orien
                         else:
                             orien=orientationCache[word]
                         if(isNegativeSen and orien is not None):
                             orien= not orien
                         if(orien==True):
                             outputKeywordOpinionTuples[aspect][0]+=1
                         elif(orien==False):
                             outputKeywordOpinionTuples[aspect][1]+=1
                         elif(orien is None):
                             outputKeywordOpinionTuples[aspect][2]+=1
        if(count>0):
            #print(aspect,' ', outputAspectOpinionTuples[aspect][0], ' ',outputAspectOpinionTuples[aspect][1], ' ',outputAspectOpinionTuples[aspect][2])
            outputKeywordOpinionTuples[aspect][0]=round((outputKeywordOpinionTuples[aspect][0]/count)*100,2)
            outputKeywordOpinionTuples[aspect][1]=round((outputKeywordOpinionTuples[aspect][1]/count)*100,2)
            outputKeywordOpinionTuples[aspect][2]=round((outputKeywordOpinionTuples[aspect][2]/count)*100,2)
            print(keyword,':\t\tPositive => ', outputKeywordOpinionTuples[aspect][0], '\tNegative => ',outputKeywordOpinionTuples[aspect][1])
    if(printResult):
        print(outputKeywordOpinionList)
    outputKeywordOpinionList.write(str(outputKeywordOpinionTuples))
    outputKeywordOpinionList.close();



identifyOpinionWords("posTagging.txt","keywordExtraction.txt", "identifyOpinionWords.txt", "new10.txt")

"""
