import requests
import os
from openai import OpenAI
import codecs
import json

class OpenAIBackend:
    def __init__(self, model="gpt-4o-mini"):
        self.model = model
        self.load_api_key()
        self.client = OpenAI(
            # This is the default and can be omitted
            api_key=self.api_key,
            )
        self.conversation_history = []
    def load_api_key(self):
        api_key_path = os.path.join(os.path.expanduser("~"), ".openai_api_key")
        try:
            with open(api_key_path, 'r') as file:
                self.api_key = file.read().strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"OpenAI API key file not found. Please create a file named .openai_api_key in your home directory ({os.path.expanduser('~')}) containing your OpenAI API key.")

    def communicate(self, prompt, reset=True):
        f = codecs.open("conversation_history.txt", "a", "utf-8")
        if reset:
            self.conversation_history = []

        self.conversation_history.append({"role": "user", "content": prompt})

        f.write("="*10+"\n")
        for item in self.conversation_history:
            f.write(item['role']+":\n"+str(item['content'])+"\n")
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history
            )
            assistant_message = response.choices[0].message.content.strip()
            
            f.write("-"*10+"\n"+"response:\n")
            f.write(assistant_message+"\n")
            f.close()
            self.conversation_history.append({"role": "assistant", "content": assistant_message})

            # Extract JSON if present
            if "```json" in assistant_message:
                json_start = assistant_message.index("```json") + 7
                json_end = assistant_message.rindex("```", json_start)
                json_str = assistant_message[json_start:json_end].strip()
                try:
                    assistant_message = json.loads(json_str)
                except json.JSONDecodeError:
                    print("Warning: Failed to parse JSON. Returning original message.")
                    print("-=-=-=-=\nJsonstring:\n")
                    print(json_str)
                    print("-=-=-=-=")

            return assistant_message
        except Exception as e:
            print(f"Error communicating with OpenAI API: {str(e)}")
            return "Error: Unable to get response from OpenAI API"



class llm_chatter:
    def __init__(self,host='http://127.0.0.1:1234/v1/chat/completions'):
        self.host = host
        self.msg_history = []
        self.headers = {
            "Content-Type": "application/json"
        }
    def communicate(self,prompt,greedy=True,reset=True,max_tokens=2048,template="Llama-v3"):
        f = codecs.open("conversation_history.txt", "a", "utf-8")
        if reset:
            self.msg_history = []
        self.msg_history.append({"role": "user", "content": prompt})

        f.write("="*10+"\n")
        for item in self.msg_history:
            f.write(item['role']+":\n"+str(item['content'])+"\n")
        data = {
            "mode": "instruct",
            "max_tokens": max_tokens,
            #"instruction_template":template,
                "messages": self.msg_history
        }
        if greedy:
            data['temperature'] = 0
        response = requests.post(self.host, headers=self.headers, json=data, verify=False)
        answer = response.json()['choices'][0]['message']['content']
        assistant_message = answer

        f.write("-" * 10 + "\n" + "response:\n")
        f.write(answer + "\n")
        f.close()
        self.msg_history.append({"role": "assistant", "content": answer})

        # Extract JSON if present
        if "```json" in assistant_message:
            json_start = assistant_message.index("```json") + 7
            json_end = assistant_message.rindex("```", json_start)
            json_str = assistant_message[json_start:json_end].strip()
            try:
                assistant_message = json.loads(json_str)
            except json.JSONDecodeError:
                print("Warning: Failed to parse JSON. Returning original message.")
                print("-=-=-=-=\nJsonstring:\n")
                print(json_str)
                print("-=-=-=-=")
        return assistant_message

class llm_completion:
    def __init__(self,host='http://127.0.0.1:5000/v1/completions'):
        self.host = host
        self.headers = {
            "Content-Type": "application/json"
        }
    def complete(self,prompt,greedy=False,max_tokens=2048):
        data = {
            "max_tokens": max_tokens,
            "prompt": prompt,
            "temperature": 1,
            "top_p": 0.9,
        }
        if greedy:
            data['temperature'] = 0
        response = requests.post(self.host, headers=self.headers, json=data, verify=False)
        answer = response.json()['choices'][0]['text']
        return answer
