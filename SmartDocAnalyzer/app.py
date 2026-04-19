from flask import Flask, render_template, request
import os

from agents.reader_agent import read_document
from agents.summary_agent import generate_summary
from agents.question_agent import extract_questions

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def home():
    return render_template(
        "index.html",
        summary=None,
        questions=None,
        filename=None,
        error=None
    )


@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        file = request.files.get("file")

        if not file or file.filename == "":
            return render_template("index.html", error="Please upload a file")

        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # 🔹 Read document
        text = read_document(file_path)

        if not text:
            return render_template("index.html", error="No text extracted")

        # 🔹 Generate summary
        summary = generate_summary(text)

        # 🔹 Extract questions
        questions = extract_questions(text)

        return render_template(
            "index.html",
            summary=summary,
            questions=questions,
            filename=file.filename,
            error=None
        )

    except Exception as e:
        return render_template("index.html", error=str(e))


if __name__ == "__main__":
    app.run(debug=True)