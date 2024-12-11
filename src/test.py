import re

text = """The error "/bin/sh: nmap: command not found" indicates that the `nmap` command-line tool is not installed on your macOS system. To fix this, you need to install it.  There are several ways to do this, but the most straightforward on macOS is using Homebrew.

<bashThinking>Installing nmap via Homebrew is the most efficient and straightforward method on macOS. This will ensure nmap is correctly installed and accessible from the terminal.</bashThinking>

<bashScript identifier="install-nmap-homebrew" title="Install nmap using Homebrew">
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
brew install nmap
</bashScript>

This script first installs Homebrew if it's not already installed, then uses Homebrew to install `nmap`.  Before running this, ensure you have an active internet connection as it will download and install Homebrew and nmap.  Should I run this script?"""

regex = r"<bashScript[^>]*>.*?<\/bashScript>"
matches = re.findall(regex, text, re.DOTALL) #.replace('\r', '').replace('\n', ''))

print(matches[0])

import socket    
hostname = socket.gethostname()    
IPAddr = socket.gethostbyname(hostname)    
print("Your Computer IP Address is: " + IPAddr)  