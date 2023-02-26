import os
import openai
import yaml
# from prompt_constructor import PromptConstructor

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

  def generate_messages(self): 
    response = openai.Completion.create(
      model= self.config.get("model"),
      prompt=[
        open('example_prompt.txt','r').read()#TODO Replace this with PromptConstructor service
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
  pickup = PickupLineGenerator()
  pickup.generate_messages()