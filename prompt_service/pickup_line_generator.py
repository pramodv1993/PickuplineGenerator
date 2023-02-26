import os
import openai
import yaml
from prompt_constructor import PromptConstructor

class PickupLineGenerator:
  def __init__(self):
    self.config = yaml.safe_load(open('config.yaml', 'r'))
    openai.api_key = self.config.get('key')
  
  def _parse_response(self, resps: str) -> str:
      if not resps:
          return []
      res = []
      for resp in resps.get('choices', []):
          text = resp.get('text')
          options = text.split('\n')
          res.append([f"""{option}""".strip() for option in options if len(option)])
      return res

  def generate_messages(self, prompt_constructor: PromptConstructor): 
    response = openai.Completion.create(
      model= self.config.get("model"),
      prompt=[
        prompt_constructor.construct()
      ],
      temperature=0.73,
      max_tokens=256,
      top_p=1,
      frequency_penalty=0,
      presence_penalty=0
    )
    choices = self._parse_response(response)
    print(choices)


if __name__=="__main__":
  prompt_constructor = PromptConstructor(
        prof1={'name':'p1', 
        'profession':'engineer', 
        'favorite food':'noodles', 
        'location':'germany'},
        prof2={'name':'p2', 
        'profession':'teacher', 
        'favorite food':'vada pav', 
        'location': 'india'}
    )
  history= ["P2:Engineers know how to build things, but teachers know how to make things better - wanna join forces?",\
    "P1:Absolutely! I'm great with building, and you're great with bettering - let's get to work!",
    "P2:Great minds think alike! Let's put our heads together and see what we can come up with."
  ]
  reply_to = 'P2'
  msg_attr = ['witty', 'funny', 'curious to know the other']
  prompt_constructor.update_prompt(history=history, msg_attr=msg_attr, reply_to=reply_to)
  pickup = PickupLineGenerator()
  msgs = pickup.generate_messages(prompt_constructor=prompt_constructor)
  print(msgs)
