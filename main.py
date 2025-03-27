from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from diffusers import StableDiffusionPipeline
import torch
import uuid
import os
import logging
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve static files from the 'generated' directory
app.mount("/generated", StaticFiles(directory="generated"), name="generated")

# Load Stable Diffusion model
model_id = "nitrosocke/Ghibli-Diffusion"
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
pipe.to("mps")  # Use Apple M1/M2 GPU

# Ensure the 'generated' directory exists
if not os.path.exists("generated"):
    os.makedirs("generated")

class PromptRequest(BaseModel):
    prompt: str

@app.post("/generate")
async def generate_image(request: PromptRequest):
    try:
        # Start logging the image generation request
        logger.info(f"Received request to generate image with prompt: {request.prompt}")

        # Handle the case of an empty prompt
        if not request.prompt.strip():
            raise HTTPException(status_code=400, detail="Prompt cannot be empty")

        # Generate the image
        start_time = datetime.now()
        image = pipe(request.prompt).images[0]
        image_path = f"generated/{uuid.uuid4()}.png"
        image.save(image_path)

        # Log the image generation time
        generation_time = datetime.now() - start_time
        logger.info(f"Image generated and saved as {image_path}. Generation time: {generation_time}")

        # Return image URL and metadata
        return {
            "image_url": f"http://127.0.0.1:8000/{image_path}",
            "generated_at": start_time.isoformat(),
            "generation_time": str(generation_time),
            "image_size": os.path.getsize(image_path),  # File size in bytes
        }
    
    except Exception as e:
        # Handle unexpected errors
        logger.error(f"Error generating image: {str(e)}")
        raise HTTPException(status_code=500, detail="An error occurred while generating the image")

@app.get("/status")
async def status():
    """ Endpoint to check if the server is running smoothly """
    return {"status": "Server is running", "model_loaded": model_id}