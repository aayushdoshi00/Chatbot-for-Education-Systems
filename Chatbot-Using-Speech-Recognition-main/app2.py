from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from time import ctime
import pyttsx3
import speech_recognition as sr

import random
import nltk
import string


app = Flask(__name__)
CORS(app)
r = sr.Recognizer()



f=open('SFIT.txt','r',errors = 'ignore')
m=open('AICTE.txt','r',errors = 'ignore')
checkpoint = "./chatbot_weights.ckpt"

raw=f.read()
rawone=m.read()
raw=raw.lower()# converts to lowercase
rawone=rawone.lower()# converts to lowercase
#nltk.download('punkt') # first-time use only
#nltk.download('wordnet') # first-time use only
sent_tokens = nltk.sent_tokenize(raw)# converts to list of sentences 
word_tokens = nltk.word_tokenize(raw)# converts to list of words
sent_tokensone = nltk.sent_tokenize(rawone)# converts to list of sentences 
word_tokensone = nltk.word_tokenize(rawone)# converts to list of words


sent_tokens[:2]
sent_tokensone[:2]

word_tokens[:5]
word_tokensone[:5]

lemmer = nltk.stem.WordNetLemmatizer()
def LemTokens(tokens):
    return [lemmer.lemmatize(token) for token in tokens]
remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))


GREETING_INPUTS = ("hello", "hi","hiii","hii","hiiii","hiiii", "greetings", "sup", "what's up","hey",)
GREETING_RESPONSES = ["hi", "hey", "hii there", "hi there", "hello", "I am glad! You are talking to me"]
def greeting(sentence):
    for word in sentence.split():
        if word.lower() in GREETING_INPUTS:
            alexis_speak(random.choice(GREETING_RESPONSES))
            return random.choice(GREETING_RESPONSES)
            

Basic_Q = ("saint francis institute of technology ?","saint francis institute of technology"," saint francis institute of technology","saint francis institute of technology ")
Basic_Ans = "St. Francis Institute of Technology in Mumbai, India is an engineering college named after Francis of Assisi, the 12th-century Italian saint. The college is accredited by the National Board of Accreditation, approved by the AICTE and is affiliated to University of Mumbai."
def basic(sentence):
    for word in Basic_Q:
        if sentence.lower() == word:
            alexis_speak(Basic_Ans)
            return Basic_Ans

Basic_Om = ("aicte","aicte ","All India Council for Technical Education","who is aicte")
Basic_AnsM = ["The All India Council for Technical Education is a statutory body, and a national-level council for technical education, under the Department of Higher Education.","All India Council for Technical Education (AICTE) was set up in November 1945 as a national-level Apex Advisory Body to conduct a survey on the facilities available for technical education and to promote development in the country in a coordinated and integrated manner."]
def basicM(sentence):
    for word in Basic_Om:
        if sentence.lower() == word:
            alexis_speak(random.choice(Basic_AnsM))
            return random.choice(Basic_AnsM)
        
Introduce_Ans = ["My name is Alexis.","My name is Alexis, I'm alexa's cousin","Im alexis","My name is alexis. and my nickname is lex and i am happy to solve your queries :) "]
def IntroduceMe(sentence):
    alexis_speak(random.choice(Introduce_Ans))
    return random.choice(Introduce_Ans)


from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# Generating response
def response(voice_data):
    robo_response=''
    sent_tokens.append(voice_data)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokens)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokens[idx]
        print(robo_response)
        alexis_speak(robo_response)
        
      
# Generating response
def responseone(voice_data):
    robo_response=''
    sent_tokensone.append(voice_data)
    TfidfVec = TfidfVectorizer(tokenizer=LemNormalize, stop_words='english')
    tfidf = TfidfVec.fit_transform(sent_tokensone)
    vals = cosine_similarity(tfidf[-1], tfidf)
    idx=vals.argsort()[0][-2]
    flat = vals.flatten()
    flat.sort()
    req_tfidf = flat[-2]
    if(req_tfidf==0):
        robo_response=robo_response+"I am sorry! I don't understand you"
        return robo_response
    else:
        robo_response = robo_response+sent_tokensone[idx]
        print(robo_response)
        alexis_speak(robo_response)
         
    
def respond(voice_data):
    if 'time' in voice_data:
        alexis_speak(ctime())
        return ctime()
        
    if 'exit' in voice_data:
        return()
    
    voice_data=voice_data.lower()
    keyword = "institute"
    keywordone = " institute"
    keywordsecond = "institute "
        
    if(voice_data!='exit'):
        if(voice_data=='thanks' or voice_data=='thank you' ):
            alexis_speak("You are welcome..")
            return
        elif(basicM(voice_data)!=None):
            return basicM(voice_data)
        elif(basic(voice_data)!=None):
            return basic(voice_data)
        else:
            if(voice_data.find(keyword) != -1 or voice_data.find(keywordone) != -1 or voice_data.find(keywordsecond) != -1):
                return responseone(voice_data)
                sent_tokensone.remove(voice_data)
            elif(greeting(voice_data)!=None):
                return greeting(voice_data)
            elif(voice_data.find("your name") != -1 or voice_data.find(" your name") != -1 or voice_data.find("your name ") != -1 or voice_data.find(" your name ") != -1):
                return IntroduceMe(voice_data)
            
            else:
                return response(voice_data)
                sent_tokens.remove(voice_data)


def alexis_speak(audio_string):
    converter = pyttsx3.init()
    converter.setProperty('rate', 150)
    converter.setProperty('volume', 0.7)
    converter.say(audio_string)
    converter.runAndWait()
    
@app.post("/predict")
def predict():
    text = request.get_json().get("message")
    # TODO: Check if text is valid
    response = respond(text)
    message = {"answer" : response}
    return jsonify(message)

if __name__ == "__main__":
    app.run(debug=True)