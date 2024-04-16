from openai import OpenAI
from dotenv import load_dotenv
import pandas as pd
import ast
import json

def query_openai_with_polling_data(user_query):

    # Load the CSV file into a DataFrame
    df = pd.read_csv('polling/data/polling.csv')
    print(df.describe())

    # Convert the DataFrame to a dictionary with the column name as keys and data as lists
    columns_dict = {column: df[column].tolist() for column in df.columns}

    unique_questions = set(columns_dict['question'])

    # Serialize the dictionary to a JSON string
    polling_data_serialised = df.to_json(orient='records')

    # json_string now contains all data in a JSON formatted string

    load_dotenv()
    client = OpenAI()
    # print(f"{user_query=}")
    # print(f"{polling_data_serialised=}")


    # Step 1: Query LLM to get relevant questions
    initial_completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Your job is to extract a list of poll questions that are relevant to a users query. The format of your response should be a json array of the relevant questions. The json array should be a single level. In your returned response, use the exact wording of the questions."},
            {"role": "user", 
             "content": "polling questions with answers and demographics: " + str(polling_data_serialised) + 
             "\nuser query: " + user_query}
        ]
    )

    initial_completion_content = initial_completion.choices[0].message.content
    relevant_questions = ast.literal_eval(initial_completion_content)
    print(f"{relevant_questions=}")

    filtered_df = df[df['polling_questions'].str.contains('|'.join(relevant_questions), case=False, na=False)]

    json_string = filtered_df.to_json(orient='records')

    print(f"{json_string=}")

    # Step 2: Extract facts for the given audience and question
    extraction_completion = client.chat.completions.create(
        model="gpt-4-turbo",
        messages=[
            {"role": "system", "content": "Your job is to identify which 5 audiences are the most sensitive to the questions provided. A sensitive audience is an audience that scored very highly in either the positive or the negative direction. Your response should be a JSON array where each element is a JSON object with the keys 'demographic', 'question', and 'value'."},
            {"role": "user", "content": f"{json_string}"}
        ]
    )
    facts = extraction_completion.choices[0].message  # Assuming the response is a string of facts
    data = json.loads(facts)

    output_string = "Using polling results, the following audiences were identified as particularly sensitive:\n"
    for d in data:
        result_string = f"Demographic: {d['demographic']} (question: {d['question']}, response: {d['value']})"
        output_string.append(result_string)
    return output_string

# Example usage:
user_query = "I am giving a speech on policing in the North East."
result = query_openai_with_polling_data(user_query)
print(result)
