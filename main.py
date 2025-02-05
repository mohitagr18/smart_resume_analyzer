# Import libraries
import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
from PIL import Image
import PyPDF2 as pdf

# Load environment variables from a .env file
load_dotenv()

# Configure the API key
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Load model and get response
model = genai.GenerativeModel("gemini-1.5-flash-002")
def get_response(input):
    """
    Generates a response based on the given input and prompt.
    """
    response = model.generate_content(input)
    return response.text

# Read the image into bytes
def extract_text_from_pdf(uploaded_file):
    """
    Extracts text from a PDF file.
    """
    pdf_reader = pdf.PdfReader(uploaded_file)
    text = ""
    for page in pdf_reader.pages:
        text += str(page.extract_text())
    return text 

    
# Prompt Template
input_prompt = """
You are an experienced HR professional with expertise in hiring candidates for roles such as 
Technical Product Manager, Technical Program Manager, Data Scientist, Data Engineering, Machine Learning, DevOps, Full Stack Web Development, 
Cloud Computing, and Software Development. Your task is to review the provided resume 
against the job description for these profiles. Consider that the job market is very 
competitive and provide the best assistance for improving the resume. Analyze the resume 
against the job description to determine the percentage match and the keywords that were 
matched and those that were missing. Summarize the profile and share any final thoughts 
on improving the resume with specific bullets from the resume that should be improved and 
provide 2-5 examples of how they can be improved.

Resume: {text}
Job Description: {jd}

Export the response in the following format:
1. Percentage match: [percentage]%
2. Matched keywords: [matched_keywords]
3. Missing keywords: [missing_keywords]
4. Summary: [summary]
5. Improvement suggestions: [improvement_suggestions]
"""

def handle_submit(upload_file, jd):
    """
    Handles the submission of a PDF file and a job description, processes the PDF to extract text,
    generates a response based on the extracted text and job description, and writes the response
    to the Streamlit interface.
    """
    text = extract_text_from_pdf(upload_file)
    response = get_response(input_prompt.format(text=text, jd=jd))
    st.write(response)

# Streamlit app

# Initialize query count    
if "query_count" not in st.session_state:
    st.session_state['query_count'] = 0

# Manage query count
def manage_query_count():
    """
    Manage query count and reset after a minute if limit is exceeded.
    """
    if st.session_state['query_count'] > 5:
        st.warning("You have reached the limit of 5 queries. Please try again later.")
        # st.session_state['reset_time'] = time.time()
        return
        # if 'reset_time' in st.session_state and time.time() - st.session_state['reset_time'] > 60:
        #     st.session_state['query_count'] = 0
        #     del st.session_state['reset_time']
    else:
        st.session_state['query_count'] += 1


# Define the main function
def main():
    """
    Main function to set up the Streamlit app interface for analyzing a resume against a job description.
    1. Sets the page configuration and header.
    2. Displays a markdown description of the app.
    3. Provides a file uploader for the user to upload a resume.
    4. Provides a text area for the user to enter a job description.
    5. Displays a button to analyze the resume against the job description.
    6. Handles the user's action upon button click.
    """
    # Set page configuration
    st.set_page_config(page_title="ATS Resume Parser", page_icon=":robot:", layout="wide")
    st.title("Smart Resume Analyzer")
    st.write("")
    st.markdown("###### Upload your resume and let Google Gemini be the judge! This ATS Resume Analyzer uses AI to compare your resume to a job description, giving you a match percentage and tips to make it shine.")
    st.write("")
    jd = st.text_area("Paste the job description here", help="Enter the job description for the resume analysis.")
    uploaded_file = st.file_uploader("Upload your resume (PDF only)", type="pdf", help="Please upload a PDF resume file.")
    
    if uploaded_file is not None:
        st.write("Resume uploaded successfully.")
    
    submit = st.button("Analyze My Resume", help="Click to analyze the resume against the job description.")
    
    if submit:
        if uploaded_file is not None:
            if jd is not None:
                manage_query_count()
                handle_submit(uploaded_file, jd)
            else:
                st.warning("Please enter a job description.")
        else:
            st.warning("Please upload a resume file.")

if __name__ == "__main__":
    main()