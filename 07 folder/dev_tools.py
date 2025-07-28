from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import subprocess
import tempfile
import uuid
import json
import time
from datetime import datetime
import shutil
import threading
import queue

dev_tools_bp = Blueprint('dev_tools', __name__)

# Supported programming languages and their configurations
SUPPORTED_LANGUAGES = {
    'python': {
        'extension': '.py',
        'compile_cmd': None,
        'run_cmd': 'python3 {file}',
        'docker_image': 'python:3.11-slim',
        'packages': ['pip install numpy pandas matplotlib scikit-learn tensorflow pytorch flask django fastapi']
    },
    'javascript': {
        'extension': '.js',
        'compile_cmd': None,
        'run_cmd': 'node {file}',
        'docker_image': 'node:18-alpine',
        'packages': ['npm install -g typescript react vue angular express']
    },
    'typescript': {
        'extension': '.ts',
        'compile_cmd': 'tsc {file}',
        'run_cmd': 'node {file_js}',
        'docker_image': 'node:18-alpine',
        'packages': ['npm install -g typescript @types/node']
    },
    'rust': {
        'extension': '.rs',
        'compile_cmd': 'rustc {file} -o {output}',
        'run_cmd': './{output}',
        'docker_image': 'rust:1.70-slim',
        'packages': ['cargo install serde tokio actix-web']
    },
    'go': {
        'extension': '.go',
        'compile_cmd': 'go build -o {output} {file}',
        'run_cmd': './{output}',
        'docker_image': 'golang:1.20-alpine',
        'packages': ['go mod init project && go get github.com/gin-gonic/gin']
    },
    'java': {
        'extension': '.java',
        'compile_cmd': 'javac {file}',
        'run_cmd': 'java {class_name}',
        'docker_image': 'openjdk:17-alpine',
        'packages': ['maven gradle spring-boot']
    },
    'kotlin': {
        'extension': '.kt',
        'compile_cmd': 'kotlinc {file} -include-runtime -d {output}.jar',
        'run_cmd': 'java -jar {output}.jar',
        'docker_image': 'openjdk:17-alpine',
        'packages': ['kotlin compiler']
    },
    'swift': {
        'extension': '.swift',
        'compile_cmd': 'swiftc {file} -o {output}',
        'run_cmd': './{output}',
        'docker_image': 'swift:5.8',
        'packages': ['swift package manager']
    },
    'csharp': {
        'extension': '.cs',
        'compile_cmd': 'csc {file}',
        'run_cmd': 'mono {output}.exe',
        'docker_image': 'mcr.microsoft.com/dotnet/sdk:7.0',
        'packages': ['dotnet new console']
    },
    'cpp': {
        'extension': '.cpp',
        'compile_cmd': 'g++ {file} -o {output}',
        'run_cmd': './{output}',
        'docker_image': 'gcc:latest',
        'packages': ['cmake make']
    },
    'c': {
        'extension': '.c',
        'compile_cmd': 'gcc {file} -o {output}',
        'run_cmd': './{output}',
        'docker_image': 'gcc:latest',
        'packages': ['cmake make']
    },
    'julia': {
        'extension': '.jl',
        'compile_cmd': None,
        'run_cmd': 'julia {file}',
        'docker_image': 'julia:1.9',
        'packages': ['Pkg.add("DataFrames", "Plots", "MLJ")']
    },
    'r': {
        'extension': '.R',
        'compile_cmd': None,
        'run_cmd': 'Rscript {file}',
        'docker_image': 'r-base:latest',
        'packages': ['install.packages(c("ggplot2", "dplyr", "shiny"))']
    },
    'php': {
        'extension': '.php',
        'compile_cmd': None,
        'run_cmd': 'php {file}',
        'docker_image': 'php:8.2-cli',
        'packages': ['composer laravel symfony']
    },
    'ruby': {
        'extension': '.rb',
        'compile_cmd': None,
        'run_cmd': 'ruby {file}',
        'docker_image': 'ruby:3.2-alpine',
        'packages': ['gem install rails sinatra']
    },
    'scala': {
        'extension': '.scala',
        'compile_cmd': 'scalac {file}',
        'run_cmd': 'scala {class_name}',
        'docker_image': 'hseeberger/scala-sbt:17.0.2_1.6.2_2.13.8',
        'packages': ['sbt akka play-framework']
    },
    'dart': {
        'extension': '.dart',
        'compile_cmd': None,
        'run_cmd': 'dart {file}',
        'docker_image': 'dart:stable',
        'packages': ['flutter sdk']
    },
    'solidity': {
        'extension': '.sol',
        'compile_cmd': 'solc {file}',
        'run_cmd': None,
        'docker_image': 'ethereum/solc:stable',
        'packages': ['truffle hardhat web3']
    }
}

