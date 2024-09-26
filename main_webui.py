import streamlit as st
from agent import Agent
from utils import *
from agent_literal import *
import time
import os
import datetime
import json
import yaml

def chat(query, query_additional, agent1, agent2, project, persistent_memory, chatter, chat_history):
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
def main():
    st.set_page_config(page_title="Cosmo Nicefellow Tech", layout="wide")

    # Arrange the title and the image in columns
    col1, col2 = st.columns([3, 1])  # Adjust column widths as needed
    with col1:
        st.title("Cosmo Nicefellow Tech")
    with col2:
        st.image("assets/cosmo-nicefellow-tech-office.png", width=500)  # Adjust width as needed


    # Initialize session state
    if 'project' not in st.session_state:
        st.session_state['project'] = ''
    if 'clarification' not in st.session_state:
        st.session_state['clarification'] = False
    if 'persistent_memory' not in st.session_state:
        st.session_state['persistent_memory'] = {}
    if 'chatter' not in st.session_state:
        # Use OpenAI backend
        st.session_state['chatter'] = OpenAIBackend()
    if 'conversation_history' not in st.session_state:
        st.session_state['conversation_history'] = []
    if 'clarification_done' not in st.session_state:
        st.session_state['clarification_done'] = False
    if 'system_design_done' not in st.session_state:
        st.session_state['system_design_done'] = False
    if 'code_writing_done' not in st.session_state:
        st.session_state['code_writing_done'] = False
    if 'code_reviewing_done' not in st.session_state:
        st.session_state['code_reviewing_done'] = False
    if 'readme_done' not in st.session_state:
        st.session_state['readme_done'] = False
    if 'requirements_done' not in st.session_state:
        st.session_state['requirements_done'] = False
    if 'project_path_done' not in st.session_state:
        st.session_state['project_path_done'] = False

    st.title("Virtual Software Development")

    # Input section
    st.sidebar.header("Project Settings")
    st.session_state['project'] = st.sidebar.text_area("Software Requirement", st.session_state['project'])
    st.session_state['clarification'] = st.sidebar.checkbox("CEO asks for clarification", st.session_state['clarification'])
    if st.sidebar.button("Start Project"):
        st.session_state['clarification_done'] = False
        st.session_state['system_design_done'] = False
        st.session_state['code_writing_done'] = False
        st.session_state['code_reviewing_done'] = False
        st.session_state['readme_done'] = False
        st.session_state['requirements_done'] = False
        st.session_state['project_path_done'] = False
        st.session_state['persistent_memory'] = {}
        st.session_state['conversation_history'] = []

    # Tabs for each stage
    tabs = st.tabs(["Goal Setting", "System Design", "Programming", "Code Reviewing", "Documentation", "Requirement Writing", "Project Path"])

    # Stage 1: Goal Setting
    with tabs[0]:
        st.header("Goal Setting")
        if st.session_state['project']:
            st.write(f"**Project Description:** {st.session_state['project']}")
            if st.session_state['clarification']:
                if not st.session_state['clarification_done']:
                    # CEO asks for clarification
                    ceo = Agent("CEO")
                    query = f"You are {ceo.literal}. Our customer has a project idea: {st.session_state['project']}. If you need clarification from the customer, please provide the questions for the customer. Please try not to ask too many questions. Please put the questions in a json format with \"questions\" as the key and the questions you want to ask as the value."
                    response = st.session_state['chatter'].communicate(query)
                    try:
                        questions = json.loads(response)['questions']
                    except:
                        questions = response
                    st.session_state['clarification_questions'] = questions
                    st.write(f"**Questions from CEO:**")
                    for q in questions:
                        st.write(f"- {q}")
                    # User provides answers
                    st.session_state['clarification_answers'] = st.text_area("Your Answers", key='clarification_answers')
                    if st.button("Submit Answers"):
                        answer = st.session_state['clarification_answers']
                        while True:
                            query = f"The customer has answered your questions with the following: {answer}. Please determine if you need more information from the customer. If so, please put the questions for the customer in a json format with \"questions\" as the key and the questions you want to ask as the value. If not, please put \"no\" as the value."
                            response = st.session_state['chatter'].communicate(query, reset=False)
                            if len(response) < 10:
                                questions = 'no'
                            else:
                                try:
                                    questions = json.loads(response)['questions']
                                except:
                                    questions = response
                            if questions == "no":
                                query = f"Please summarize the customer's answers to your questions and provide a clear and concise summary. Please put the summary in a json format with \"summary\" as the key and the summary as the value."
                                response = st.session_state['chatter'].communicate(query, reset=False)
                                try:
                                    summary = response['summary']
                                except:
                                    summary = response
                                st.write(f"**CEO's Summary:** {summary}")
                                st.session_state['persistent_memory']['clarification'] = summary
                                break
                            else:
                                st.write(f"**Additional Questions from CEO:**")
                                for q in questions:
                                    st.write(f"- {q}")
                                # Get additional answers
                                answer = st.text_area("Your Additional Answers", key='additional_answers')
                                if st.button("Submit Additional Answers"):
                                    pass  # Loop continues
                        st.session_state['clarification_done'] = True
            else:
                st.write("No clarification requested.")
        else:
            st.write("Please enter a project description in the sidebar to start.")

    # Stage 2: System Design
    with tabs[1]:
        st.header("System Design")
        if st.session_state['project']:
            if not st.session_state['system_design_done']:
                ceo = Agent("CEO")
                cpo = Agent("SystemDesigner")
                chat_history = []
                query = "Please design the system architecture for the project required by the customer. Please provide a detailed list of all the files that need to be created, and the functions and classes that need to be written. Please don't include any files that are not in text format because our company doesn't support non-text files."
                query_additional = "For the system design, write in json format with system_design as the key."
                response = chat(query, query_additional, ceo, cpo, st.session_state['project'], st.session_state['persistent_memory'], st.session_state['chatter'], chat_history)
                try:
                    system_design = response['system_design']
                except:
                    system_design = response
                st.session_state['persistent_memory']['system_design'] = system_design
                st.write(f"**System Design:**")
                st.json(system_design)
                st.session_state['system_design_done'] = True
            else:
                st.write(f"**System Design:**")
                st.json(st.session_state['persistent_memory']['system_design'])
        else:
            st.write("Please enter a project description in the sidebar to start.")

    # Stage 3: Programming
    with tabs[2]:
        st.header("Programming")
        if st.session_state['system_design_done']:
            if not st.session_state['code_writing_done']:
                cpo = Agent("CPO")
                programmer = Agent("Programmer")
                chat_history = []
                query = "Please write the code for the project required by the customer. Please use the system design provided to you to write the code."
                query_additional = '''For the code writing, write in YAML format with the file path as the key and the code as a multi-line string value. Include only the file name followed by the code content without additional titles. Ensure the format is like this:
                ```yaml
                file_name.py: |
                  code content here
                  code content continues...
                another_file.py: |
                  more code content here
                  ...
                ```'''
                response = chat(query, query_additional, cpo, programmer, st.session_state['project'], st.session_state['persistent_memory'], st.session_state['chatter'], chat_history)
                code = response
                st.session_state['persistent_memory']['code'] = code
                st.session_state['code_writing_done'] = True
            else:
                code = st.session_state['persistent_memory']['code']
            st.write("**Code Files:**")
            if isinstance(code, dict):
                for file_name, code_content in code.items():
                    st.subheader(f"File: {file_name}")
                    st.code(code_content, language='python')
            else:
                st.write(code)
        else:
            st.write("Please complete the System Design stage first.")

    # Stage 4: Code Reviewing
    with tabs[3]:
        st.header("Code Reviewing")
        if st.session_state['code_writing_done']:
            if not st.session_state['code_reviewing_done']:
                programmer = Agent("Programmer")
                code_reviewer = Agent("CodeReviewer")
                cpo = Agent("CPO")
                n_rounds = 5
                code = st.session_state['persistent_memory']['code']
                for i in range(n_rounds):
                    st.write(f"**Code Reviewing Round {i+1}**")
                    chat_history = []
                    query = f"Please review the code for the project required by the customer. Please use the system design provided to you to review the code and provide feedback to me. The major focus is to ensure the code is correct and complete so that our customer can directly run the code without any modification. This is the {i+1}th round of a {n_rounds} rounds of code reviewing."
                    query_additional = 'If you are satisfied with the code because the code is correct and complete, please answer with "<ReviewComplete>" tag. If you are not satisfied with the code because the code is not correct or complete, please provide your feedback without "<ReviewNotComplete>" tag.'
                    response = chat(query, query_additional, cpo, code_reviewer, st.session_state['project'], st.session_state['persistent_memory'], st.session_state['chatter'], chat_history)
                    st.write(f"**Code Reviewer Feedback:** {response}")
                    if "<ReviewComplete>" in response:
                        st.write("Code reviewing is complete.")
                        break
                    # Programmer revises code
                    query = "Please write the code again based on the feedback provided by the code reviewer."
                    query_additional = '''For the code writing, write in YAML format with the file path as the key and the code as a multi-line string value. Include only the file name followed by the code content without additional titles. Ensure the format is like this:
                    ```yaml
                    file_name.py: |
                      code content here
                      code content continues...
                    another_file.py: |
                      more code content here
                      ...
                    ```'''
                    response = chat(query, query_additional, cpo, programmer, st.session_state['project'], st.session_state['persistent_memory'], st.session_state['chatter'], chat_history)
                    code = response
                    st.session_state['persistent_memory']['code'] = code
                st.session_state['code_reviewing_done'] = True
            else:
                st.write("Code reviewing has been completed.")
        else:
            st.write("Please complete the Programming stage first.")

    # Stage 5: Documentation (README)
    with tabs[4]:
        st.header("Documentation")
        if st.session_state['code_reviewing_done']:
            if not st.session_state['readme_done']:
                ceo = Agent("CEO")
                cpo = Agent("CPO")
                chat_history = []
                query = "Please write the readme.md file for the project required by the customer. Please use the system design provided to you to write the readme.md file."
                query_additional = "Please put the content of readme.md in YAML format with README.MD as the key and the content as a multi-line string value."
                response = chat(query, query_additional, ceo, cpo, st.session_state['project'], st.session_state['persistent_memory'], st.session_state['chatter'], chat_history)
                try:
                    readme_file = response['README.MD']
                except:
                    readme_file = response
                st.session_state['persistent_memory']['readme'] = readme_file
                st.session_state['readme_done'] = True
            else:
                readme_file = st.session_state['persistent_memory']['readme']
            st.subheader("README.md")
            st.markdown(readme_file)
        else:
            st.write("Please complete the Code Reviewing stage first.")

    # Stage 6: Requirement Writing
    with tabs[5]:
        st.header("Requirement Writing")
        if st.session_state['readme_done']:
            if not st.session_state['requirements_done']:
                ceo = Agent("CEO")
                cpo = Agent("CPO")
                chat_history = []
                query = "Please write the requirements file for the project required by the customer. "
                query_additional = "Please put the content of requirements in a json format with the file name (e.g., requirements.txt for python projects) as the key and the content as the value."
                response = chat(query, query_additional, ceo, cpo, st.session_state['project'], st.session_state['persistent_memory'], st.session_state['chatter'], chat_history)
                requirements_file = response
                st.session_state['persistent_memory']['requirements'] = requirements_file
                st.session_state['requirements_done'] = True
            else:
                requirements_file = st.session_state['persistent_memory']['requirements']
            st.write("**Requirements File:**")
            for file_name, content in requirements_file.items():
                st.subheader(f"File: {file_name}")
                st.code(content)
        else:
            st.write("Please complete the Documentation stage first.")

    # Stage 7: Project Path Determination
    with tabs[6]:
        st.header("Project Path")
        if st.session_state['requirements_done']:
            if not st.session_state['project_path_done']:
                ceo = Agent("CEO")
                cpo = Agent("CPO")
                chat_history = []
                query = "Please determine the project name for the project required by the customer. It will be used as the folder name for the project so please don't use any special characters or spaces."
                query_additional = 'Please put the content of project name in a json format with "name" as the key and the content as the value.'
                response = chat(query, query_additional, ceo, cpo, st.session_state['project'], st.session_state['persistent_memory'], st.session_state['chatter'], chat_history)
                try:
                    project_path = response['name']
                except:
                    project_path = response
                timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
                project_path = f"{project_path}_{timestamp}"
                st.session_state['persistent_memory']['project_path'] = project_path
                st.session_state['project_path_done'] = True
            else:
                project_path = st.session_state['persistent_memory']['project_path']
            st.write(f"**Project Path:** {project_path}")
            # Write to files
            if st.button("Save Project Files"):
                write_to_file(st.session_state['persistent_memory'])
                st.success("Project files saved.")
        else:
            st.write("Please complete the Requirement Writing stage first.")

