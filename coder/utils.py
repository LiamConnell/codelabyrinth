import datetime
import json
import os
import subprocess

import openai
import tiktoken
from langchain import schema
from langchain.chat_models import ChatOpenAI

MODEL_MAX_TOKENS = {
    "gpt-3.5-turbo": 4096,
    "gpt-4": 8192,
    "gpt-4-32k": 32768,
    "code-davinci-002": 8000
}


def get_embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']


def count_tokens(text, model_name="gpt-3.5-turbo"):
    encoder = tiktoken.encoding_for_model(model_name)
    encoding = encoder.encode(text)
    return len(encoding)


def summarize_title(query):
    llm = ChatOpenAI(model_name="gpt-3.5-turbo")
    prompt = f"""Summarize the following as a pithy title: {query}\n\n"""
    return llm([schema.HumanMessage(content=prompt)]).content.strip().replace('"', "")


def get_git_hash():
    return subprocess.check_output(["git", "rev-parse", "HEAD"]).decode("utf-8").strip()


class ConversationLogger:
    def __init__(self, title: str, logs_dir: str = "./logs"):
        """
        Creates a directory in the logs directory with the title and current timestamp.

        Args:
            title (str): The title of the conversation.
            logs_dir (str, optional): The directory path for storing the logs. Defaults to "./logs".
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        self.log_dir = os.path.join(logs_dir, f"{timestamp}_{title}")
        os.makedirs(self.log_dir, exist_ok=True)

    def log_prompt(self, prompt: str):
        """
        Writes the prompt as a markdown file.

        Args:
            prompt (str): The prompt text to log.
        """
        prompt_file_path = os.path.join(self.log_dir, "prompt.md")
        with open(prompt_file_path, "w") as f:
            f.write(prompt)

    def log_response(self, response: str):
        """
        Writes the response as a markdown file.

        Args:
            response (str): The response text to log.
        """
        response_file_path = os.path.join(self.log_dir, "response.md")
        with open(response_file_path, "w") as f:
            f.write(response)

    def log_metadata(self, conversation_data: dict):
        """
        Writes a JSON file of all conversation metadata.

        Args:
            conversation_data (dict): The dictionary containing conversation metadata.
        """
        metadata_file_path = os.path.join(self.log_dir, "metadata.json")
        with open(metadata_file_path, "w") as f:
            json.dump(conversation_data, f)