import os
import json
from datetime import datetime
from utils import generate_greeting, format_article_for_markdown, write_newsletter_to_file

# ✅ Define the function before calling it
def generate_newsletter(user_name, articles, interests):
    """
    Generate a personalized newsletter in markdown format.
    """
    # Step 1: Generate greeting
    greeting = generate_greeting(user_name)
    
    # Step 2: Filter articles based on user interests
    relevant_articles = [article for article in articles if any(interest.lower() in article['tags'].lower() for interest in interests)]
    
    # Step 3: Format articles for markdown
    formatted_articles = ""
    for article in relevant_articles:
        formatted_articles += format_article_for_markdown(article["title"], article["summary"], article["link"])
    
    # Step 4: Generate newsletter content
    newsletter_content = f"{greeting}\n\n{formatted_articles}"
    
    # Step 5: Generate the filename for the newsletter
    safe_name = user_name.lower().replace(" ", "_")
    filename = f"{safe_name}_newsletter_{datetime.now().strftime('%Y-%m-%d')}.md"
    
    # Step 6: Write to a markdown file
    write_newsletter_to_file(newsletter_content, filename)
    print(f"✅ Newsletter generated for {user_name} and saved to {filename}")
