from django.shortcuts import render,Http404
from django.http import HttpResponse 
from django.http import JsonResponse
import sys
sys.path.append('../')
from generator.generator import question_generator
from tts.tts import tts
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt




def home_view(request):
    return render(request,'homepage.html')


news_articles = {
    "Article_1": "Advances in Quantum Computing Set to Revolutionize Data Security - Recent breakthroughs in quantum computing are poised to transform the landscape of data security, with new algorithms capable of solving complex encryption problems that are currently unsolvable with classical computers. Experts predict that within the next decade, quantum computers will begin to impact every industry reliant on data security, from banking to national defense. Leading the charge, QuantumTech Inc. announced a successful test of their prototype quantum processor that promises to enhance cryptographic processes exponentially.",
    "article_2": "Global Health Initiatives Target Malaria Eradication by 2030 - In an ambitious push to eradicate malaria, several global health organizations have launched a new campaign aimed at eliminating the disease by 2030. Leveraging recent advancements in vaccine development and distribution logistics, the initiative focuses on sub-Saharan Africa, where malaria incidence is highest. The World Health Organization (WHO) has pledged support, providing new funding and resources to affected regions. Success in this initiative could save millions of lives and dramatically improve public health outcomes in dozens of countries.",
    "article_3": "Urban Greening: Cities Adopt Eco-Friendly Infrastructure - Cities around the world are increasingly turning to green infrastructure to combat the effects of climate change and urban sprawl. From rooftop gardens to permeable pavements, urban planners are integrating nature-based solutions into the fabric of city planning. Environmentalists applaud these efforts, citing significant improvements in air quality and reductions in urban heat islands. These initiatives not only enhance the quality of urban life but also serve as vital components in the fight against global warming."
}


user_input_styles = {
    "Hostile" : "Hostile journalsit",
    "Friendly": "Friendly journalsit"
}


def handle_search_query(request):
    if request.method == "POST":
        # Get input text from user searc h
        input_text = request.POST.get('inputText')  
        # Pass this into the question generator and return the output in the UI
        #llm_output = query_news(input_text)
        llm_output = question_generator(input_text,news_articles, user_input_styles)

    else:
        question = "Please submit some input."
    return render(request, 'homepage.html', {'question': llm_output})
 

#def text_to_speech(request):
#    if request.method == "POST":
#    llm_output = question_generator(input_text,news_articles, user_input_styles)
##    input_text = request.POST.get('inputText')  
#    wav_file = tts(llm_output)
#    else:
#        ""
#    return render(request, 'homepage.html', {'question': llm_output})
  #      question = "Please submit some input."
  #  return render(request, 'homepage.html', {'question': wav_file})

    