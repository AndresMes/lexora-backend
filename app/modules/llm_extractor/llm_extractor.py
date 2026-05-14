import json
import os
from dotenv import load_dotenv
from google import genai

from app.schemas.responses.ocr_result_read import OCRResult


load_dotenv()

class LLMExtractor():
    
    def __init__(self, model_name):
        self.api_key = os.getenv("GEMINI_API_KEY")
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel(model_name)
    
    def extract_invoice_data(self, ocr_text: OCRResult):
        
        prompt = self._build_prompt(ocr_text.raw_text)
        response = self.model.generate_content(prompt)
        return self._parse_response(response.text)
        
        
    def _build_prompt(self, ocr_text: str) -> str:
        return f"""
    Eres un extractor de datos de facturas colombianas. Se te proporcionará texto extraído mediante OCR de una factura y deberás identificar y estructurar la información.

    INSTRUCCIONES:
    - Devuelve ÚNICAMENTE un JSON válido, sin texto adicional, sin markdown, sin bloques de código.
    - Por cada campo, incluye "value" y "confidence" (entre 0.0 y 1.0).
    - Si un campo no está presente en el texto, usa null para "value" y 0.0 para "confidence".
    - Las fechas deben estar en formato YYYY-MM-DD.
    - Los valores numéricos deben ser números, no strings. Elimina puntos y comas de separadores.
    - La confianza debe reflejar qué tan seguro estás de haber identificado correctamente ese campo.
    - Para party_type, usa "DISTRIBUTOR" si la factura fue emitida por un proveedor o distribuidor, y "CLIENT" si fue emitida por un cliente. En caso de duda, usa "DISTRIBUTOR".

    FORMATO DE RESPUESTA:
    {{
    "invoice": {{
        "invoice_number": {{"value": "...", "confidence": 0.0}},
        "issue_date": {{"value": "...", "confidence": 0.0}},
        "subtotal": {{"value": 0.0, "confidence": 0.0}},
        "iva": {{"value": 0.0, "confidence": 0.0}},
        "total": {{"value": 0.0, "confidence": 0.0}},
        "category": {{"value": "...", "confidence": 0.0}}
    }},
    "provider": {{
        "name": {{"value": "...", "confidence": 0.0}},
        "nit": {{"value": "...", "confidence": 0.0}},
        "party_type": {{"value": "DISTRIBUTOR", "confidence": 0.0}}
    }},
    "items": [
        {{
        "description": {{"value": "...", "confidence": 0.0}},
        "quantity": {{"value": 0.0, "confidence": 0.0}},
        "unit_price": {{"value": 0.0, "confidence": 0.0}},
        "total": {{"value": 0.0, "confidence": 0.0}}
        }}
    ]
    }}

    TEXTO DE LA FACTURA:
    {ocr_text}
    """
    
    def _parse_response(self, gemini_response: str):
        try:
            clean = gemini_response.strip()
            if clean.startswith("```"):
                clean = clean.split("```")[1]
                if clean.startswith("json"):
                    clean = clean[4:]
            return json.loads(clean.strip())
        except json.JSONDecodeError as e:
            raise ValueError(f"Gemini devolvió un JSON inválido: {e}")