from django.shortcuts import render, redirect

# Create your views here.
from django.http import HttpResponse

from .models import *
from .form import *



from chatterbot.trainers import ChatterBotCorpusTrainer
from chatterbot import ChatBot
from chatterbot.trainers import ListTrainer
import re
import warnings
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy import sparse
import numpy as np
import nltk
import string
#import speech_recognition as sr  
import pyttsx3
from sklearn.metrics.pairwise import cosine_similarity


def preprocess_sentence(sentence):
  sentence = sentence.lower().strip()
  sentence = sentence.strip()
  # creating a space between a word and the punctuation following it
  # eg: "he is a boy." => "he is a boy ."
  sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
  sentence = re.sub(r'[" "]+', " ", sentence)
  # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",")
  sentence = re.sub(r"[^a-zA-Z?.!,]+", " ", sentence)
  sentence = sentence.strip()
  # adding a start and an end token to the sentence
  return sentence
def code(request,q):
	my_bot = ChatBot(name='PyBot', read_only = True, logic_adapters = 
                 ['chatterbot.logic.BestMatch'])
	file=open("/home/rakshith/Downloads/techfest/chatbot/dataset2.txt")
	small_talk=file.readlines()
	for i in range(len(small_talk)):
		small_talk[i]=preprocess_sentence(small_talk[i])
	#list_trainer = ListTrainer(my_bot)
	#list_trainer.train(small_talk)
	warnings.filterwarnings('ignore')
	vectorizer=TfidfVectorizer()
	data=vectorizer.fit(small_talk)
	data=vectorizer.transform(small_talk)
	data=list(data.toarray())


	x=''
	for i in range(1):
	    test=q
	    #test=input()
	    test=[test]
	    test_vec=vectorizer.transform(test)
	    
	    data.append(test_vec.toarray()[0])
	    #print(test_vec.toarray())
	    data1=np.mat(data)
	    vals=cosine_similarity(np.array(data1[-1]),data1)
	    #print(len(vals[0]),len(small_talk))
	    #print(my_bot.get_response(small_talk[np.argmax(vals[0][:-1])]))

	    # initialisation 
	    engine = pyttsx3.init()
	    rate = engine.getProperty('rate')
	    engine.setProperty('rate', 120) 

	  
	    state=my_bot.get_response(small_talk[np.argmax(vals[0][:-1])])
	    x=state
	    #engine.setProperty('volume',1)

	    engine.say(my_bot.get_response(small_talk[np.argmax(vals[0][:-1])]))

	    engine.runAndWait()
	return x




def index(request):
	chat = Chatbot.objects.all()
	#answer1=Ans.objects.all()
	#anss=Ans()

	anss=Chatbot()
	
	form = ChatForm()
	if request.method =='POST':
		form = ChatForm(request.POST)
		q=request.POST
		p=q.get('title')
		print(p)
		
		x=code(request,p)
		print(x,">>>>>>>>>>>>>>>>>>>>>>>>>")
		if form.is_valid():
			form.save()
			anss.title=x
			anss.save()
			
		return redirect('/')

	context = {'chat': chat, 'form': form}
	
	
	return render(request,'index.html',context)