def write_to_file(persistent_memory):
    base_path = 'work_space/'
    project_path = persistent_memory['project_path']

    if not os.path.exists(base_path):
        os.makedirs(base_path)
    if not os.path.exists(base_path + project_path):
        os.makedirs(base_path + project_path)
    base_path = base_path + project_path + '/'
    #os.rename('conversation_history.txt', base_path+'conversation_history.txt')
    system_design = persistent_memory['system_design']
    code = persistent_memory['code']
    readme = persistent_memory['readme']
    if 'clarification' in persistent_memory:
        clarification = persistent_memory['clarification']
        with open(base_path + 'clarification.txt', 'w') as f:
            f.write(clarification)
    with open(base_path + 'system_design.txt', 'w') as f:
        print("type(system_design):", type(system_design))
        f.write(system_design)
    requirements = persistent_memory['requirements']
    for k, v in requirements.items():
        with open(base_path + k, 'w') as f:
            if isinstance(v, dict):
                json.dump(v, f, indent=4)
            elif isinstance(v, list):
                v = '\n'.join(v)
                f.write(v)
            elif isinstance(v, str):
                f.write(v)
    if isinstance(code, dict):
        for file_path, code_content in code.items():
            full_path = os.path.join(base_path, file_path)
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(code_content)
    with open(base_path + 'readme.md', 'w') as f:
        f.write(readme)

if __name__ == "__main__":
    main()
