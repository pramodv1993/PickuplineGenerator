import os
import re
import openai
import yaml
from prompt_service.prompt_constructor import PromptConstructor
from prompt_service.models import Msg
class PickupLineGenerator:
  def __init__(self):
    self.config = yaml.safe_load(open('prompt_service/config.yaml', 'r'))
    openai.api_key = os.getenv("KEY")
  
  def _parse_response(self, resps: str) -> str:
      if not resps:
          return []
      res = []
      choices = resps.get('choices', [])
      if len(choices):
        text = choices[0].get('text', '')
        options = text.split('\n')
        for option in options:
          option = option.strip()

          if not option:
            continue

          option = re.sub('^[0-9)]*[\s*P1-2:]*', '', option)
          option = option.replace('"', "")
          res.append(option)
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
  msg_attr = ['witty', 'funny', 'curious to know the other']
  prompt_constructor = PromptConstructor(
        prof1={'name':'p1', 
        'profession':'engineer', 
        'favorite food':'noodles', 
        'location':'germany'},
        prof2={'name':'p2', 
        'profession':'teacher', 
        'favorite food':'vada pav', 
        'location': 'india'},
        sender='P1',
        msg_attr = ['witty', 'funny', 'curious to know the other']
    )
  history= [
  Msg(sender="P1", msg="Hey P2, I'm P1 from Germany. I heard your favorite food is Vada Pav. Do you have any tips on how to make the perfect Vada Pav?"),
  Msg(sender='P2', msg="Wow, an engineer from Germany wanting to learn the art of making Vada Pav! I'm flattered. Of course, I can share with you my secret recipe."),
  Msg(sender='P1', msg="Hey P2, I'm P1 from Germany. I'm an engineer and I love noodles! Have you ever tried eating noodles with Vada Pav? I'm sure it would be a delicious combination!"),
  Msg(sender='P2', msg="I'm sure noodles and Vada Pav would be a match made in heaven! Have you ever tried it before?")
  ]
  sender = 'P1'
  prompt_constructor.update_prompt(history=history, sender=sender, msg_attr=msg_attr)
  print(prompt_constructor.construct())
  pickup = PickupLineGenerator()
  msgs = pickup.generate_messages(prompt_constructor=prompt_constructor)
  print(msgs)