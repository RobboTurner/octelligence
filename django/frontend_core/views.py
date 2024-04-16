from django.shortcuts import render,Http404
from django.http import HttpResponse 
from django.http import JsonResponse
import sys
sys.path.append('../')


#from tts.tts import tts
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from generator.generator import question_generator
from newscatcher.newscatcher import query_newscatcher


def home_view(request):
    return render(request,'homepage.html')


def handle_search_query(request):
    if request.method == "POST":
        # Get input text from user searc h
        input_text = request.POST.get('inputText')  
        # Pass this into the question generator and return the output in the UI
        newcatcher_output = query_newscatcher(input_text)
        print(newcatcher_output)
        llm_output = question_generator(newcatcher_output,"Happy")
        #out = llm_output[0][0].text
        #print(out)
    else:
        question = "Please submit some input."
    return render(request, 'homepage.html', {'question': llm_output})
 

#def text_to_speech(request):
#    llm_output = question_generator(input_text,news_articles, user_input_styles)
#    if request.method == "POST":
#    wav_file = tts(llm_output)
#    else:
#        ""
###    input_text = request.POST.get('inputText')  
#    return render(request, 'homepage.html', {'question': llm_output})
#       question = "Please submit some input."
  #  return render(request, 'homepage.html', {'question': wav_file})

    