# This file is part of ETHAM.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
#ETHAM by Zacarias Juliano Capingala - Comunidadedo Saber
import os
import json
from difflib import get_close_matches


#Create a new file in case that don't exist
def create_file(file_name: str):
    content: dict = {
            "questions": [
                {
                "question": "Olá...",
                "answer": "Olá mundo..."
                },
                {
                "question": "ola",
                "answer": "Ola mundo..."
                }
            ]
        }

    if os.path.exists(file_name):
        return

    with open(file_name, 'w') as data:
        json.dump(content, data, indent=2)


#Load the content of a file
def read_file_content(file_path: str) -> dict or None:
    if os.path.exists(file_path):  
        with open(file_path, 'r') as file:
            data: dict = json.load(file)
        return data
    else:      
        return create_file(file_path)


#Save the new question and answer
def update_file_content(file_path: str, data: dict):
    if not os.path.exists(file_path):
        return None
    
    with open(file_path, 'w') as file:        
        json.dump(data, file, indent=2)


def delete_file(file_path):
    if not os.path.exists(file_path):
        print(f'O arquivo "{file_path}" não existe. Não é possível excluir.')
        return

    os.remove(file_path)
    print(f'Arquivo "{file_path}" excluído com sucesso.')


#Search for the answer
def find_best_match(user_question: str, questions: list) -> str or None:
    matches: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return matches[0] if matches else None


#Get the answer of a question
def get_answer_for_question(question: str, knowledge_base: dict) -> str or None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]


#Validate the user input
def get_input(info: str):
    MIN_INPUT_LENGTH = 1
    MAX_INPUT_LENGTH = 250
    
    user_input = input(info)

    if MIN_INPUT_LENGTH <= len(user_input) <= MAX_INPUT_LENGTH:
        return user_input[:MAX_INPUT_LENGTH]
    else:
        return 'quit'


#ETHAM     
def chat_bot(knowledge_base):    
    while True:
        user_input: str = get_input('Você: ')

        if user_input.lower() == 'quit':
            break

        best_match: str or None = find_best_match(user_input.lower(), [q["question"].lower() for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base)
            print(f'Chat: {answer} \n')

        else:
            print('Chat: Não sei como reponder.')
            new_answer: str = get_input('Podes me ensinar a resposta: ')

            if new_answer.lower() == 'quit':
                pass
            elif new_answer.lower() != 'not':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                update_file_content(file, knowledge_base)
                print('Chat: Agora aprendi.')
            print("")


#Start the ChatBot
if __name__ == '__main__':

    while True:
        username:str = get_input('LOGIN: ')
        
        if username.lower() == 'quit':
            break

        file: str = username.lower() + '.json'
        knowledge_base: dict = read_file_content(file)

        if knowledge_base == None:
            print(f'O arquivo "{file}" não existe.\n Foi criado um novo arquivo para vocẽ poder usar.\n')
        else:
            chat_bot(knowledge_base)

    