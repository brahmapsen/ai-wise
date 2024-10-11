# Import from standard library
import os
import logging

# Import from 3rd party libraries
import streamlit as st

from _openai import generate_cover_letter_text, find_resume_match_percent

# Configure logger
logging.basicConfig(format="\n%(asctime)s\n%(message)s", level=logging.INFO, force=True)

# Configure Streamlit page and state
st.set_page_config(page_title="BetterJobs", page_icon="📡")

if "text_error" not in st.session_state:
    st.session_state.text_error = ""

if "visibility" not in st.session_state:
    st.session_state.visibility = "visible"

if "job_desc" not in st.session_state:
    st.session_state.job_desc = ""

if "resume_fpath" not in st.session_state:
    st.session_state.resume_fpath = ""

if "cover_letter" not in st.session_state:
    st.session_state.cover_letter = "Cover letter will be here"

if "resume_match" not in st.session_state:
    st.session_state.resume_match = ""

# Force responsive layout for columns also on mobile
st.write(
    """
    <style>
    [data-testid="column"] {
        width: calc(50% - 1rem);
        flex: 1 1 calc(50% - 1rem);
        min-width: calc(50% - 1rem);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title to the app
st.title("Better Jobs")

#Description to the app
st.markdown(
    "Better Jobs - Jobs match making between a candidate and an Organization"
)

job_req = st.file_uploader(label="Upload Job Description", type=["pdf",])
if job_req is not None:
    job_req_filename = "output/" + job_req.name
    with open(job_req_filename, "wb") as f:
        f.write(job_req.getbuffer())
    st.session_state.job_desc = job_req_filename

cand_resume = st.file_uploader(label="Upload Candidate Resume", type=["pdf",])
if cand_resume is not None:
    res_filename = "output/" + cand_resume.name
    with open(res_filename, "wb") as f:
        f.write(cand_resume.getbuffer())
    st.session_state.resume_fpath = res_filename


def test_filestream():
    # Example: Read and print the content of the file stream
    content = job_req.read()
    st.write("File content size:", len(content))  # Process content as needed
    
def create_cover_letter():
    cover_letter = generate_cover_letter_text(st.session_state.job_desc, st.session_state.resume_fpath)
    st.session_state.cover_letter = cover_letter

def find_resume_match():
    # res_match_prcnt = find_resume_match_percent(job_req, cand_resume)
    res_match_prcnt = find_resume_match_percent( st.session_state.job_desc, st.session_state.resume_fpath)
    st.session_state.resume_match = res_match_prcnt

st.text_input("Resume Match %: ", st.session_state.resume_match)

# # Create a column layout
col1, col2 = st.columns(2)
with col1:
    # Create a button to match resume
    st.button(
        label="Resume Match",  # name on the button
        help="Find resume match %",  # hint text (on hover)
        key="find_resume_match",  # key to be used for the button
        type="secondary",  # red default streamlit button
        on_click=find_resume_match,  # function to be called on click
        args=(),  # arguments to be passed to the function
    )

with col2:
    # Create a button to create Cover letter using openAI
    st.button(
        label="Create Cover letter",  # name on the button
        help="Click to create letter for a Job",  # hint text (on hover)
        key="cr_cover_letter",  # key to be used for the button
        type="primary",  # red default streamlit button
        on_click=create_cover_letter,  # function to be called on click
        args=(),  # arguments to be passed to the function
    )

st.text_area("Cover Letter", st.session_state.cover_letter)

# Shows loading icon while podcast and audio are being generated
text_spinner_placeholder = st.empty()

# Shows error message if any error occurs
if st.session_state.text_error:
    st.error(st.session_state.text_error)
