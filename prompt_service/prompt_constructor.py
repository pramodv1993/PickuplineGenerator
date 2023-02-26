from typing import List

class PromptConstructor:
    def __init__(self, prof1: dict, prof2: dict):
        self.prof1 = prof1
        self.prof2 = prof2
        self.prompt = '''P1, P2 are two people.
        '''
    def _add_profiles(self):
        self.prompt += ('\nP1 has the profile:\n') +\
                        ('\n'.join([f'{str(k)}:{str(v)}' for k,v in self.prof1.items()]))
        self.prompt += ('\n\nP2 has the profile:\n') + \
                         ('\n'.join([f'{str(k)}:{str(v)}' for k,v in self.prof2.items()]))

    def _add_history(self, history: List[str]):
        '''history: ['P1:msg1', P2:'msg2'..]'''
        self.prompt += ("\n\nP1 and P2's conversations so far:\n") +\
                         ('\n'.join(history))
    
    def _add_reply_requirement(self, reply_to: str, reply_attr: List[str]):
        '''reply_attr: ['witty', 'funny'...]
        reply_to: P1/P2
        '''
        _from = 'P1' if reply_to=='P2' else 'P2'
        self.prompt += (f'\n\nSuggest 3 messages for {_from} in response to {reply_to} which has to be ') +\
                        (', '.join(reply_attr)) +\
                        ':\n1) '
    
    def construct(self, history: List[str]=None, reply_attr: List[str]=None, reply_to: str=None):
        self._add_profiles()
        if history:
            self._add_history(history)
            reply_attr = ['witty'] if not len(reply_attr) else reply_attr
            self._add_reply_requirement(reply_attr=reply_attr, reply_to=reply_to)
        
        else:
            #initial message
            self.prompt += '''\n\nSuggest 3 messages each for P1 and P2 which has to be witty, funny: \nFrom P1 to P2:\n1) '''
        return self.prompt
        
        

if __name__=="__main__":
    prompt = PromptConstructor(
        prof1={'name':'p1', 
        'profession':'engineer', 
        'favorite food':'noodles', 
        'location':'germany'},
        prof2={'name':'p2', 
        'profession':'teacher', 
        'favorite food':'vada pav', 
        'location': 'india'}
    )
    history= ['''P1:Hey P2, I'm sure teaching must be a demanding job - but at least you get to enjoy some delicious snacks during breaks!''']
    reply_to = 'P1'
    reply_attr = ['witty', 'funny', 'curious to know P1']
    # print(prompt.construct())
    print(prompt.construct(history=history, reply_attr=reply_attr, reply_to=reply_to))


