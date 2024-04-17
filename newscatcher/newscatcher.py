
import anthropic
import pandas as pd
import os
import re
from pprint import pprint
from newscatcherapi_client import Newscatcher, ApiException
from langchain_anthropic import ChatAnthropic
from langchain_core.prompts import ChatPromptTemplate
import pandas as pd 


from dotenv import load_dotenv, dotenv_values


load_dotenv() 
claude_api_key = os.getenv("ANTHROPIC_KEY")
news_catcher_api_key = os.getenv("NEWS_CATCHER_API")


newscatcher = Newscatcher(api_key = news_catcher_api_key)

client = anthropic.Anthropic(api_key = claude_api_key)


model = ChatAnthropic(model_name='claude-3-haiku-20240307', temperature=0.6, api_key=claude_api_key)
def generate_terms(topic = "policing"):
    total_prompt = f"""Generate diverse single word search terms for news articles based on this topic {topic}
    Only return a python list of keywords.
    """
    output = model.invoke(total_prompt)
    terms = extract_bracket_contents(output.content)
    return terms
def extract_bracket_contents(text):
    pattern = r'\[(.*?)\]'  # Pattern to find text inside brackets
    list_of_terms  = re.findall(pattern, text)[0].split(",")
    return [text.strip(" '") for text in list_of_terms]

def create_newscatcher_query(terms):
    query_result = "("
    for word in terms:
        if word == terms[-1]:
            query_result += "(" + word + ")) AND Britain"
        else:
            query_result += "(" + word + ")" + " OR "
    return query_result

def query_newscatcher(query=""):
    if query == "":
        return newscatcher.search.get(q="Britain",
                                      search_in="content",
                                      lang = "en",
                                      theme = "Politics",
                                      predefined_sources = "top 30 GB",
                                      from_ = "2 days ago",
                                      clustering_enabled = True,
                                      page_size = 1000,
                                      include_nlp_data = True)
    else:
        return newscatcher.search.get(q=query,
                                      search_in="content",
                                      lang = "en",
                                      predefined_sources = "top 100 GB",
                                      from_ = "7 days ago",
                                      clustering_enabled = True,
                                      page_size = 1000,
                                      include_nlp_data = True)


def extract_summary_texts(newscatcher_output):
    summary_list = []
    cluster_list = [x["articles"] for x in newscatcher_output.dict()["clusters"]][:5]
    for cluster in cluster_list:
        summary_text=""
        for article in cluster:
            summary_text += " ``` " + article["nlp"]["summary"]
        summary_list.append(summary_text)
        
    return summary_list   


def generate_summary(summary_list):
    succinct_summary = []
    for summary in summary_list:
        message = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=1000,
            temperature=0,
            messages=[
                {
                    "role": "user",
                    
                    "content": [
                        {
                            "type": "text",
                            "text": f'Summarise the following content separated by ``` into one sentance: {summary}. Keep each summary at max, 32 words.'
                            
                        }
                    ]
                }
            ]
        )
        succinct_summary.append(message.content)
    return succinct_summary 



def newscatcher_main(query):
    test_terms = generate_terms(query)
    test_query = create_newscatcher_query(test_terms)
    test_nc_output = query_newscatcher(test_query)
    test_summary_text = extract_summary_texts(test_nc_output)
    test_output = generate_summary(test_summary_text)
    return test_output
