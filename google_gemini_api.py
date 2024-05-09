# import google.generativeai as genai

# def send_query_to_ai (prompt, API_KEY):
#     try:
#         generation_config = genai.GenerationConfig(temperature=0,top_p=1,top_k=100)
#         genai.configure(api_key=API_KEY, transport='rest')
#         model = genai.GenerativeModel('gemini-pro')
#         response = model.generate_content(prompt, generation_config=generation_config)
#         return response.text
#     except Exception as e:
#         print(e)
#         return False

# def calculate_token_size(text):
#     words = text.split()
#     token_count = len(words)
#     return token_count

"""
At the command line, only need to run once to install the package via pip:

$ pip install google-generativeai
"""

from pathlib import Path
import hashlib
import google.generativeai as genai
#from langchain_community.document_loaders import PyPDFLoader



genai.configure(api_key="Your_API_Key",transport='rest')

# Set up the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
}

safety_settings = [
  {
    "category": "HARM_CATEGORY_HARASSMENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_HATE_SPEECH",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
  {
    "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
    "threshold": "BLOCK_MEDIUM_AND_ABOVE"
  },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

uploaded_files = []
def upload_if_needed(pathname: str) -> list[str]:
  path = Path(pathname)
  hash_id = hashlib.sha256(path.read_bytes()).hexdigest()
  try:
    existing_file = genai.get_file(name=hash_id)
    return [existing_file.uri]
  except:
    pass
  uploaded_files.append(genai.upload_file(path=path, display_name=hash_id))
  return [uploaded_files[-1].uri]

def extract_pdf_pages(pathname: str) -> list[str]:
  parts = [f"--- START OF PDF ${pathname} ---"]
  # Add logic to read the PDF and return a list of pages here.
  pages = []
  for index, page in enumerate(pages):
    parts.append(f"--- PAGE {index} ---")
    parts.append(page)
  return parts
file1= r"C:\GeminiChatBot\PDF_comparision\SHG Application Form.pdf"
file2=r"C:\GeminiChatBot\PDF_comparision\SHG App1.pdf"
convo = model.start_chat(history=[
  {
    "role": "user",
    "parts": extract_pdf_pages(file1)
  },
  {
    "role": "user",
    "parts": extract_pdf_pages(file2)
  },
  {
    "role": "user",
    "parts": [" Is both the pdf file having the same content"]
  },
  {
    "role": "model",
    "parts": ["Yes, both PDF files you provided, `genai-for-next-gen-governments.pdf`, appear to have the same content based on the text you shared."]
  },
  {
    "role": "user",
    "parts": extract_pdf_pages("<path>/document2.pdf")
  },
  {
    "role": "user",
    "parts": extract_pdf_pages("<path>/document3.pdf")
  },
  {
    "role": "user",
    "parts": ["is both the file having the same content?"]
  },
  {
    "role": "model",
    "parts": ["No, the content of the two PDF files you provided is different. \n\n* **\"genai-for-next-gen-governments.pdf\"** discusses the potential of Generative AI (GenAI) for improving government services and governance, including its applications, benefits, and challenges. \n* **\"Krishan Bisht-1.pdf\"** appears to be a resume outlining the skills and experience of an individual named Krishan Bisht, who specializes in Automation Testing, Functional Testing, API Testing, and Database Testing."]
  },
])
file_path = "path/to/your/document.pdf"
#loader1 = PyPDFLoader(file1)
# documents1 = loader1.load()
# loader2 = PyPDFLoader(file2)
# documents2 = loader2.load()
message="if {File1} and {file2} is having the same content? and also print actual content from {file1}",file1,file2
convo.send_message(message)
print(convo.last.text)
for uploaded_file in uploaded_files:
  genai.delete_file(name=uploaded_file.name)