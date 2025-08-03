from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORS
from pydantic import BaseModel
from transformers import pipeline
import os

# Initialize FastAPI
app = FastAPI()

# Enable CORS for Render frontend
app.add_middleware(
    CORS,
    allow_origins=["https://<your-app>.onrender.com", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load LLaMA 3 8B model (adjust model name as needed)
try:
    model = pipeline('text-generation', model='meta-llama/Llama-3-8b', device=0)  # Requires GPU
except Exception as e:
    print(f"Failed to load model: {e}")
    model = None  # Fallback for error handling

class ChatInput(BaseModel):
    message: str

@app.get('/')
async def root():
    return {"message": "Hugging Face Spaces backend for chat"}

@app.post('/api/chat')
async def chat(input: ChatInput):
    if not model:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Generate response from the model
        response = model(input.message, max_length=100, num_return_sequences=1)[0]['generated_text']
        return {"response": response}
    except Exception as e:
        print(f"Error during inference: {e}")
        raise HTTPException(status_code=500, detail="Error generating response")

if __name__ == '__main__':
    import uvicorn
    port = int(os.environ.get('PORT', 7860))  # Default port for Hugging Face Spaces
    uvicorn.run(app, host='0.0.0.0', port=port)