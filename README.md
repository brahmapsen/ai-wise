# BetterJobsAI

BetterJobsAI matches candidate multi-modal artifacts with job requirements and company culture
using Agentic work flow, open AI O1 model

- add OPENAI_API_KEY and TWELVELABS_API_KEY, XI_API_KEY to ".env" file

# create virtual env "env"

python -m venv env

# Load libraries

pip install -r requirements.txt

## if virtual env already created

source env/bin/activate

# Run the app

streamlit run app.py
