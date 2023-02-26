from typing import List

class PromptConstructor:
    def __init__(self, prof1: dict, prof2: dict):
        self.prof1 = prof1
        self.prof2 = prof2
        self.prompt = "P1, P2 are two people."

    def _add_profiles(self):
        self.prompt += ('\nP1 has the profile:\n') +\
                        ('\n'.join([f'{str(k)}:{str(v)}' for k,v in self.prof1.items()]))
        self.prompt += ('\n\nP2 has the profile:\n') + \
                         ('\n'.join([f'{str(k)}:{str(v)}' for k,v in self.prof2.items()]))

    def _add_history(self, history: List[str]):
        '''
        history: ['P1:msg1', 'P2:msg2'..]
        '''
        self.prompt += ("\n\nP1 and P2's conversations so far:\n") +\
                         ('\n'.join(history))
    
    def _add_msg_requirement(self, reply_to: str, msg_attr: List[str]):
        '''
        msg_attr: ['witty', 'funny'...]
        reply_to: P1/P2
        '''
        _from = 'P1' if reply_to=='P2' else 'P2'
        self.prompt += (f'\n\nSuggest 3 messages for {_from} in response to {reply_to} which has to be ') +\
                        (', '.join(msg_attr)) +\
                        ':\n1) '
    
    def update_prompt(self, history: List[str]=None, msg_attr: List[str]=None, reply_to: str=None):
        self.history = history
        self.msg_attr = msg_attr
        self.reply_to = reply_to
    
    def construct(self):
        self._add_profiles()
        self.msg_attr = ['witty'] if not len(self.msg_attr) else self.msg_attr
        if self.history:
            self._add_history(self.history)
            self._add_msg_requirement(msg_attr=self.msg_attr, reply_to=self.reply_to)
        else:
            #initial message
            self
            self.prompt += "\n\nSuggest 3 messages each for P1 and P2 which has to be: "+\
                (", ".join(self.msg_attr)) +\
                ".\nFrom P1 to P2:" +\
                "\n1) "
        return self.prompt