# Project templates for different types of applications
PROJECT_TEMPLATES = {
    'web_app': {
        'name': 'Web Application',
        'languages': ['javascript', 'typescript', 'python', 'php', 'ruby'],
        'frameworks': ['react', 'vue', 'angular', 'django', 'flask', 'express', 'laravel', 'rails'],
        'files': {
            'package.json': '{"name": "web-app", "version": "1.0.0", "scripts": {"start": "node server.js"}}',
            'server.js': 'const express = require("express");\nconst app = express();\napp.get("/", (req, res) => res.send("Hello World!"));\napp.listen(3000, () => console.log("Server running on port 3000"));',
            'index.html': '<!DOCTYPE html><html><head><title>Web App</title></head><body><h1>Hello World!</h1></body></html>'
        }
    },
    'mobile_app': {
        'name': 'Mobile Application',
        'languages': ['dart', 'javascript', 'kotlin', 'swift'],
        'frameworks': ['flutter', 'react-native', 'ionic', 'xamarin'],
        'files': {
            'main.dart': 'import "package:flutter/material.dart";\nvoid main() => runApp(MyApp());\nclass MyApp extends StatelessWidget {\n  Widget build(BuildContext context) {\n    return MaterialApp(home: Scaffold(appBar: AppBar(title: Text("Hello World")), body: Center(child: Text("Welcome to Flutter!"))));\n  }\n}'
        }
    },
    'dapp': {
        'name': 'Decentralized Application',
        'languages': ['solidity', 'javascript', 'typescript'],
        'frameworks': ['truffle', 'hardhat', 'web3', 'ethers'],
        'files': {
            'contract.sol': 'pragma solidity ^0.8.0;\ncontract HelloWorld {\n    string public message = "Hello, World!";\n    function setMessage(string memory _message) public {\n        message = _message;\n    }\n}',
            'deploy.js': 'const Web3 = require("web3");\n// Deployment script for smart contract'
        }
    },
    'ai_ml': {
        'name': 'AI/ML Project',
        'languages': ['python', 'julia', 'r'],
        'frameworks': ['tensorflow', 'pytorch', 'scikit-learn', 'pandas', 'numpy'],
        'files': {
            'main.py': 'import numpy as np\nimport pandas as pd\nfrom sklearn.model_selection import train_test_split\nfrom sklearn.linear_model import LinearRegression\n\n# Sample ML project\nprint("AI/ML Project Template")',
            'requirements.txt': 'numpy\npandas\nscikit-learn\ntensorflow\nmatplotlib\nseaborn'
        }
    },
    'game': {
        'name': 'Game Development',
        'languages': ['csharp', 'cpp', 'javascript', 'python'],
        'frameworks': ['unity', 'unreal', 'godot', 'pygame'],
        'files': {
            'game.py': 'import pygame\npygame.init()\nscreen = pygame.display.set_mode((800, 600))\npygame.display.set_caption("My Game")\nrunning = True\nwhile running:\n    for event in pygame.event.get():\n        if event.type == pygame.QUIT:\n            running = False\n    screen.fill((0, 0, 0))\n    pygame.display.flip()\npygame.quit()'
        }
    },
    'api': {
        'name': 'REST API',
        'languages': ['python', 'javascript', 'go', 'rust', 'java'],
        'frameworks': ['flask', 'fastapi', 'express', 'gin', 'actix-web', 'spring-boot'],
        'files': {
            'app.py': 'from flask import Flask, jsonify\napp = Flask(__name__)\n\n@app.route("/api/health")\ndef health():\n    return jsonify({"status": "healthy"})\n\nif __name__ == "__main__":\n    app.run(debug=True)'
        }
    },
    'blockchain': {
        'name': 'Blockchain Project',
        'languages': ['solidity', 'rust', 'go', 'javascript'],
        'frameworks': ['substrate', 'cosmos-sdk', 'web3', 'ethers'],
        'files': {
            'token.sol': 'pragma solidity ^0.8.0;\nimport "@openzeppelin/contracts/token/ERC20/ERC20.sol";\ncontract MyToken is ERC20 {\n    constructor() ERC20("MyToken", "MTK") {\n        _mint(msg.sender, 1000000 * 10 ** decimals());\n    }\n}'
        }
    }
}

# Active development environments
active_environments = {}

