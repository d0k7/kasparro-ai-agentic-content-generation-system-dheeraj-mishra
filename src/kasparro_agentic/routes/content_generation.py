from flask import Blueprint, jsonify, request

from kasparro_agentic.services.content_generation_service import generate_product_content

content_bp = Blueprint('content_generation', __name__)

@content_bp.route('/generate-content', methods=['POST'])
def generate_content():
    try:
        # Extract the product name from the POST request body
        data = request.json
        product_name = data.get("product_name")
        
        if not product_name:
            return jsonify({"error": "Product name is required"}), 400
        
        # Call service to generate content via Puter.js
        content = generate_product_content(product_name)
        
        return jsonify(content)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
