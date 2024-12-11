## Serpico

![Serpico](https://pad.mymovies.it/filmclub/2006/02/302/locandina.jpg "Serpico security agent")

This repository contains a suite of specialized agents designed to perform various autonomous cyber security tasks. Each agent is powered by **Serpe**, a fine-tuned AI model specialized in cyber security applications. These agents are tailored to assist security professionals, automate routine tasks, and enhance the efficiency of cyber defense operations.

## Features

- **Fine-Tuned AI Model**: Built on Serpe, a state-of-the-art fine-tuned model designed specifically for cyber security contexts.
- **Task-Specific Agents**: Modular agents specialized for various cyber security tasks, such as vulnerability analysis, threat detection, incident response, and more.
- **Scalable Framework**: Easily extendable architecture to add new agents or customize existing ones.
- **Autonomous Agents**: It is possibile to use the planner and the orchestrator agents for creating autonomous tasks.  

---

## Table of Contents

- [Features](#features)
- [Agents](#agents)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

---

## Agents

### 1. **Planner autonomous agents**
- **Purpose**: From a user task create an autonomous system capable of solving all the steps involved in performing the steps
- **Key Capabilities**:
  - Create a set of tasks
  - Orchestrate the tasks between different agents.
  - Autonomously fix and check errors.



---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/mii-llm/serpico
   cd serpico
   pip install -r requirements.txt
   python src/main.py
