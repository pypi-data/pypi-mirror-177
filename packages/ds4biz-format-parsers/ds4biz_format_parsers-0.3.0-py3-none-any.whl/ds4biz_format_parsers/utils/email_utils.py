from pathlib import Path
import email

def get_email(path:Path,encoding="latin"):
    with open(path,encoding=encoding) as o:
        return email.message_from_file(o)
