# rhit_IRPA_2023

Rose-hulman Institute of Technology Class of Senior Design 2023 IRPA Chatbots Project

## Setup instructions:

1. Install Anaconda.

2. Open Anaconda Terminal.

3. Run "conda env create -f environment.yml" in anaconda terminal this will create an environment called irpa_chatbot and install the necessary libraries.

4. Activate the environment that was created by running "conda activate irpa_chatbot"

5. Run "pip install farm-haystack==1.16.0"

6. Create an .env file with the following fields:
  - SECRET_KEY
  - ROOT_USERNAME
  - ENVIRONMENT #Options: development, production

  See the .env_template file for an example.
  SECRET_KEY specifies a a key used to create authorization token for the admin
  ROOT_USERNAME specifies the initial root administrator user who can access the system and add admins. It should be a Rose-Hulman username.
  ENVIRONMENT specifies the environment the software is in. The options are development and production.

## Running Locally

- Open four anaconda terminal and each should be in the irpa_chatbot environment. (conda activate irpa_chatbot). Each
  terminal is for starting each of the services below:

  ### Starting Rasa API
  In the anaconda terminal, run "python -m  rasa run --cors "*" --enable-api"
  
  ### Starting Rasa Action Server
  In the anaconda terminal, run "python -m rasa run actions"

  ### Starting Backend API
  In the anaconda terminal, run "uvicorn general_api:app --reload"

  ### Starting Frontend
  1. cd into chatbot_app folder
  2. Run "npm install"

## Testing:
Open anaconda terminal, cd into the project directory
### Test Rasa Model:
 Type rasa test in the terminal. The test results will be in failed_stories.yml in the results directory.
### Unit Test and Integration Test
 Don't need to cd into test directory. At the project's root directory run the following command:
   - To run all test: python -m unittest discover tests test*.py
   - To run individual test: python -m unittest tests/{name of test}.py 
      - For example: python -m unittest tests/test_knowledgebase.py
      - Note: all test files should start with prefix "test"

