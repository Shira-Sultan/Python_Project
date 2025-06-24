## 🛠️Code Analysis System - Project Overview

### 📋Overview
This project is a backend system integrated with the wit push command to automatically analyze Python files for code quality issues.
It helps maintain high-quality code by detecting common problems and visualizing insights through graphs.

### 🧰Technologies Used:
Language: Python
Server Framework: FastAPI
Code Analysis: Abstract Syntax Tree (AST)
Visualization: Matplotlib

### 🏗️Project Components
#### wit
A simplified version control system with commands: init, add, commit, log, status, checkout and push.

#### FastAPI Server
A backend server that listens for wit push requests and performs:

Code analysis using AST

Detection of code quality issues

Generation of visual graphs

### 🌐API Endpoints
Endpoint	Method	Description
/analyze	POST	Accepts files and returns graphs
/alerts	POST	Accepts files and returns issue warnings

### 🧹Code Quality Checks
The system performs these checks for each pushed Python file:

Function Length: Warn if a function is longer than 20 lines

File Length: Warn if the file has more than 200 lines

Unused Variables: Warn if a variable is assigned but never used

Missing Docstrings: Warn if a function lacks a documentation string

### 📊Visual Graphs
The server generates and returns these visualizations after analysis:

Histogram — Distribution of function lengths

Pie Chart — Number of issues per issue type

Bar Chart — Number of issues per file

Line Chart — Tracks number of issues over time (bonus feature)

Graphs are returned as PNG images after analysis.


## 📁 Project Folder Structure

```
project-root/
│   Alert.py
│   analyze.py
│   daily_issues_history.json
│   Graph.py
│   Main.py
│   README.md
│
├───.idea/
├───.pytest_cache/
├───Graphs/
│   ├───Commit/
│   ├───File/
│   ├───main/
│   └───Repository/
└───__pycache__/
```
Below is the folder structure of the project showing the main files and folders generated during development.


## 🚀Installation & Execution Instructions

1. **Clone the repository:**

   ```bash
   git clone <URL-of-your-repository>
   cd <repository-folder>
   
Create a Python virtual environment:
python -m venv env
source env/bin/activate   # On Windows use: env\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Run the FastAPI server:
uvicorn main:app --reload

Use the wit push command to push your code and trigger the analysis.
The server will analyze your code and return graphs and results.
