import requests
from extractInfo import ExtractLiterature
import fitz
'''
input file is the pdf
'''
file=fitz.open(r'email_test_cases\test_02.pdf')
extract_obj = ExtractLiterature(file=file)
paragraph = extract_obj.extract_paragraphs()
print("Paragraph Extracted --> ")
print(paragraph)
API_URL = "https://api-inference.huggingface.co/models/sshleifer/distilbart-cnn-12-6"
headers = {"Authorization": "Bearer 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"}

def query(payload):
	response = requests.post(API_URL, headers=headers, json=payload)
	return response.json()
	
output = query({
	"inputs": paragraph,
})
print(output)