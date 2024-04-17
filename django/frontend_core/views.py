from django.shortcuts import render,Http404
from django.http import HttpResponse 
from django.http import JsonResponse
import sys
sys.path.append('../')


#from tts.tts import tts
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt

from generator.generator import question_generator
from newscatcher.newscatcher import newscatcher_main


#from polling.insights import get_insights
from polling.audience_id import get_audiences



def home_view(request):
    return render(request,'homepage.html')


def handle_search_query(request):
    if request.method == "POST":
        # Get input text from user searc h
        input_text = request.POST.get('inputText')  
        question_generator_mood = request.POST.get('Radio_input')  
        print(question_generator_mood)
        # Pass this into the question generator and return the output in the UI
        newcatcher_output = newscatcher_main(str(input_text))
        
        # Get the top five articles from the news catch_output 
        top_5_articles = [newcatcher_output[0][0].text,
                          newcatcher_output[1][0].text,
                          newcatcher_output[2][0].text,
                          newcatcher_output[3][0].text,
                          newcatcher_output[4][0].text]
  

        llm_output_1 = question_generator(top_5_articles,question_generator_mood)
        llm_output_2 = question_generator(top_5_articles,question_generator_mood)
        llm_output_3 = question_generator(top_5_articles,question_generator_mood)

        questions = [llm_output_1[0].text,llm_output_2[0].text,llm_output_3[0].text]

        polling_data = get_audiences(input_text)

    else:
        question = "Please submit some input."
    return render(request, 'homepage.html', {'articles': top_5_articles,'questions_dict': questions, 'polling_data':polling_data})



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

