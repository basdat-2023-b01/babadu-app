
def convert_to_slug(text):
    return text.lower().replace(' ', '-')

def convert_to_title(slug):
    return slug.replace('-', ' ').title()