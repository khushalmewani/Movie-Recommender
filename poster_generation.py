import base64
import io
from openai import OpenAI
from PIL import Image
from dotenv import load_dotenv
import os

# Load .env variables
load_dotenv()

# Get API key from environment
API_KEY = os.getenv('FLUX_API_KEY')

def generate_movie_poster(movie_name, genre):
    """
    Generate a movie poster using the Nebius API
    """
    try:
        client = OpenAI(
            base_url="https://api.studio.nebius.com/v1/",
            api_key=API_KEY
        )
        
        prompt = f"""
        Create a high-quality, professional movie poster image for a {genre} film titled "{movie_name}".
        
        The poster should:
        - Have a visual style typical of {genre} movies
        - Include the title "{movie_name}" prominently displayed
        - Have appropriate color palette and imagery for the genre
        - Look like a professional Hollywood movie poster
        - Be in portrait orientation (taller than wide)
        - Include space for credits at the bottom
        
        Make the poster visually striking and compelling to attract viewers.
        """
        
        print(f"Sending request to Nebius API with prompt: {prompt}")
        
        response = client.images.generate(
            model="black-forest-labs/flux-dev",
            response_format="b64_json",
            extra_body={
                "response_extension": "png",
                "width": 512,
                "height": 768,
                "num_inference_steps": 28,
                "negative_prompt": "blurry, low quality, distorted text, unprofessional",
                "seed": -1
            },
            prompt=prompt
        )
        
        print("API response received successfully")
        
        image_data = base64.b64decode(response.data[0].b64_json)
        image = Image.open(io.BytesIO(image_data))
        return image
    
    except Exception as e:
        print(f"Error generating poster: {str(e)}")
        return None
