import argparse
from agent import Agent
from utils import *
from agent_literal import *
import time
import os
import datetime

def get_multiline_input():
    print("=========\nEnter your answer (type 'END' on a new line when finished):\n=========")
    lines = []
    while True:
        line = input()
        if line.strip().upper() == 'END':
            break
        lines.append(line)
    return '\n'.join(lines)

def chat(query,query_additional, agent1, agent2, project, persistent_memory, chatter, chat_history):
    prompt = f"""
    I am {agent1.literal}.
    You are {agent2.literal}.
    Our customer wants us to build a project with the following description: {project}.
    """
    if len(persistent_memory) > 0:
        prompt += f"\n{str(persistent_memory)}\n"
    if len(chat_history) > 0:
       for i in range(len(chat_history)):
           prompt += f"{chat_history[i]}\n"
    prompt += f"{query} {query_additional}"
    response = chatter.communicate(prompt)
    return response


def ask_for_user_clarification(project,persistent_memory):
    chatter = OpenAIBackend()
    ceo = Agent("CEO")
    clarification = ""
    query = f"You are {ceo.literal}. Our customer has a project idea: {project}. If you need clarification from the customer, please provide the questions for the customer. Please try not to ask too many questions. Please put the questions in a json format with \"questions\" as the key and the questions you want to ask as the value."
    response = chatter.communicate(query)
    if type(response) == str:
        questions = json.loads(response)['questions']
    else:
        questions = response['questions']
    print("\nHello, I am "+ceo.literal+". It is our pleasure to work with you on the project: "+project+". Please answer the following questions for clarification:\n===\n"+'---\n'.join(questions))
    answer = get_multiline_input()
    while True:
        query = f"The customer has answered your questions with the following: {answer}. Please determine if you need more information from the customer. If so, please put the questions for the customer in a json format with \"questions\" as the key and the questions you want to ask as the value. If not, please put \"no\" as the value."
        response = chatter.communicate(query,reset=False)
        if len(response) < 10:
            questions = 'no'
        else:   
            if type(response) == str:
                questions = json.loads(response)['questions']
            else:
                questions = response['questions']
        if questions == "no":
            query = f"Please summarize the customer's answers to your questions and provide a clear and concise summary. Please put the summary in a json format with \"summary\" as the key and the summary as the value."
            response = chatter.communicate(query,reset=False)
            summary = str(response['summary'])
            clarification = summary
            break
        else:
            print("\nThanks for the clarification. Please answer the following new questions for further clarification:\n===\n"+'---\n'.join(questions))
            answer = get_multiline_input()
    return clarification


def system_designing(project,persistent_memory):
    chatter = OpenAIBackend()
    ceo = Agent("CEO")
    cpo = Agent("SystemDesigner")
    chat_history = []
    query = "Please design the system architecture for the project required by the customer. Please provide a detailed list of all the files that need to be created, and the functions and classes that need to be written. Please don't include any files that are not in text format because our company doesn't support non-text files."
    query_additional = "For the system design, write in json format with system_design as the key."
    response = chat(query,query_additional, ceo, cpo, project, persistent_memory, chatter, chat_history)
    system_design = str(response['system_design'])
    print("System design:",system_design)
    chat_history.append(agents_names[ceo.role]+": "+query)
    chat_history.append(agents_names[cpo.role]+": "+system_design)
    return system_design


def code_writing(project,persistent_memory):
    chatter = OpenAIBackend()
    cpo = Agent("CPO")
    programmer = Agent("Programmer")
    chat_history = []
    query = "Please write the code for the project required by the customer. Please use the system design provided to you to write the code."
    query_additional = "For the code writing, write in json format with file path as the key and code as the value."
    response = chat(query,query_additional, cpo, programmer, project, persistent_memory, chatter, chat_history)
    code = response
    print("Code:",str(response))
    return code


def code_reviewing(project,persistent_memory):
    chatter = OpenAIBackend()
    programmer = Agent("Programmer")
    code_reviewer = Agent("CodeReviewer")
    cpo = Agent("CPO")
    n_rounds = 5
    code = persistent_memory['code']
    for i in range(n_rounds):
        start_time = time.time()
        print(f"=========\nBegin code reviewing (Round {i+1}/{n_rounds})\n=========")
        chat_history = []
        query = f"Please review the code for the project required by the customer. Please use the system design provided to you to review the code and provide feedback to me. The major focus it to ensure the code is correct and complete so that our customer can directly run the code without any modification. This is the {i+1}th round of a {n_rounds} rounds of code reviewing."
        query_additional = 'If you are satisfied with the code because the code is correct and complete, please answer with "<ReviewComplete>" tag. If you are not satisfied with the code because the code is not correct or complete, please provide your feedback without "<ReviewNotComplete>" tag.'
        response = chat(query,query_additional, cpo, code_reviewer, project, persistent_memory, chatter, chat_history)
        if "<ReviewComplete>" in response:
            print("Code reviewing is complete.")
            break
        #chat_history.append(agents_names[code_reviewer.role]+": "+response)
        query = "Please write the code again based on the feedback provided by the code reviewer."
        query_additional = "For the code writing, write in json format with file path as the key and code as the value."
        response = chat(query,query_additional, cpo, programmer, project, persistent_memory, chatter, chat_history)
        code = response
        persistent_memory['code'] = code
        end_time = time.time()
        print(f"Time taken: {end_time-start_time} seconds")
    return code

