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
    return choices


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
  history= ["P1:Hey P2, I heard you teach and I'm an engineer. Looks like the only thing we have in common is our love for vada pav!"
  "P2:I'm surprised to find out that another engineer also loves vada pav! What made you fall for it?"
  ]
  reply_to = 'P2'
  msg_attr = ['witty', 'funny', 'curious to know the other']
  prompt_constructor.update_prompt(history=history, msg_attr=msg_attr, reply_to=reply_to)
  # print(prompt_constructor.construct())
  pickup = PickupLineGenerator()
  msgs = pickup.generate_messages(prompt_constructor=prompt_constructor)
  print(msgs)
