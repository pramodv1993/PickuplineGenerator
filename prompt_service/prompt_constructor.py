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
    
    def update_details(self, history: List[str]=None, reply_attr: List[str]=None, reply_to: str=None):
        self.history = history
        self.reply_attr = reply_attr
        self.reply_to = reply_to
        return self

    def construct(self):
        self._add_profiles()
        self.reply_attr = ['witty'] if not len(self.reply_attr) else self.reply_attr
        if self.history:
            self._add_history(self.history)
            self._add_reply_requirement(reply_attr=self.reply_attr, reply_to=self.reply_to)
        else:
            #initial message
            self
            self.prompt += "\n\nSuggest 3 messages each for P1 and P2 which has to be: "+\
                (", ".join(self.reply_attr)) +\
                ".\nFrom P1 to P2:" +\
                "\n1) "
        return self.prompt