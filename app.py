from flask import Flask, render_template
import os
import markdown
from newsletter_generator import generate_newsletter
import json
app = Flask(__name__,template_folder= "./templates")

NEWSLETTER_DIR = '.'  # All newsletters are in root

@app.route('/')
def home():
    # Fetch all .md newsletters generated
    with open("user_profiles.json", "r") as file:
        user_profiles = json.load(file)

    # Sample articles (you can replace this with your own fetched ones)
    articles = [
        {"title": "AI in Healthcare", "summary": "AI is revolutionizing healthcare...", "tags": "AI, healthcare", "link": "https://example.com/ai-healthcare"},
        {"title": "Blockchain for Finance", "summary": "Blockchain is transforming finance...", "tags": "blockchain, finance", "link": "https://example.com/blockchain-finance"},
        {"title": "F1 and AI Meet", "summary": "AI is now helping analyze F1 races...", "tags": "F1, AI", "link": "https://example.com/f1-ai"}
    ]

    # ✅ Loop through each user in the JSON
    for user in user_profiles.values():
        generate_newsletter(user["name"], articles, user["interests"])


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
