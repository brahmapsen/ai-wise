import fitz  # PyMuPDF
from fuzzywuzzy import fuzz
import os
import openai
from openai import OpenAI
from dotenv import load_dotenv


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


def find_resume_match_percent(job_req_stream, resume_stream):
    ## first find the matching Job requistions 
    # job_req_content = job_req_stream.read()  #"data/job_desc.pdf"
    # resume_content = resume_stream.read()  #"data/resume.pdf"
    # similarity_index = compare_pdfs(job_req_content, resume_content)
    similarity_index = compare_pdfs(job_req_stream, resume_stream)
    return similarity_index

def generate_cover_letter_text(job_req_stream, resume_stream):
    resume_text = extract_text_from_pdf(job_req_stream) #"data/resume.pdf")
    job_requisition = extract_text_from_pdf(resume_stream) ##"data/job_desc.pdf")
    return generate_cover_letter(resume_text, job_requisition)

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


def compare_pdfs(resume_path, job_desc_path):
    if not resume_path or not job_desc_path:
        return "Error: Both file paths must be provided"

    # Extract text from the PDF files using the provided paths
    resume_text = extract_text_from_pdf(resume_path)
    job_desc_text = extract_text_from_pdf(job_desc_path)

    if resume_text is None or job_desc_text is None:
        return "Error: One or both files not found"

    # Compare the two texts using FuzzyWuzzy
    similarity_ratio = fuzz.ratio(resume_text, job_desc_text)

    return similarity_ratio





