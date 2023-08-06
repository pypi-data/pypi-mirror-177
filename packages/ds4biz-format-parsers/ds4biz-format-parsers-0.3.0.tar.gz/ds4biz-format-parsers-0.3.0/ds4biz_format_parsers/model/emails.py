from typing import List, Dict


class TextEmail(object):
    """ Represents an email """

    def __init__(self, id: str, sender: str = "", subject: str = "", recipients: List[str] = None, cc: List[str] = None,
                 bcc: List[str] = None, body_parts: List[str] = None, attachments: Dict[str, str] = None):
        self.id = id
        self.sender = sender
        self.subject = subject
        self.recipients = recipients or []
        self.cc = cc or []
        self.bcc = bcc or []
        self.body_parts = body_parts or []
        self.attachments = attachments or {}
