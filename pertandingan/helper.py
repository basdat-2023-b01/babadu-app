def convert_to_slug(text):
    return text.lower().replace(' ', '-')

def convert_to_title(slug):
    return slug.replace('-', ' ').title()

def get_jenis_babak(jml_peserta):
    if jml_peserta == 2:
        return "Final"
    elif jml_peserta == 4:
        return "Semifinal"
    elif jml_peserta == 8:
        return "Perempat Final"
    elif jml_peserta == 16:
        return "R16"
    else:
        return "R32"