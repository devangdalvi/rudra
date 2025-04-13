def generate_greeting(user_name):
    """
    Generate a personalized greeting message for the user.
    """
    return f"Hello {user_name},\n\nHere are your personalized articles for today!"

def format_article_for_markdown(title, summary, link):
    """
    Format an article for markdown with title, summary, and link.
    """
    return f"## [{title}]({link})\n\n{summary}\n\n"

def write_newsletter_to_file(content, filename):
    """
    Write the newsletter content to a file.
    """
    with open(filename, 'w') as file:
        file.write(content)
