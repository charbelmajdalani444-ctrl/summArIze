from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import PyPDF2

app = Flask(__name__)
CORS(app)

genai.configure(api_key="AIzaSyB_hbMrBbB4-O4sHuMWd1e6AFlYzgOtoZs")

model = genai.GenerativeModel("gemini-2.5-flash-lite")

print("Gemini Flash loaded successfully!")


def extract_pdf_text(file):
    text = ""

    try:
        pdf_reader = PyPDF2.PdfReader(file)

        for i, page in enumerate(pdf_reader.pages):
            page_text = page.extract_text()

            if page_text:
                cleaned_text = " ".join(page_text.split())

                text+= f"\n\n--- Page {i+1} ---\n{cleaned_text}"

    except Exception as e:
        print("PDF READ ERROR:", str(e))
        return ""

    return text


@app.route("/")
def home():
    return "Gemini Summarization API Running!"


@app.route("/summarize", methods=["POST"])
def summarize():
    text = ""
    
    if request.form.get("text"):
        text = request.form.get("text")

    elif "file" in request.files:
        file = request.files["file"]

        if not file.filename.endswith(".pdf"):
            return jsonify({
                "error": "Only PDF files are allowed"
            }), 400

        text = extract_pdf_text(file)

        if not text.strip():
            return jsonify({
                "error": "Could not extract text from PDF"
            }), 400

    else:
        return jsonify({
            "error": "Please enter text or upload a PDF"
        }), 400

    if not text.strip():
        return jsonify({
            "error": "Input cannot be empty"
        }), 400

    if len(text.split()) < 20:
        return jsonify({
            "error": "Please provide longer content"
        }), 400

    if len(text.split()) > 50000:
        return jsonify({
            "error": "File too large. Please upload a smaller PDF."
        }), 400

    try:
    
        words = text.split()

        if len(words) > 15000:
            text = " ".join(words[:15000])

        prompt = f"""
        You are an expert academic assistant.

        Understand what is given and then,
        Create clean, well-structured study notes.

        STRICT FORMATTING RULES:
        - Put the file or text name as the main title and the rest as subtitles (READ THE NAME VERY WELL DON'T MISTAKE THE CHAPTER NUMBER)
        - Use bullet points
        - Add spacing between sections
        - Keep it clear and easy to read
        - No long paragraphs

        OUTPUT FORMAT:
        Title / Topic Name

        1. Main Section
        - Bullet point
        - Bullet point

        2. Main Section
        - Bullet point
        - Bullet point

        Content:

        OUTPUT FORMAT:
        Title / Topic Name

        1. Main Section
        - Bullet point
        - Bullet point

        2. Main Section
        - Bullet point
        - Bullet point

        Content:
        {text}
        """

        response = model.generate_content(prompt)

        if hasattr(response, "text") and response.text:
            summary = response.text
        else:
            summary = "Summary could not be generated."

        return jsonify({
            "summary": summary
        })

    except Exception as e:
        error_message = str(e)
        print("FULL ERROR:", str(e))

        if "429" in error_message :
            return jsonify({
                "error": "Daily limit has been reached. Please try again later."
            }), 429

        return jsonify({
            "error": "Server.error. Please try again later."
        }), 500


if __name__ == "__main__":
    app.run(debug=True) jjj