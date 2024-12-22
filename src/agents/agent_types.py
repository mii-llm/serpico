from typing import Tuple
import lxml.etree
import subprocess
import platform
import re
import socket


# Define the base class
class AgentClass:
    def __init__(self, name, description ,llm, messages):
        self.name = name
        self.llm = llm
        self.description = description
        self.messages = messages
         
    def display_info(self):
        return f"This is a base class object named {self.name}"
    
    def run(self, llm, messages):
        completion = llm.chat.completions.create(
            model="Coloss/Serpe-7B-Instruct",
            messages=messages
        )
        return completion
    



