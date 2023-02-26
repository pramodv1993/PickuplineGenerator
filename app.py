from fastapi import FastAPI
from prompt_service.prompt_constructor import PromptConstructor
from prompt_service.pickup_line_generator import PickupLineGenerator
import json

app = FastAPI()

@app.get("/")
def read_root():
    return { "Pickupline Generator": "Welcome to Pickup line generator" }

@app.get("/GetPickupLne")
def get_pickup_line(Profile_1: str,Profile_2: str,reply_to: str,msg_attr: str,history: str):
    """
        returns pickup lines as string
        parameters for getting pickup line


        Profile_1= "{'name':'p1',
                            'profession':'engineer',
                    'favorite food':'noodles',
                    'location':'germany'}"
         Profile_2= "{'name':'p2',
                     'profession':'teacher',
                     'favorite food':'vada pav',
                     'location': 'india'}"
        reply_to='P2'
        msg_attr=witty,funny,curious to know the other
        history="P1:Hey P2, I heard you teach and I'm an engineer. Looks like the only thing we have in common is our love for vada pav!"
        "P2:I'm surprised to find out that another engineer also loves vada pav! What made you fall for it?"
    """

    prompt_constructor=PromptConstructor(prof1=json.loads(Profile_1), prof2=json.loads(Profile_2))
    history = [
        "P1:Hey P2, I heard you teach and I'm an engineer. Looks like the only thing we have in common is our love for vada pav!"
        "P2:I'm surprised to find out that another engineer also loves vada pav! What made you fall for it?"
        ]
    reply_to = 'P2'
    msg_attr = ['witty', 'funny', 'curious to know the other']
    prompt_constructor.update_prompt(history=list(history.split(",")), msg_attr=list(msg_attr.split(",")), reply_to=reply_to)
    # print(prompt_constructor.construct())
    pickup = PickupLineGenerator()
    msgs = pickup.generate_messages(prompt_constructor=prompt_constructor)



    return {"response":msgs}