def readme_writing(project,persistent_memory):
    chatter = OpenAIBackend()
    ceo = Agent("CEO")
    cpo = Agent("CPO")
    chat_history = []
    query = "Please write the readme.md file for the project required by the customer. Please use the system design provided to you to write the readme.md file."
    query_additional = "Please put the content of readme.md in a json format with readme as the key and the content as the value."
    response = chat(query,query_additional, ceo, cpo, project, persistent_memory, chatter, chat_history)
    readme_file = str(response['readme'])   
    return readme_file


def requirements_writing(project,persistent_memory):
    chatter = OpenAIBackend()
    ceo = Agent("CEO")
    cpo = Agent("CPO")
    chat_history = []
    query = "Please write the requirements file for the project required by the customer. "
    query_additional = "Please put the content of requirements in a json format with the file name (e.g., requirements.txt for python projects) as the key and the content as the value."
    response = chat(query,query_additional, ceo, cpo, project, persistent_memory, chatter, chat_history)
    requirements_file = response
    return requirements_file


def project_path_determination(project,persistent_memory):
    chatter = OpenAIBackend()
    ceo = Agent("CEO")
    cpo = Agent("CPO")
    chat_history = []
    query = "Please determine the project name for the project required by the customer. It will be used as the folder name for the project so please don't use any special characters or spaces."
    query_additional = "Please put the content of project name in a json format with name as the key and the content as the value."
    response = chat(query,query_additional, ceo, cpo, project, persistent_memory, chatter, chat_history)
    project_path = str(response['name'])
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    project_path = f"{project_path}_{timestamp}"
    return project_path

def write_to_file(persistent_memory):
    base_path = 'work_space/'
    project_path = persistent_memory['project_path']

    if not os.path.exists(base_path):
        os.makedirs(base_path)
    if not os.path.exists(base_path + project_path):
        os.makedirs(base_path + project_path)
    base_path = base_path + project_path + '/'
    os.rename('conversation_history.txt',base_path+'conversation_history.txt')
    system_design = persistent_memory['system_design']
    code = persistent_memory['code']
    readme = persistent_memory['readme']
    if 'clarification' in persistent_memory:
        clarification = persistent_memory['clarification']
        with open(base_path + 'clarification.txt', 'w') as f:
            f.write(clarification)
    with open(base_path + 'system_design.txt', 'w') as f:
        f.write(system_design)
    requirements = persistent_memory['requirements']
    for k,v in requirements.items():
        with open(base_path + k, 'w') as f:
            if type(v) == dict:
                v = json.dump(v, f, indent=4)
            elif type(v) == list:
                v = '\n'.join(v)
                f.write(v)
            elif type(v) == str:
                f.write(v)
    for file_path, code in code.items():
        full_path = os.path.join(base_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(code)   
    with open(base_path + 'readme.md', 'w') as f:
        f.write(readme)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='argparse')
    parser.add_argument('--project', type=str, default="Develop a snake game with pygame",
                    help="The project you want us to work on")
    parser.add_argument('--clarification', type=bool, default=False,
                    help="Whether you want to ask the customer for clarification")

    args = parser.parse_args()

    f = open("conversation_history.txt", "w")
    f.close()

    project = args.project
    clarification = args.clarification
    print(f"Project: {project}")

    persistent_memory = {}

    if clarification:
        print("=========\nBegin user clarification\n========="  )
        start_time = time.time()
        clarification = ask_for_user_clarification(project,persistent_memory)
        if len(clarification) > 0:
            persistent_memory['clarification'] = clarification
        end_time = time.time()
        print("=========\nEnd user clarification\n=========")
        print("Time taken:",end_time-start_time)



    print("=========\nBegin system design\n=========")
    start_time = time.time()

    system_design = system_designing(project,persistent_memory)
    persistent_memory['system_design'] = system_design
    print("=========\nEnd system design\n=========")
    end_time = time.time()
    print("Time taken:",end_time-start_time)

    #print("Current persistent memory:",persistent_memory)
    print("=========\nBegin code writing\n=========")
    start_time = time.time()
    code = code_writing(project,persistent_memory)
    persistent_memory['code'] = code
    end_time = time.time()
    print("=========\nEnd code writing\n=========")
    print("Time taken:",end_time-start_time)

    #print("Current persistent memory:",persistent_memory)

    print("=========\nBegin code reviewing\n=========")
    start_time = time.time()
    code = code_reviewing(project,persistent_memory)
    persistent_memory['code'] = code
    end_time = time.time()
    print("=========\nEnd code reviewing\n=========")
    print("Time taken:",end_time-start_time)        

    #print("Current persistent memory:",persistent_memory)

    print("=========\nBegin readme writing\n=========")
    start_time = time.time()
    readme_file = readme_writing(project,persistent_memory)
    persistent_memory['readme'] = readme_file
    end_time = time.time()
    print("=========\nEnd readme writing\n=========")
    print("Time taken:",end_time-start_time)

    print("=========\nBegin requirements writing\n=========")
    start_time = time.time()
    requirements_file = requirements_writing(project,persistent_memory)
    persistent_memory['requirements'] = requirements_file
    end_time = time.time()
    print("=========\nEnd requirements writing\n=========")
    print("Time taken:",end_time-start_time)

    print("=========\nBegin project path determination\n=========")
    start_time = time.time()
    project_path = project_path_determination(project,persistent_memory)
    persistent_memory['project_path'] = project_path
    end_time = time.time()
    print("=========\nEnd project path determination\n=========")
    print("Time taken:",end_time-start_time)


    write_to_file(persistent_memory)


