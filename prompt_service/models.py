from typing import Union, List
from pydantic import BaseModel

class Msg(BaseModel):
    sender: str
    msg: str

class MsgRequest(BaseModel):
    profile1: dict={"name":"p1", "profession":"engineer", "favorite food":"noodles"}
    profile2: dict={"name":"p2", "profession":"doctor", "favorite location":"iceland", "location": "germany"}
    sender: Union[str, None] = None
    msg_attr: List[str] = ['witty']
    history: Union[List[Msg], None] = None

class MsgResponse(MsgRequest):
    choices: Union[List[str], None] = None