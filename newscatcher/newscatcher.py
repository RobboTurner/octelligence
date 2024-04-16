model = ChatAnthropic(model_name='claude-3-haiku-20240307', temperature=0.6, api_key=api_key)
def generate_terms(topic = "policing"):
    total_prompt = f"""Generate diverse search terms for news articles based on this topic {topic}
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
    query_result = ""
    for word in terms:
        if word == terms[-1]:
            query_result += "(" + word + ")"
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
                                      search_in="summary",
                                      lang = "en",
                                      predefined_sources = "top 30 GB",
                                      from_ = "2 days ago",
                                      clustering_enabled = True,
                                      page_size = 1000,
                                      include_nlp_data = True)

def extract_article_summaries(newscatcher_output):
    cluster_list = [x["articles"] for x in newscatcher_output.dict()["clusters"]][:5]
    summary_list = []
    for cluster in cluster_list:
        summary_text=""
        for article in cluster:
            summary_text += " ``` " + article["nlp"]["summary"]
        summary_list.append(summary_text)
        
    return summary_list

def generate_cluster_summary(summary_list):
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
                            "text": f'Summarise the following content separated by ``` into one sentance: {summary}.'
                            
                        }
                    ]
                }
            ]
        )
        succinct_summary.append(message.content)
    return succinct_summary 

