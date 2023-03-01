import json
from typing import Union, List
from fastapi import FastAPI
from pydantic import BaseModel
from prompt_service.prompt_constructor import PromptConstructor
from prompt_service.pickup_line_generator import PickupLineGenerator

app = FastAPI()

class MsgRequest(BaseModel):
    profile1: dict={"name":"p1", "profession":"engineer", "favorite food":"noodles"}
    profile2: dict={"name":"p2", "profession":"doctor", "favorite location":"iceland", "location": "germany"}
    sender: Union[str, None] = None
    msg_attr: List[str] = ['witty']
    history: Union[List[str], None] = None

class MsgResponse(MsgRequest):
    choices: Union[List[str], None] = None

@app.get("/")
def read_root():
    return { "Pickupline Generator": "Welcome to Pickup line generator" }

@app.post("/GetPickupLine")
def get_pickup_line(msg_req: MsgRequest) -> MsgResponse:
    """
        ex request body:\n
        {\n
            "profile1": {"name":"p1", "profession":"engineer", "favorite food":"noodles"},\n
            "profile2": {"name":"p1", "profession":"engineer", "favorite food":"noodles"},\n
            "sender": "P1",\n
            "msg_attr": [\n
                "witty",\n
                "funny",\n
                "curious to know about each other"\n
            ],\n
            "history": [\n
                "P1:Hey P2, I heard you teach and I'm an engineer. Looks like the only thing we have in common is our love for vada pav!",\n
                "P2:I'm surprised to find out that another engineer also loves vada pav! What made you fall for it?"\n
            ]\n
        }\n
    """
    if not msg_req.msg_attr:
        raise Exception("Please specify message attributes!")
    if not msg_req.sender:
        raise Exception("Please specify sender!")
    prompt_constructor=PromptConstructor(prof1=msg_req.profile1, 
                                        prof2=msg_req.profile2,
                                        sender=msg_req.sender,
                                        msg_attr=msg_req.msg_attr)
    if msg_req.history:
        prompt_constructor.update_prompt(history=msg_req.history,
                                         msg_attr=msg_req.msg_attr)
    pickup = PickupLineGenerator()
    msgs = pickup.generate_messages(prompt_constructor=prompt_constructor)
    msg_resp = MsgResponse(**msg_req.dict())
    msg_resp.choices = msgs
    return msg_resp