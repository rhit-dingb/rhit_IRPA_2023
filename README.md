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
- To activate rasa server, run 'rasa run --cors "*" --enable-api'
- Also need to run 'rasa run actions' to start action server so custom actions can be run