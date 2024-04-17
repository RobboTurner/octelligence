import os
import sqlite3
import pandas as pd
import ast
from dotenv import load_dotenv
import anthropic

def get_audiences(user_query):
    load_dotenv()
    client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_KEY"))

    # Connect to SQLite database
    conn = sqlite3.connect('/Users/mawuliagamah/gitprojects/octelligence/polling/data/polling.db')
    cursor = conn.cursor()

    # Fetch all unique questions from the database
    cursor.execute('SELECT DISTINCT question FROM polling')
    questions = cursor.fetchall()
    unique_questions = [q[0] for q in questions]

    # Serialize the unique questions to a JSON string
    questions_json = pd.Series(unique_questions).to_json(orient='values')

    # Define the system prompt for the LLM
    system_prompt_search = "Identify the questions most sensitive to the user's topic of interest from the following list. Return only a JSON array of relevant questions. Do not return anything except a JSON array. Return the questions exactly as they appear from the user."
    
    # Query the LLM
    print("Querying the LLM for relevant questions...")
    initial_completion = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system=system_prompt_search,
        messages=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": f"{questions_json}\nuser query: {user_query}"
                    }
                ]
            }
        ]
    )

    # Evaluate the LLM's output
    relevant_questions = ast.literal_eval(initial_completion.content[0].text)

    # Query the database for each relevant question to find demographics with the highest and lowest scores
    demographic_info = {}
    for question in relevant_questions:
        # Fetch demographic with the highest score
        cursor.execute('SELECT demographic, MAX(value) FROM polling WHERE question = ?', (question,))
        max_result = cursor.fetchone()
        if max_result[0] not in demographic_info:
            demographic_info[max_result[0]] = []
        demographic_info[max_result[0]].append((question, 'Highest', max_result[1]))

        # Fetch demographic with the lowest score
        cursor.execute('SELECT demographic, MIN(value) FROM polling WHERE question = ?', (question,))
        min_result = cursor.fetchone()
        if min_result[0] not in demographic_info:
            demographic_info[min_result[0]] = []
        demographic_info[min_result[0]].append((question, 'Lowest', min_result[1]))

    # Construct the summary string grouped by demographic
    summary = []
    for demographic, details in demographic_info.items():
        evidence = "; ".join([f"Question: '{d[0]}', {d[1]} (value: {d[2]})" for d in details])
        summary.append(f"Demographic: {demographic} - {evidence}")

    #summary = "\n".join(summary)

    # Close database connection
    conn.close()

    return summary

user_query = "I am giving a speech on policing in the North East."
# summary = get_audiences(user_query)
# print(summary)