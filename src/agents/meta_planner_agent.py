from typing import Tuple
import lxml.etree
import subprocess
import platform
import re
import socket

from agents.agent_types import AgentClass

class PlannerAgent(AgentClass):
    def __init__(self, name, description, llm, instruction, messages):
        os = self._os_detection()
        
        if not messages:
            messages = [
                {"role": "system", "content": 
                 f'''You are an AI assistant. User will you give you a task.
                 Your goal is to create an exaustive ordered list of sequential steps necessary for solving the problem 
                 For each point provide justification of your steps.
                '''},
                {
                    "role": "user",
                    "content": instruction
            }
        ]
        super().__init__(name, llm, description, instruction, messages)

    def display_info(self):
        return f"PlannerAgent: {self.name}"
    
    def _os_detection(self):
        return platform.platform()
    
    def _extract_actions_plan(self,content):
        print("CONTENT")
        print(content)
        return content
    

    def run(self, llm):
        os = self._os_detection()
        completion = llm.chat.completions.create(
            model="Coloss/Serpe-7B-Instruct",
            messages=self.messages
        )
        print(completion)
        return completion