class DevelopmentEnvironment:
    def __init__(self, user_id, project_id, language, project_type):
        self.user_id = user_id
        self.project_id = project_id
        self.language = language
        self.project_type = project_type
        self.workspace_path = f"/tmp/dev_env_{user_id}_{project_id}"
        self.container_id = None
        self.created_at = datetime.now()
        self.last_activity = datetime.now()
        self.files = {}
        self.terminal_output = []
        
        # Create workspace directory
        os.makedirs(self.workspace_path, exist_ok=True)
        
        # Initialize project files
        self.initialize_project()
    
    def initialize_project(self):
        """Initialize project with template files"""
        if self.project_type in PROJECT_TEMPLATES:
            template = PROJECT_TEMPLATES[self.project_type]
            for filename, content in template['files'].items():
                self.create_file(filename, content)
    
    def create_file(self, filename, content):
        """Create a new file in the workspace"""
        file_path = os.path.join(self.workspace_path, filename)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        self.files[filename] = {
            'content': content,
            'modified': datetime.now().isoformat(),
            'size': len(content)
        }
        self.last_activity = datetime.now()
    
    def read_file(self, filename):
        """Read file content"""
        file_path = os.path.join(self.workspace_path, filename)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
            self.files[filename] = {
                'content': content,
                'modified': datetime.now().isoformat(),
                'size': len(content)
            }
            return content
        return None
    
    def update_file(self, filename, content):
        """Update file content"""
        self.create_file(filename, content)
    
    def delete_file(self, filename):
        """Delete a file"""
        file_path = os.path.join(self.workspace_path, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            if filename in self.files:
                del self.files[filename]
            self.last_activity = datetime.now()
            return True
        return False
    
    def list_files(self):
        """List all files in the workspace"""
        files = []
        for root, dirs, filenames in os.walk(self.workspace_path):
            for filename in filenames:
                rel_path = os.path.relpath(os.path.join(root, filename), self.workspace_path)
                files.append(rel_path)
        return files
    
    def execute_code(self, filename, input_data=""):
        """Execute code file"""
        if self.language not in SUPPORTED_LANGUAGES:
            return {"error": "Unsupported language"}
        
        lang_config = SUPPORTED_LANGUAGES[self.language]
        file_path = os.path.join(self.workspace_path, filename)
        
        if not os.path.exists(file_path):
            return {"error": "File not found"}
        
        try:
            output = []
            error = []
            
            # Compile if needed
            if lang_config['compile_cmd']:
                output_name = os.path.splitext(filename)[0]
                compile_cmd = lang_config['compile_cmd'].format(
                    file=file_path,
                    output=os.path.join(self.workspace_path, output_name)
                )
                
                compile_process = subprocess.run(
                    compile_cmd.split(),
                    cwd=self.workspace_path,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if compile_process.returncode != 0:
                    return {
                        "error": "Compilation failed",
                        "stderr": compile_process.stderr,
                        "stdout": compile_process.stdout
                    }
                
                output.append(f"Compilation successful: {compile_cmd}")
            
            # Run the code
            if lang_config['run_cmd']:
                run_cmd = lang_config['run_cmd'].format(
                    file=file_path,
                    output=os.path.join(self.workspace_path, os.path.splitext(filename)[0]),
                    file_js=file_path.replace('.ts', '.js'),
                    class_name=os.path.splitext(filename)[0]
                )
                
                run_process = subprocess.run(
                    run_cmd.split(),
                    cwd=self.workspace_path,
                    input=input_data,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                result = {
                    "stdout": run_process.stdout,
                    "stderr": run_process.stderr,
                    "return_code": run_process.returncode,
                    "execution_time": "< 1s"
                }
                
                # Add to terminal output
                self.terminal_output.append({
                    "command": run_cmd,
                    "output": run_process.stdout,
                    "error": run_process.stderr,
                    "timestamp": datetime.now().isoformat()
                })
                
                self.last_activity = datetime.now()
                return result
            
            return {"error": "No run command configured for this language"}
            
        except subprocess.TimeoutExpired:
            return {"error": "Execution timeout (30 seconds)"}
        except Exception as e:
            return {"error": f"Execution failed: {str(e)}"}
    
    def run_terminal_command(self, command):
        """Run a terminal command in the workspace"""
        try:
            process = subprocess.run(
                command,
                shell=True,
                cwd=self.workspace_path,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            result = {
                "stdout": process.stdout,
                "stderr": process.stderr,
                "return_code": process.returncode,
                "command": command
            }
            
            # Add to terminal output
            self.terminal_output.append({
                "command": command,
                "output": process.stdout,
                "error": process.stderr,
                "timestamp": datetime.now().isoformat()
            })
            
            self.last_activity = datetime.now()
            return result
            
        except subprocess.TimeoutExpired:
            return {"error": "Command timeout (60 seconds)"}
        except Exception as e:
            return {"error": f"Command failed: {str(e)}"}
    
    def get_terminal_history(self, limit=50):
        """Get terminal command history"""
        return self.terminal_output[-limit:]
    
    def cleanup(self):
        """Clean up the development environment"""
        try:
            if os.path.exists(self.workspace_path):
                shutil.rmtree(self.workspace_path)
        except Exception as e:
            print(f"Error 
(Content truncated due to size limit. Use line ranges to read in chunks)