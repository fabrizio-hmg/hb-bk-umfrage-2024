import os
from textwrap import dedent

from openai import OpenAI
from pydantic import BaseModel


class Answer(BaseModel):
    insight: str


class Insight():
    prompt = '''
        Act like a seasoned Senior Data Analyst with over a decade of experience.
        You will receive a dataset and a specific question related to it. 
        
        Your task is to:

        1. Analyze the entire dataset thoroughly.
        2. Understand the given question and its context.
        3. Generate insightful and accurate answers STRICTLY based on the provided dataset.
    
        Your response must adhere to the following structure:
        - Insight: Provide a clear and concise answer to the question based on the provided dataset. Be as detailed or brief as necessary to fully address the question.
    '''

    def __init__(self, api_key = os.getenv('OPENAI_API_KEY'), model = 'gpt-4o-mini'):
        self.api_key = api_key
        self.model = model
        self.client = OpenAI(api_key = self.api_key)

    def generate_insight(self, df, question):
        completion = self.client.beta.chat.completions.parse(
            model = self.model,
            messages = [
                {'role': 'system', 'content': dedent(self.prompt)},
                {'role': 'user', 'content': f'Dataset: {df} | Question: {question}'}
            ],
            response_format = Answer
        )

        return completion.choices[0].message.parsed
    