from typing import List

class PromptConstructor:
    def __init__(self, prof1: dict, prof2: dict, sender: str, msg_attr: str):
        '''
        history: ['P1:msg1', 'P2:msg2'..]
        msg_attr: ['witty', 'funny'...]
        reply_to: P1/P2
        '''
        self.prof1 = prof1
        self.prof2 = prof2
        self.prompt = "P1, P2 are two people."
        self.history = None
        self.msg_attr = msg_attr
        self.sender = sender
        if not self.sender:
            raise Exception("Please specify sender")

    def _add_profiles(self):
        self.prompt += ('\nP1 has the profile:\n') +\
                        ('\n'.join([f'{str(k)}:{str(v)}' for k,v in self.prof1.items()]))
        self.prompt += ('\n\nP2 has the profile:\n') + \
                         ('\n'.join([f'{str(k)}:{str(v)}' for k,v in self.prof2.items()]))

    def _add_history(self):
        self.prompt += ("\n\nP1 and P2's conversations so far:\n") +\
                         ('\n'.join(self.history))
    
    def _add_sender_and_receiver_info(self):
        self.prompt += (f"\n\nSuggest 3 messages for {self.sender} in response to {'P1' if self.sender=='P2' else 'P1'} which has to be ") +\
                        (', '.join(self.msg_attr)) +\
                        ':\n1) '
    
    def update_prompt(self, history: List[str]=None, msg_attr: List[str]=None, sender: str=None):
        self.history = history
        self.msg_attr = msg_attr
        self.sender = sender
    
    def construct(self):
        self._add_profiles()
        if self.history:
            self._add_history()
            self._add_sender_and_receiver_info()
        else:
            self.prompt += f"\n\nSuggest 3 messages for {self.sender} which has to be: "+\
                (", ".join(self.msg_attr)) +\
                ". \n1) "
        return self.prompt