import requests
from flask import current_app

PUTER_API_URL = "https://js.puter.com/v2/"

def generate_product_content(product_name):
    try:
        # Make the API request to Puter.js for generating product-related content
        response = requests.post(PUTER_API_URL, json={
            "input": f"Generate questions and answers for the product: {product_name}",
            "model": "gpt-4o"
        })

        if response.status_code != 200:
            return {"error": "Failed to generate content", "details": response.text}
        
        data = response.json()
        questions = data.get("questions", [])
        answer = data.get("answer", "")

        # Return questions and the generated answer
        return {
            "questions": questions,
            "answer": answer
        }
    
    except Exception as e:
        current_app.logger.error(f"Error generating content: {e}")
        return {"error": str(e)}
