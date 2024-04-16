import anthropic
import os 
from dotenv import load_dotenv, dotenv_values

load_dotenv() 
api_key = os.getenv("ANTHROPIC_KEY")

client = anthropic.Anthropic(
    api_key=api_key,
)

news_articles = {
    "Article_1": "Advances in Quantum Computing Set to Revolutionize Data Security - Recent breakthroughs in quantum computing are poised to transform the landscape of data security, with new algorithms capable of solving complex encryption problems that are currently unsolvable with classical computers. Experts predict that within the next decade, quantum computers will begin to impact every industry reliant on data security, from banking to national defense. Leading the charge, QuantumTech Inc. announced a successful test of their prototype quantum processor that promises to enhance cryptographic processes exponentially.",
    "article_2": "Global Health Initiatives Target Malaria Eradication by 2030 - In an ambitious push to eradicate malaria, several global health organizations have launched a new campaign aimed at eliminating the disease by 2030. Leveraging recent advancements in vaccine development and distribution logistics, the initiative focuses on sub-Saharan Africa, where malaria incidence is highest. The World Health Organization (WHO) has pledged support, providing new funding and resources to affected regions. Success in this initiative could save millions of lives and dramatically improve public health outcomes in dozens of countries.",
    "article_3": "Urban Greening: Cities Adopt Eco-Friendly Infrastructure - Cities around the world are increasingly turning to green infrastructure to combat the effects of climate change and urban sprawl. From rooftop gardens to permeable pavements, urban planners are integrating nature-based solutions into the fabric of city planning. Environmentalists applaud these efforts, citing significant improvements in air quality and reductions in urban heat islands. These initiatives not only enhance the quality of urban life but also serve as vital components in the fight against global warming."
}


user_input_styles = {
    "Hostile" : "Hostile journalsit",
    "Friendly": "Friendly journalsit"
}

user_input_styles['Hostile']


def question_generator(articles:dict,style:dict):
        message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system="You are a journalist crafting a single challenging question for a press conference with the prime minister. Your question should be direct, provocative, and concise.",  # <-- system prompt
        messages=[
            {
                "role": "user",
                
                "content": [
                    {
                        "type": "text",
                        "text": f'Based on the articles provided: {articles}, craft a question in the style of a {style["Hostile"]} journalist.'

                    }
                ]
            }
        ]
    )
        return print(message.content)


def main():
    question_generator(news_articles,user_input_styles)


if __name__ == "__main__":
    main()