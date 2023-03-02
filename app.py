import json
from typing import Union, List
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from prompt_service.prompt_constructor import PromptConstructor
from prompt_service.pickup_line_generator import PickupLineGenerator
from prompt_service.models import Msg, MsgRequest, MsgResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return { "Pickupline Generator": "Welcome to Pickup line generator" }

@app.post("/GetPickupLine")
def get_pickup_line(msg_req: MsgRequest) -> MsgResponse:
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
                                         msg_attr=msg_req.msg_attr,
                                         sender=msg_req.sender
                                        )
    pickup = PickupLineGenerator()
    msgs = pickup.generate_messages(prompt_constructor=prompt_constructor)
    msg_resp = MsgResponse(**msg_req.dict())
    msg_resp.choices = msgs
    return msg_resp