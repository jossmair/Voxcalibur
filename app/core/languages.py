"""Supported multilingual Parakeet languages, ordered for the French UI."""
LANGUAGES = (
    ("fr-FR", "Français"), ("auto", "Auto détection"),
    ("en", "Anglais"), ("es", "Espagnol"), ("de", "Allemand"), ("it", "Italien"),
    ("bg", "Bulgare"), ("hr", "Croate"), ("da", "Danois"), ("et", "Estonien"),
    ("fi", "Finnois"), ("el", "Grec"), ("hu", "Hongrois"), ("lv", "Letton"),
    ("lt", "Lituanien"), ("mt", "Maltais"), ("nl", "Néerlandais"),
    ("pl", "Polonais"), ("pt", "Portugais"), ("ro", "Roumain"),
    ("ru", "Russe"), ("sk", "Slovaque"), ("sl", "Slovène"),
    ("sv", "Suédois"), ("cs", "Tchèque"), ("uk", "Ukrainien"),
)
LANGUAGE_CODES = {code for code, _ in LANGUAGES}
