from flask import Flask, render_template
import os
import markdown

app = Flask(__name__)

NEWSLETTER_DIR = '.'  # All newsletters are in root

@app.route('/')
def home():
    # Fetch all .md newsletters generated
    newsletter_files = [f for f in os.listdir(NEWSLETTER_DIR) if f.endswith('.md')]
    return render_template("index.html", files=newsletter_files)

@app.route('/newsletter/<filename>')
def view_newsletter(filename):
    try:
        file_path = os.path.join(NEWSLETTER_DIR, filename)
        with open(file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        html_content = markdown.markdown(md_content)
        return render_template("newsletter.html", content=html_content)
    except FileNotFoundError:
        return f"<h2>Newsletter '{filename}' not found.</h2>", 404

if __name__ == '__main__':
    app.run(debug=True)
