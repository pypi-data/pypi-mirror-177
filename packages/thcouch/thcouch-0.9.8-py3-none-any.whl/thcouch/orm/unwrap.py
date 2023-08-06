__all__ = [
    'CouchDocument',
    'CouchAttachment',
    'CouchClient',
    'CouchDatabase',
]

from thresult import auto_unwrap

from thcouch.orm.document import CouchDocument
from thcouch.orm.attachment import CouchAttachment
from thcouch.orm.client import CouchClient
from thcouch.orm.database import CouchDatabase


CouchDocument = auto_unwrap(CouchDocument)

# FIXME: in `._common` implement proper `CouchAttachment` so auto_unwrap can work
# CouchAttachment = auto_unwrap(CouchAttachment)
CouchAttachment = CouchAttachment

CouchClient = auto_unwrap(CouchClient)
CouchDatabase = auto_unwrap(CouchDatabase)
