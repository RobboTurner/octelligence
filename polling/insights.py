import anthropic
from dotenv import load_dotenv
import pandas as pd
import ast
import json
import os

#  This hallucinates quite a bit
def get_insights(user_query):

    load_dotenv()
    client = anthropic.Anthropic(api_key = os.getenv("ANTHROPIC_KEY"))

    # Load the CSV file into a DataFrame
    df = pd.read_csv('polling/data/polling.csv')

    # Serialize the dictionary to a JSON string
    polling_data_serialised = df.to_json(orient='records')

    # Also convert the DataFrame to a dictionary with the column name as keys and data as lists
    columns_dict = {column: df[column].tolist() for column in df.columns}

    unique_questions = set(columns_dict['question'])

    # Stuff the context with all the data to extract insights.
    system_prompt_search = "Your job is to extract a list of poll questions that are relevant to a users query. Give your response concisely. When responding with insights, give a list of containing the full question, the relevant demographic and the value for that record. Make sure you are quoting the records faithfully, without making anything up."

    user_prompt_search = "polling questions with answers and demographics: " + str(polling_data_serialised) + "\nuser query: " + user_query

    print("Querying the LLM for audience insights...")
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
                        "text": f"{user_prompt_search}"
                    }
                ]
            }
        ]
    )

    initial_completion_content = initial_completion.content[0].text
    return initial_completion_content

    # relevant_questions = ast.literal_eval(initial_completion_content)
    # print(f"{relevant_questions=}")

    # filtered_df = df[df['polling_questions'].str.contains('|'.join(relevant_questions), case=False, na=False)]

    # json_string = filtered_df.to_json(orient='records')

    # print(f"{json_string=}")

    # # Step 2: Extract facts for the given audience and question
    # extraction_completion = client.chat.completions.create(
    #     model="gpt-4-turbo",
    #     messages=[
    #         {"role": "system", "content": "Your job is to identify which 5 audiences are the most sensitive to the questions provided. A sensitive audience is an audience that scored very highly in either the positive or the negative direction. Your response should be a JSON array where each element is a JSON object with the keys 'demographic', 'question', and 'value'."},
    #         {"role": "user", "content": f"{json_string}"}
    #     ]
    # )
    # facts = extraction_completion.choices[0].message  # Assuming the response is a string of facts
    # data = json.loads(facts)

    # output_string = "Using polling results, the following audiences were identified as particularly sensitive:\n"
    # for d in data:
    #     result_string = f"Demographic: {d['demographic']} (question: {d['question']}, response: {d['value']})"
    #     output_string.append(result_string)
    return output_string

# Example usage:
user_query = "I am giving a speech on policing in the North East."
result = get_insights(user_query)
print(result)
