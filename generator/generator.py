import anthropic
import os 
from dotenv import load_dotenv, dotenv_values

load_dotenv() 
api_key = os.getenv("ANTHROPIC_KEY")

client = anthropic.Anthropic(
    api_key=api_key,
)

def question_generator(articles:dict,
                       style: str,
                       prompt: str = "ministerial interview"):
        message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="""
        You are a journalist crafting a single challenging question for a press conference with a government minister.
            
            Your question should be direct, provocative, and concise. Only include the question and not context for the prompt.

            
            """,  # <-- system prompt
        messages=[
            {
                "role": "user",
                
                "content": [
                    {
                        "type": "text",
                        "text": f'Based on the articles provided: {articles}, craft a question in the style of a {style} journalist in the context of {prompt}.   DO NOT INCLUDE THE NAME OR TITLE OF THE PERSON YOU ARE INTERVIEWING. The questioner may not be the subject of the news story.'

                    }
                ]
            }
        ]
    )
        return print(message.content)
