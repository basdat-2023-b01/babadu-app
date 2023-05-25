import datetime

def convert_to_slug(text):
    return text.lower().replace(' ', '-')

def convert_to_title(slug):
    return slug.replace('-', ' ').title()

def convert_to_date(slug):
    return datetime.datetime.strptime(slug, "%d-%B-%Y").date()
