import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.organization = "org-3eNk6Uvt78Hq699icvIDvLg5"
openai.api_key = os.getenv("OPENAI_API_KEY")

models = {
    "chat":"text-davinci-003",
    "edit_text":"text-davinci-edit-001",
    "edit_code":"code-davinci-edit-001",
}

def chat(prompt):
    response = openai.Completion.create(
        model=models['chat'],
        prompt=prompt,
        temperature=0.1,
        max_tokens=64,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response['choices'][0]['text'].strip()

def edit_text(prompt, instruction):
    response = openai.Edit.create(
    model=models['edit_text'],
    input=prompt,
    instruction=instruction
    )
    return response['choices'][0]['text'].strip()

def edit_code(prompt, instruction):
    response = openai.Edit.create(
    model=models['edit_code'],
    input=prompt,
    instruction=instruction
    )
    return response['choices'][0]['text'].strip()

def generate_image(prompt):
    response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="512x512"
    )
    return response['data'][0]['url']

if __name__ == "__main__":
    lines = []
    while True:
        user_input = input()
        if user_input == '':
            break
        else:
            lines.append(user_input + '\n')
    
    code=''.join(lines)
    inst=input("inst: ")
    print(edit_code(code, inst))
    # print(generate_image(prompt))
# print(response['choices'][0]['text'])


# curl https://api.openai.com/v1/completions \
# -H "Content-Type: application/json" \
# -H "Authorization: Bearer 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" \
# -d '{"model": "text-davinci-003", "prompt": "Say this is a test", "temperature": 0, "max_tokens": 7, "echo": true, "stream": true}'
#include <stdio.h>
# int main() { printf("Hello, World!");return 0;}

