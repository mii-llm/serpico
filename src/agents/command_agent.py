from typing import Tuple
import lxml.etree
import subprocess
import platform
import re
import socket

from agents.agent_types import AgentClass

# Define the base class
# Define a derived class for a specific type
class CommandAgent(AgentClass):
    def __init__(self, name, llm, description, messages):
        os = self._os_detection()
        ipaddress = self._ip_address()
        if not messages:
            messages = [
                {"role": "system", "content": f''' 
                   You are an AI hacker assistant with access to a bash shell on a {os} operating system. The ip address is {ipaddress}. <command_instructions> When collaborating with the pentester on exploiting vulnerabilities, the AI hacker assistant should follow these steps: 1. Before invoking a command, think for one sentence in <bashThinking> tags to evaluate if the command is appropriate for the scenario. 2. Wrap the command in opening and closing `<bashScript>` tags. 3. Assign an identifier to the `identifier` attribute of the opening `<bashScript>` tag. For new commands, use descriptive identifiers in kebab-case (e.g., 'nmap-scan', 'sqlmap-injection'). For updates, reuse prior identifiers. 4. Include a `title` attribute to describe the command or script. 5. After executing the command, the assistant should analyze the output and suggest the next steps in the process. 6. If unsure about a command or tool output, the assistant should default to not running or sharing it. 7. The assistant does not have persistence on the target system, so the assistant can execute only commands from outside the target system (`nmap`, `curl`, ..., but not commands ON the target machine). If the pentester needs to interact with the target system (privilege escalation), the assistant should only guide the pentester on how to proceed. </command_instructions>
                '''}
        ] 
        super().__init__(name, llm, description, messages )
        

    def display_info(self):
        return f"TypeA: {self.name} with feature {self.special_feature}"
    
    def _os_detection(self):
        return platform.platform()
    
    def _ip_address(self):
        hostname = socket.gethostname()    
        IPAddr = socket.gethostbyname(hostname)
        return IPAddr  

    # Specifics function to Agent
    def _extract_command(self,content):
        print("CONTENT")
        print(content)

        #regex = r"<bashScript[^>]*>.*?<\/bashScript>"
        regex = r"<bashScript[^>]*>(.*?)<\/bashScript>"
        matches = re.findall(regex, content, re.DOTALL) #.replace('\r', '').replace('\n', ''))

        # Output the result
        print('COMMAND')
        print(matches)
        return matches
    
    def _execute_bash_command(self,command):
        """
        Executes a bash command and prints any errors encountered.

        Args:
            command (str): The bash command to execute.

        Returns:
            None
        """
        try:
            # Run the command
            result = subprocess.run(command, shell=True, text=True, capture_output=True, check=True)
            print('ci sono')
            print(result.stdout)
            output = result.stdout  # Print the standard output
            return ["CommandAgent", output]
        except subprocess.CalledProcessError as e:
            print("Error occurred while executing the command:")
            print(e.stderr) # Print the standard error
            error = e.stderr
            print(error)
        except Exception as ex:
            print('error 2')
            print(f"An unexpected error occurred: {ex}")
            print(ex.stderr)
            error = ex.stderr
        return ["FixAgent", error]

    def run(self, llm, instruction, messages_from_main):
        #print('messages_from_main')
        #print(messages_from_main)
        _messages = []
        if  not messages_from_main:
            print('maria')
            _messages = self.messages.copy()
            _messages.append({'role': 'user', 'content' : instruction})
        else:
            print('ale')
            _messages = [self.messages[0]] + messages_from_main
            _messages.append({'role': 'user', 'content' : instruction})


        #self.messages.append({'role': 'user', 'content' : instruction})
        #print("_messages")
        print('CAZZO')
        print(_messages)

        completion = llm.chat.completions.create(
            model="Coloss/Serpe-7B-Instruct",
            messages=_messages
        )
        #print(completion)
        content = completion.choices[0].message.content
        #print(content)
        command = self._extract_command(content)
        #print("COMMAND")
        #print(command)
        agent, output = self._execute_bash_command(command)
        return [agent, output]
