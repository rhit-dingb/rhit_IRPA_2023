# rhit_IRPA_2023
Rose-hulman Institute of Technology Class of Senior Design 2023 IRPA Chatbots Project


## Setup instructions:
- Required: Python 3.8.x; Anaconda; Rasa; ujson; Tensorflow
Instructions are from this video: https://www.youtube.com/watch?v=oNLhg29aykc

Install Anaconda.

**Windows:** Search anaconda prompt on the windows tab and open anaconda prompt 
  **Mac:** open terminal

cd into the github folder.

Create a new environment by typing this into the prompt: conda create --name irpa_chatbot python==3.8

Activate the environment: conda activate irpa_chatbot

Install the following packages:

conda install ujson

Conda install tensorflow

pip install rasa

- NEVER run rasa init, it will recreate another project
- run 'rasa train' everytime after git pull
- run 'rasa shell' to open interactive shell
- run 'rasa data validate' to validate the training data after making changes.
- Also need to run 'rasa run actions' to start action server so custom actions can be run

1. Open anaconda terminal, cd into the project directory
2. Don't need to cd into test directory. At the project's root directory run the following command:
   - To run all test: python -m unittest discover tests test*.py
   - To run individual test: python -m unittest tests/{name of test}.py 
      - For example: python -m unittest tests/test_knowledgebase_enrollment.py
      - Note: all test files should start with prefix "test"
- To activate rasa server, run 'rasa run --cors "*" --enable-api'
- Also need to run 'rasa run actions' to start action server so custom actions can be run

Testing:
Open anaconda terminal, cd into the project directory
Don't need to cd into test directory. At the project's root directory run the following command:
To run all test: python -m unittest discover tests test*.py
To run individual test: python -m unittest tests/{name of test}.py
For example: python -m unittest tests/test_knowledgebase_enrollment.py
Note: all test files should start with prefix "test"
