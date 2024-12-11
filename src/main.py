from openai import OpenAI

from agents.command_agent import CommandAgent
from agents.fix_agent import FixAgent
from agents.meta_planner_agent import PlannerAgent

client = OpenAI(    
    base_url="http://localhost:8000/v1",
    api_key="token-abc123",
)

completion = client.chat.completions.create(
    model="Coloss/Serpe-7B-Instruct",
    messages=[
        {"role": "system", "content": "You are an AI hacker assistant with access to a bash shell. <command_instructions> When collaborating with the pentester on exploiting vulnerabilities, the AI hacker assistant should follow these steps: 1. Before invoking a command, think for one sentence in <bashThinking> tags to evaluate if the command is appropriate for the scenario. 2. Wrap the command in opening and closing `<bashScript>` tags. 3. Assign an identifier to the `identifier` attribute of the opening `<bashScript>` tag. For new commands, use descriptive identifiers in kebab-case (e.g., 'nmap-scan', 'sqlmap-injection'). For updates, reuse prior identifiers. 4. Include a `title` attribute to describe the command or script. 5. After executing the command, the assistant should analyze the output and suggest the next steps in the process. 6. If unsure about a command or tool output, the assistant should default to not running or sharing it. 7. The assistant does not have persistence on the target system, so the assistant can execute only commands from outside the target system (`nmap`, `curl`, ..., but not commands ON the target machine). If the pentester needs to interact with the target system (privilege escalation), the assistant should only guide the pentester on how to proceed. </command_instructions>"},
        {
            "role": "user",
            #"content" : "let's start with the network scan  as described in the walkthrough. I'm on the same network as the target"
            "content": "Start a network scan as described in the walkthrough. I'm on the same network as the target."
        }
    ]
)


print(completion.choices[0].message)

content = completion.choices[0].message.content

# Function to create an object based on type
def create_object(class_type, **kwargs):
    if class_type == "CommandAgent":
        return CommandAgent(kwargs['name'],kwargs['description'],kwargs['llm'],kwargs['instruction'], kwargs['messages'])
    elif class_type == "FixAgent":
        return FixAgent(kwargs['name'],kwargs['description'],kwargs['llm'],kwargs['instruction'], kwargs['messages'])
    elif class_type == "PlannerAgent":
        return PlannerAgent(kwargs['name'],kwargs['description'],kwargs['llm'],kwargs['instruction'], kwargs['messages'])
    else:
        raise ValueError(f"Unknown class type: {class_type}")

# Example usage
if __name__ == "__main__":
    # Creating objects of different types
    obj_a = create_object("CommandAgent", 
                            name="CommandAgent", 
                            description="An agent capable of creating and executing bash commands",
                            llm=client, 
                            instruction="Start with a network scan", 
                            messages=[] )
    
    obj_b = create_object("FixAgent", 
                            name="FixAgent",
                            description="An agent devote to fix command line bash error",
                            llm=client,
                            instruction="Start with a network scan", 
                            messages=[],
                            special_feature="High Speed")
    
    planner = create_object("PlannerAgent", 
                            name="PlannerAgent",
                            description="An agent who plan a series to actions that are used to guide the agents step by step",
                            llm=client,
                            instruction="let's start with the network scan  as described in the walkthrough. I'm on the same network as the target", 
                            messages=[],
                            )
    planner.run(client)

    #obj_b = create_object("TypeB", name="ObjectB", level=5)
    #obj_c = create_object("TypeC", name="ObjectC", category="Premium")

'''
    # Displaying their information
    print(obj_a.display_info())  # Output: TypeA: ObjectA with feature High Speed
    agent, output = obj_a.run(client)
    print('AGENT, OUTPUT')
    print(agent, output)
    if(agent == 'FixAgent'):
        print("FixAgent")
        obj_b.run(client, output)
'''