import json
from datetime import datetime, timedelta
from openai import OpenAI
import random

# --------------------------------------------------------------
# Use OpenAI's Function Calling Feature for a Cloud Computing Quiz
# --------------------------------------------------------------

client = OpenAI(api_key="") # <================== insert own API key here

# --------------------------------------------------------------
# Use OpenAI's Function Calling Feature for a Cloud Computing Quiz
# --------------------------------------------------------------

function_descriptions = [
    {
        "name": "generate_quiz",
        "description": "Generate a quiz with multiple question types for cloud computing topics",
        "parameters": {
            "type": "object",
            "properties": {
                "difficulty": {
                    "type": "string",
                    "description": "The difficulty level of the quiz (e.g., 'Easy', 'Medium', 'Hard')",
                },
                "topics": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "The cloud computing topics to include in the quiz (e.g., 'Virtualization', 'Cloud Storage', 'Load Balancing')",
                    },
                },
                "num_questions": {
                    "type": "integer",
                    "description": "The total number of questions to generate for the quiz",
                },
                "question_types": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "description": "The types of questions to include in the quiz (e.g., 'MCQ', 'Short Answer', 'Essay')",
                    },
                },
            },
            "required": ["difficulty", "topics", "num_questions", "question_types"],
        },
    }
]

user_prompt = "Generate a quiz with 5 questions, including MCQ, Short Answer, and Essay questions, on \
the topics of 'Serverless Computing' and 'Cloud Security' with a medium difficulty level."

completion = client.chat.completions.create(
    model="gpt-3.5-turbo-0613",
    messages=[{"role": "user", "content": user_prompt}],
    functions=function_descriptions,
    function_call="auto",
)

output = completion.choices[0].message
print(output)
print('\n')

# # --------------------------------------------------------------
# # Add a Function to Generate Quiz Questions
# # --------------------------------------------------------------
def generate_quiz(difficulty, topics, num_questions, question_types):
    """Generate a quiz with multiple question types for cloud computing topics."""

    # Generate questions based on the specified parameters
    for _ in range(num_questions):
        question_type = random.choice(question_types)
        topic = random.choice(topics)

        # Generate a question and answer using the language model
        question_prompt = f"Generate a {question_type} question on the topic of '{topic}' with a {difficulty} difficulty level, and provide the answer with explanations."
        if question_type == "MCQ":
            question_prompt += " Include the options and indicate the correct answer."

        question_completion = client.chat.completions.create(
            model="gpt-3.5-turbo-0613",
            messages=[{"role": "user", "content": question_prompt}],
        )
        question_output = question_completion.choices[0].message.content
        print(question_output)
        print('\n')

# # Use the LLM output to manually call the function
params = json.loads(output.function_call.arguments)
chosen_function = eval(output.function_call.name)
chosen_function(**params)