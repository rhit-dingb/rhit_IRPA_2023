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

- conda install ujson
- conda install tensorflow
- conda install -c anaconda requests
- conda install -c conda-forge word2number
- conda install -c anaconda pandas
- conda install -c conda-forge fastapi
- conda install -c conda-forge uvicorn
- conda install -c conda-forge gensim
- conda install -c anaconda nltk


pip install rasa

- NEVER run rasa init, it will recreate another project
- run 'rasa train' everytime after git pull
- run 'rasa shell' to open interactive shell
- run 'rasa data validate' to validate the training data after making changes.

1. Open anaconda terminal, cd into the project directory
2. Don't need to cd into test directory. At the project's root directory run the following command:
   - To run all test: python -m unittest discover tests test*.py
   - To run individual test: python -m unittest tests/{name of test}.py 
      - For example: python -m unittest tests/test_knowledgebase_enrollment.py
      - Note: all test files should start with prefix "test"
- To activate rasa server, run 'rasa run --cors "*" --enable-api'
- Also need to run 'rasa run actions' to start action server so custom actions can be run

**Frontend environment**
Here are the packages I install, you may try go to the chatbot_app folder and run 'npm install'
- npm install -g create-react-app
- npm i bootstrap@4.4.1
- npm i --save bootstrap jquery popper.js
- npm install react-router-dom@5.2.0


### Testing:
Open anaconda terminal, cd into the project directory
#### Test Rasa Model:
 Type rasa test in the terminal. The test results will be in failed_stories.yml in the results directory.
##### Test backend logic:
 Don't need to cd into test directory. At the project's root directory run the following command:
   - To run all test: python -m unittest discover tests test*.py
   - To run individual test: python -m unittest tests/{name of test}.py 
      - For example: python -m unittest tests/test_knowledgebase.py
      - Note: all test files should start with prefix "test"

