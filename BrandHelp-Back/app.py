from dotenv import load_dotenv
from flask import Flask, request, jsonify
import openai
from openai import OpenAI
import os
from flask_cors import CORS

load_dotenv()


client = OpenAI()
app = Flask(__name__)
CORS(app, origins=["http://127.0.0.1:5500"])


@app.route("/")
def hola_mundo():
    return "<p>¡Hola mundo!</p>"


@app.route("/process_prompt", methods=["POST"])
def process_prompt():
    print (request)
    data = request.get_json()
    print(data)
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-0125",
            response_format={"type": "json_object"},
            messages=[
                {"role": "system", "content": "You are a helpful assistant designed to output JSON"},
                {
                    "role": "user",
                    "content": f"Busco nombres creativos para mi nuevo emprendimiento de {data.get('emprendimiento')}, inspirado en {data.get('hito')}. Quiero que transmitan {data.get('experiencia')}. Los nombres deben ser en español, de máximo 3 palabras)",
                },
            ],
        )

        generated_text = response.choices[0].message.content  # Accessing content attribute

        return jsonify({"response": generated_text})
    except Exception as e:
        # Handle errors appropriately
        return jsonify({"error": str(e)})


if __name__ == "__main__":
    app.run("localhost", 8080, debug=True)
