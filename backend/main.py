from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse
import os
from transformers import pipeline

app = FastAPI()

# Summarization pipeline using a pre-trained model
summarizer = pipeline("summarization")

# Directory to store uploaded files
UPLOAD_DIR = "uploaded_files"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    # Save the uploaded file
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_path, "wb") as f:
        f.write(file.file.read())
    
    return {"filename": file.filename}

@app.post("/summarize/")
async def summarize_file(filename: str):
    # Load the file
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")
    
    with open(file_path, "r") as f:
        text = f.read()
    
    # Summarize the content
    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
    
    return JSONResponse(content={"summary": summary[0]['summary_text']})
