import os
import re
import openai
import yaml
from prompt_service.prompt_constructor import PromptConstructor

class PickupLineGenerator:
  def __init__(self):
    self.config = yaml.safe_load(open('prompt_service/config.yaml', 'r'))
    openai.api_key = self.config.get('key')
  
  def _parse_response(self, resps: str) -> str:
      if not resps:
          return []
      res = []
      choices = resps.get('choices', [])
      if len(choices):
        text = choices[0].get('text', '')
        options = text.split('\n')
        res = [f"{re.sub('^[0-9)]+', '', option)}".strip() for option in options if len(option)]
      return res

  def generate_messages(self, prompt_constructor: PromptConstructor):
    response = openai.Completion.create(
      model= self.config.get("model"),
      prompt=prompt_constructor.construct(),
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
        'location': 'india'},
        sender='P1'
    )
  history= [
  "P1:Hey P2, looks like you are a teacher who loves Vada Pav and I'm an engineer who loves noodles! Let's swap recipes!"
  ]
  sender = 'P2'
  msg_attr = ['witty', 'funny', 'curious to know the other']
  # prompt_constructor.update_prompt(history=history, sender=sender, msg_attr=msg_attr)
  print(prompt_constructor.construct())
  pickup = PickupLineGenerator()
  msgs = pickup.generate_messages(prompt_constructor=prompt_constructor)
  print(msgs)