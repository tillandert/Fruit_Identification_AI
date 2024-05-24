# Fruity-AI
Fruity AI is a web application that predicts what fruit a plant bears based on an image.

## Installation
1. Install [Node.js](https://nodejs.org/en)
2. Clone the repository into your local environment.
3. To make sure you have the proper Python environment for the backend, run this command in the main directory:
    * `pip install -r requirements.txt`
4. To make sure you have all the required dependencies for the frontend, run these commands in the main directory:
    * `cd frontend`
    * `npm install`

## AWS Secret Environment Variables
Using this code requires the user to use their own AWS Access Key and Secret Key, which is free up until a certain number of requests. To view your keys, you must sign into or create and AWS accout: (https://signin.aws.amazon.com/signin?redirect_uri=https%3A%2F%2Fconsole.aws.amazon.com%2Fconsole%2Fhome%3FhashArgs%3D%2523%26isauthcode%3Dtrue%26state%3DhashArgsFromTB_us-east-2_9b933cc4a51e9dee&client_id=arn%3Aaws%3Asignin%3A%3A%3Aconsole%2Fcanvas&forceMobileApp=0&code_challenge=nfrLnofEWS3KyZLDkM9eQm2TY3vUv3gdHiVFEbI51mw&code_challenge_method=SHA-256)

### Setting Up Environment Variables
While you can just replace the indicated variable values in Backend.py and App.js with the environment variables, this is not very secure. One way you can have greater security when running this program is:
1. Create a .env file in the model folder, and add the following:
    AWS_ACCESS_KEY={insert your access key here}
    AWS_SECRET_KEY={insert your secret key here}
    AWS_REGION={insert your region here}
2. Create a .env file in the frontend folder, and add the following:
    REACT_APP_ACCESS_KEY={insert your access key here}
    REACT_APP_SECRET_KEY={insert your secret key here}
    REACT_APP_REGION={insert your region here}

## Running the Project
1. On one terminal, navigate into the model directory and start the backend using these commands:
    * `cd model`
    * `python Backend.py`
2. On a separate terminal, navigate into the frontend directory and start the frontend using these commands:
    * `cd frontend`
    * `npm start`

## Resources
* [Plants Dataset](https://www.kaggle.com/datasets/marquis03/plants-classification)
