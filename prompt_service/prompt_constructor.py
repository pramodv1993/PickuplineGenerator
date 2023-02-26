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
        self.prompt += ('\nP2 has the profile:\n') + \
                         ('\n'.join([f'{str(k)}:{str(v)}' for k,v in self.prof2.items()]))

    def _add_history(self, history: List[str]):
        '''history: ['P1:msg1', P2:'msg2'..]'''
        self.prompt += ("\nP1 and P2's conversations so far:\n") +\
                         ('\n'.join(history))
    
    def _add_reply_requirement(self, reply_to: str, reply_attr: List[str]):
        '''reply_attr: ['witty', 'funny'...]
        reply_to: P1/P2
        '''
        _from = 'P1' if reply_to=='P2' else 'P2'
        self.prompt += (f'\nSuggest 3 messages for {_from} in response to {reply_to} which has to be)') +\
                        ('\n'.join(reply_attr)) +\
                        '\n1) '
    
    def construct(self, history: List[str], reply_attr: List[str], reply_to: str):
        self._add_profiles()
        if history:
            self._add_history(history)
            reply_attr = ['witty'] if not len(reply_attr) else reply_attr
            self._add_reply_requirement(reply_attr, reply_to)
        
        else:
            #initial message
            self.prompt += '''Suggest 3 messages for P2 in response to P1 which has to be witty, funny:'\n1) '''
        return self.prompt
        
        
    


