
from typing import Any
from starlette.responses import JSONResponse
from .xtjson import toJson,toBytesJson,obj2dict


class XTJsonResponse(JSONResponse):
    media_type = "application/json"
    def __init__(
        self,
        content: Any,
        striplang:str='',
        **kwargs: Any
    ) -> None:
        if striplang:
            self.striplang =striplang if  striplang[0]=='_' else '_'+striplang
        else:
            self.striplang=''
        super().__init__(content, **kwargs)
    def render(self, content: Any) -> bytes:
        return toBytesJson(content,self.striplang)

from .cache import cache
from .CommonResponse import CommonResponse,CommonQueryShema
from .CommonError import Common500Response,TokenException,PermissionException
from .snowFlakeId import snowFlack
from .encrypt import generateKey
from .filterbuilder import filterbuilder
