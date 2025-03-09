# AI-WISE

Uses Agentic AI to streamline workflow and improve business productivity,

- add OPENAI_API_KEY and TWELVELABS_API_KEY, XI_API_KEY to ".env" file

# create virtual env "env"

python -m venv env
source ./env/bin/activate
pip install -r requirements.txt

nltk.download('punkt')
nltk.download('stopwords')
nltk.download('punkt_tab')

# Run the app

--streamlit run jobs.py

streamlit run storyboard.py
