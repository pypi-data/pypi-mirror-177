__all__ = [
    'Field',
    'BaseIndex',
    'CouchLoader',
    'BaseModel',
    'BaseObject',
]

from thresult import auto_unwrap

from thcouch.orm.decl.field import Field
from thcouch.orm.decl.index import BaseIndex
from thcouch.orm.decl.loader import CouchLoader
from thcouch.orm.decl.model import BaseModel
from thcouch.orm.decl.object import BaseObject


Field = auto_unwrap(Field)
BaseIndex = auto_unwrap(BaseIndex)

@auto_unwrap
class _CouchLoader(CouchLoader):
    def __getattr__(self, attr) -> type:
        t: type = super().__getattr__(attr)
        return auto_unwrap(t)


CouchLoader = _CouchLoader

BaseModel = auto_unwrap(BaseModel)
BaseObject = auto_unwrap(BaseObject)
