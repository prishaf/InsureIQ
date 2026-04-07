import requests

class OllamaClient:
    def __init__(self, model="mistral", base_url="http://localhost:11434"):
        self.model = model
        self.url = f"{base_url}/api/generate"

    def generate(self, prompt):
        try:
            response = requests.post(
                self.url,
                json={
                    "model": self.model,
                    "prompt": prompt,
                    "stream": False
                },
                timeout=120
            )

            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                return f"Error: {response.text}"

        except Exception as e:
            return f"Connection error: {str(e)}"


# ----------- MAIN FUNCTION -----------
def generate_insights(text):

    prompt = f"""
You are a professional insurance risk analyst.

Analyze the following insurance document and provide:

1. Risk Summary
2. Key Red Flags
3. Missing or Weak Coverage Areas
4. Recommendations

Keep the response structured and concise.

Document:
{text[:3000]}
"""

    client = OllamaClient(model="mistral")  
    return client.generate(prompt)