# Decider

## About

The purpose of this project is to serve the REST API and admin panel for the Decider project. The front-end layer of this project can be found at https://github.com/magentanova/decider-front-end. Documentation for the front-end can be found at that page. 

## To run locally 

  - Obtain a copy of the `secrets.py` module that goes with this project, and save it under `Decider/`. 

  - `cd` to the project root.  

  - [set up and activate a virtual environment]

  - `pip install -r requirements.txt`

  - `python setup.py develop`

  - `python run.py`

## Using the Admin Panel 

The Decider app has three basic data models: Questions, Tokens, and QuestionEffects. When engaging with the app, a user is presented with a question and prompted for a yes or no answer. That answer will prompt the value of one or more tokens to go down or up. For example, if the question is, "A new religion seems to be brewing. Will you crush it?", then a "no" answer may help your standing with the peasantry but hurt your standing with the clergy. 

The above scenario would involve at least five data records. One for the Question, one Token each for peasantry and clergy, and two *QuestionEffect*s, each one connecting the question to one of the affected tokens. In the admin panel, when creating a QuestionEffect, you are prompted to supply a delta value which indicates the amount by which a "yes" answer will change the value of the affected token.   

Thus the CMS fields are as follows: 

  - **Question**

    - text: how the question will appear to the user 

  - **Token**

    - name: the display name of the token, like "clergy" or "nobility"

  - **QuestionEffect**

    - token: *one* affected token

    - question: the question that will affect the token.

    - delta: the amount by which the token's value will change if the question is answered in the affirmative. if the question is answered in the negative, the additive inverse of the delta will be used to update the token's value. 

Note that if a question affects four different tokens, you will need to create four separate QuestionEffect records, one for each token affected by this question. 