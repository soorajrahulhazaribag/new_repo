import requests
from bs4 import BeautifulSoup
import nltk
import ast
import re
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet
from nltk.corpus import sentiwordnet



##-------------------------------------------------------------------------------------


## Scraping Data From amazon.in



file = open("Review.txt","w",encoding="utf-8")

i = 1;
while i<6:
    
    url = "https://www.amazon.in/Moto-Plus-Lunar-Grey-64GB/product-reviews/B071HWTHPH/ref=cm_cr_arp_d_paging_btm_2?ie=UTF8&reviewerType=all_reviews&pageNumber="+str(i)
    html_text = requests.get(url)
    soup = BeautifulSoup(html_text.text, "lxml")
    containers = soup.find_all("span",{"class": "a-size-base review-text"} ,True,None,None)
    for container in containers:
        file.write(container.get_text())    

    i = i+1;
    
file.close()

##-------------------------------------------------------------------------------------


##Analysing the scraped data using nlp



##-------------------------------------------------------------------------------------

def preProcessing (inputFileStr, outputFileStr, printResult): #preprocessing the text file
    inputFile = open(inputFileStr,"r").read()
    outputFile = open(outputFileStr,"w+")
    cachedStopWords = nltk.corpus.stopwords.words("english")
    cachedStopWords.append('OMG')
    cachedStopWords.append(':-')
    cachedStopWords.append('READ')
    cachedStopWords.append('..')
    cachedStopWords.append('...')
    cachedStopWords.append('....')
    result = (' '.join([word for word in inputFile.split() if word not in cachedStopWords]))
    if(printResult):
        print('Following are the stopwords')
        print(cachedStopWords)
        outputFile.write(str(result))
    outputFile.close()

preProcessing("Review.txt", "preProcessing.txt", "new1.txt")


##-------------------------------------------------------------------------------------




def tokenizeReviews(inputFileStr, outputFileStr, printResult): #Tokenizing by sentence
    tokenizedReviews = {}
    inputFile = open(inputFileStr,"r").read()
    outputFile = open(outputFileStr,"w")
    tokenizer = nltk.tokenize.punkt.PunktSentenceTokenizer()
    uniqueId = 1;
    cachedStopWords = nltk.corpus.stopwords.words("english")
    for sentence in tokenizer.tokenize(inputFile):
        tokenizedReviews[uniqueId] = sentence
        uniqueId+= 1
    outputFile.write(str(tokenizedReviews))
    if(printResult):
        for key,value in tokenizedReviews.items():
            print(key,' ',value)
    outputFile.close()

tokenizeReviews("preProcessing.txt", "tokenizeReviews.txt", "new1.txt")


##-------------------------------------------------------------------------------------

def posTagging(inputFileStr,outputFileStr,printResult): #Tagging each word
    inputFile = open(inputFileStr,"r").read()
    outputFile=open (outputFileStr,"w")
    inputTupples=ast.literal_eval(inputFile)
    outputPost={}
    for key,value in inputTupples.items():
        outputPost[key]=nltk.pos_tag(nltk.word_tokenize(value))
    if(printResult):
        for key,value in outputPost.items():
            print(key,' ',value)
    outputFile.write(str(outputPost))
    outputFile.close()

posTagging("tokenizeReviews.txt", "posTagging.txt", "new1.txt")

##-------------------------------------------------------------------------------------


def aspectExtraction(inputFileStr,outputFileStr,printResult): #Finding list of aspectation words
    inputFile = open(inputFileStr,"r").read()
    outputFile = open(outputFileStr,"w")
    inputTupples=ast.literal_eval(inputFile)
    prevWord=''
    prevTag=''
    currWord=''
    aspectList=[]
    outputDict={}
    for key,value in inputTupples.items():
        for word,tag in value:
            if(tag=='NN' or tag=='NNP'):
                if(prevTag=='NN' or prevTag=='NNP'):
                    currWord=prevWord +' '+word

                else:
                    aspectList.append(prevWord.upper())
                    currWord= word
            prevWord=currWord
            prevTag=tag


    for aspect in aspectList:
        if(aspectList.count(aspect)>1):
            if(outputDict.keys()!=aspect):
                outputDict[aspect]=aspectList.count(aspect)
    outputAspect=sorted(outputDict.items(),key=lambda x: x[1],reverse = True)
    print(outputAspect)
    outputFile.write(str(outputAspect))
    outputFile.close()

aspectExtraction("posTagging.txt", "aspectExtraction.txt", "new1.txt")


##-------------------------------------------------------------------------------------

def orientation(inputWord): 
    wordSynset=wordnet.synsets(inputWord)
    if(len(wordSynset) != 0):
        word=wordSynset[0].name()
        orientation=sentiwordnet.senti_synset(word)
        if(orientation.pos_score()>orientation.neg_score()):
            return True
        elif(orientation.pos_score()<orientation.neg_score()):
            return False


##-------------------------------------------------------------------------------------




def identifyOpinionWords(inputReviewListStr, inputAspectListStr, outputAspectOpinionListStr,printResult):  #identifying opinion words     
    inputReviewList = open(inputReviewListStr,"r").read()
    inputAspectList = open(inputAspectListStr,"r").read()
    outputAspectOpinionList=open(outputAspectOpinionListStr,"w")
    inputReviewsTuples=ast.literal_eval(inputReviewList)
    inputAspectTuples=ast.literal_eval(inputAspectList)
    outputAspectOpinionTuples={}
    orientationCache={}
    negativeWordSet = {"don't","never", "nothing", "nowhere", "noone", "none", "not",
                  "hasn't","hadn't","can't","couldn't","shouldn't","won't",
                  "wouldn't","don't","doesn't","didn't","isn't","aren't","ain't"}
    for aspect,no in inputAspectTuples:
        aspectTokens= word_tokenize(aspect)
        count=0
        for key,value in inputReviewsTuples.items():
            condition=True
            isNegativeSen=False
            for subWord in aspectTokens:
                if(subWord in str(value).upper()):
                    condition = condition and True
                else:
                    condition = condition and False
            if(condition):
                for negWord in negativeWordSet:
                    if(not isNegativeSen):#once senetence is negative no need to check this condition again and again
                        if negWord.upper() in str(value).upper():
                            isNegativeSen=isNegativeSen or True
                outputAspectOpinionTuples.setdefault(aspect,[0,0,0])
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
                             outputAspectOpinionTuples[aspect][0]+=1
                         elif(orien==False):
                             outputAspectOpinionTuples[aspect][1]+=1
                         elif(orien is None):
                             outputAspectOpinionTuples[aspect][2]+=1
        if(count>0):
            #print(aspect,' ', outputAspectOpinionTuples[aspect][0], ' ',outputAspectOpinionTuples[aspect][1], ' ',outputAspectOpinionTuples[aspect][2])
            outputAspectOpinionTuples[aspect][0]=round((outputAspectOpinionTuples[aspect][0]/count)*100,2)
            outputAspectOpinionTuples[aspect][1]=round((outputAspectOpinionTuples[aspect][1]/count)*100,2)
            outputAspectOpinionTuples[aspect][2]=round((outputAspectOpinionTuples[aspect][2]/count)*100,2)
            print(aspect,':\t\tPositive => ', outputAspectOpinionTuples[aspect][0], '\tNegative => ',outputAspectOpinionTuples[aspect][1])
    if(printResult):
        print(outputAspectOpinionList)
    outputAspectOpinionList.write(str(outputAspectOpinionTuples))
    outputAspectOpinionList.close();



identifyOpinionWords("posTagging.txt","aspectExtraction.txt", "identifyOpinionWords.txt", "new10.txt")


