from sqlalchemy.orm import DeclarativeMeta
from pydantic import BaseModel
from decimal import Decimal
from typing import Any
import orjson
from sqlalchemy.engine import RowMapping
def obj2dict(obj:Any,striplang='')->Any:#type: ignore
    if isinstance(obj,DeclarativeMeta):
        return obj.dict(striplang=striplang)
    elif isinstance(obj,BaseModel):
        return obj.dict()
    elif isinstance(obj,Decimal):
        return str(obj)
    elif isinstance(obj,RowMapping):
        print('RowMapping:',obj)
        return dict(obj)
    raise Exception("object are not jsonable")

def toBytesJson(obj:Any,striplang:str='')->bytes:
    return orjson.dumps(obj,default=lambda obj :obj2dict(obj,striplang=striplang))

def toJson(obj:Any,striplang:str='')->str:
    return orjson.dumps(obj,default=lambda obj :obj2dict(obj,striplang=striplang)).decode()