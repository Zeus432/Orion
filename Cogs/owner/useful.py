
def cleanup_code(content) -> str:
    """Automatically removes code blocks from the code."""
    if content.startswith('```') and content.endswith('```'):
        num = 6 if content.startswith('```py\n') else (4 if content.startswith('```\n') else 3)
        return content[num:-3]
    else: return content
    
def get_syntax_error(error) -> str:
    if error.text is None:
        return f'```py\n{error.__class__.__name__}: {error}\n```'
    return f'```py\n{error.text}{"^":>{error.offset}}\n{error.__class__.__name__}: {error}```'