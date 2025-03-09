
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv

import fitz  # PyMuPDF
from fuzzywuzzy import fuzz


load_dotenv()
apiKey = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key = apiKey)  

##
## Converts Speech to Text
## filename - "/path/to/file/speech.mp3"
def getSpeechToText(filename):
    audio_file = open(filename, "rb")
    transcription = client.audio.transcriptions.create(
    model="whisper-1", 
    file=audio_file, 
    response_format="text"
    )
    print(transcription.text)
    return transcription.text


# Function to extract text from a PDF
def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print("No file:", pdf_path)
        return None
    doc = fitz.open(pdf_path)
    text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        text += page.get_text("text")
    return text



def generate_cover_letter_text(job_req_stream, resume_stream):
    resume_text = extract_text_from_pdf(job_req_stream) #"data/resume.pdf")
    job_requisition = extract_text_from_pdf(resume_stream) ##"data/job_desc.pdf")
    print(len(resume_text))
    print(len(job_requisition))
    return "Thisiscoverletter:"#generate_cover_letter(resume_text, job_requisition)

#
##  Generate cover letter through OPENAI
###
def generate_cover_letter(resume_text, job_requisition):
    prompt = f"""
    Write a very short, 3-line cover letter for the following job based on the job requisition and the candidate's resume:
    
    Job Requisition:
    {job_requisition}
    
    Candidate's Resume:
    {resume_text}
    
    The cover letter should be concise and professional.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",  # Replace with the appropriate model name, e.g., gpt-4 or gpt-3.5-turbo
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=60  # Limit the response length to ~3 lines
    )
    return completion.choices[0].message.content.strip()
    # return completion.choices[0].message['content'].strip()








