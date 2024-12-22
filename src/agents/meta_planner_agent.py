from typing import Tuple
import lxml.etree
import subprocess
import platform
import re
import socket

from agents.agent_types import AgentClass
from schema.plan import Plan

class PlannerAgent(AgentClass):
    def __init__(self, name, description, llm, messages):
        os = self._os_detection()
        
        if not messages:
            messages = [
                {"role": "system", "content": 
                 f'''You are an AI assistant. User will you give you a task.
                 Your goal is to create an exaustive ordered list of sequential steps necessary for solving the problem 
                 For each point provide justification of your steps.
                '''}
        ]
        super().__init__(name, llm, description, messages)

    def display_info(self):
        return f"PlannerAgent: {self.name}"
    
    def _os_detection(self):
        return platform.platform()
    
    def _extract_ordered_list_with_paragraphs(self,content):
        """
        Extracts the text of ordered list items and their associated paragraphs from the given Markdown string.

        Args:
            markdown (str): The Markdown string containing the ordered list.

        Returns:
            list: A list of dictionaries where each dictionary contains the 'item' (list item text)
                and 'paragraph' (associated paragraph text).
        """
        # Use regex to match ordered list items with their associated paragraphs
        pattern = r'^\d+\.\s+(.*?)(?:\n\n|$)(.*?)(?=\n\d+\.|\Z)'
        matches = re.findall(pattern, content, re.MULTILINE | re.DOTALL)

        # Clean up matches and return
        return [{'item': match[0].strip(), 'paragraph': match[1].strip()} for match in matches]
        
    def _extract_ordered_list(self,markdown):
        """
        Extracts the text of ordered list items from the given Markdown string.

        Args:
            markdown (str): The Markdown string containing the ordered list.

        Returns:
            list: A list of strings representing the text of the ordered list items.
        """
        # Use regex to match ordered list items
        pattern = r'^\d+\.\s+(.*?)(?:\n|$)'
        matches = re.findall(pattern, markdown, re.MULTILINE)

        return matches
    
    def run(self, llm, instruction):
        os = self._os_detection()
        self.messages.append({'role': 'user', 'content' : instruction})

        completion = llm.chat.completions.create(
            model="Coloss/Serpe-7B-Instruct",
            messages=self.messages
        )
        print(completion)
        content = completion.choices[0].message.content
        actions = self._extract_ordered_list(content)
        plans = self._extract_ordered_list_with_paragraphs(content)
        print('ACTIONS:')
        print(actions)
        print(len(actions))
        print('PLANS:')
        print(plans)
        print(len(plans))
        actions_plan = []
        for plan in plans:
            '''
            print('ECCO')
            print(plan)
            print('ITEM')
            print(plan['item'])
            print('PARAGRAPH')
            print(plan['paragraph'])
            '''
            real_plan = Plan(title=plan['item'], 
                        description=plan['paragraph'],
                        status='created'
            )
            actions_plan.append(real_plan)
        return actions_plan