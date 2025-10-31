#!/usr/bin/env python3
"""
Wrapper script for generating images from text prompts using Google Gemini AI.
This script outputs base64 encoded image data to stdout for Node.js integration.
"""

import sys
import os
import argparse
import base64
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

# Load environment variables
load_dotenv()

MODEL_NAME = "gemini-2.0-flash-exp"


def generate_image_from_prompt(prompt: str) -> dict:
    """
    Generates an image from a text prompt using Gemini AI.
    
    Args:
        prompt: Text description of the image to generate
        
    Returns:
        dict with image data (base64) and metadata
    """
    try:
        # Initialize the client
        client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY"))
        
        # Configure the generation
        generate_content_config = types.GenerateContentConfig(
            temperature=1.0,
            top_p=0.95,
            top_k=40,
            candidate_count=1,
            seed=5,
            max_output_tokens=8192,
            response_modalities=["IMAGE", "TEXT"],
        )
        
        # Generate the image
        contents = [
            types.Content(
                role="user",
                parts=[types.Part.from_text(text=prompt)],
            )
        ]
        
        # Stream the response
        stream = client.models.generate_content_stream(
            model=MODEL_NAME,
            contents=contents,
            config=generate_content_config,
        )
        
        # Process the stream
        image_data = None
        text_response = ""
        
        for chunk in stream:
            if (
                chunk.candidates is None
                or chunk.candidates[0].content is None
                or chunk.candidates[0].content.parts is None
            ):
                continue
            
            for part in chunk.candidates[0].content.parts:
                if part.inline_data and part.inline_data.data:
                    # Convert image bytes to base64
                    image_data = base64.b64encode(part.inline_data.data).decode('utf-8')
                elif part.text:
                    text_response += part.text
        
        if image_data:
            return {
                "success": True,
                "imageUrl": f"data:image/jpeg;base64,{image_data}",
                "prompt": prompt,
                "text": text_response.strip() if text_response else None,
                "model": MODEL_NAME
            }
        else:
            return {
                "success": False,
                "error": "No image was generated",
                "text": text_response.strip() if text_response else None
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "type": type(e).__name__
        }


def main():
    parser = argparse.ArgumentParser(
        description="Generate images from text prompts using Google Gemini AI."
    )
    parser.add_argument(
        "--prompt",
        type=str,
        required=True,
        help="Text prompt describing the image to generate",
    )
    
    args = parser.parse_args()
    
    # Generate the image
    result = generate_image_from_prompt(args.prompt)
    
    # Output as JSON to stdout
    print(json.dumps(result))
    
    # Exit with appropriate code
    sys.exit(0 if result.get("success") else 1)


if __name__ == "__main__":
    main()
