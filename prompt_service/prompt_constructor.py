from typing import List
from prompt_service.models import Msg
class PromptConstructor:
    def __init__(self, prof1: dict, prof2: dict, sender: str, msg_attr: str):
        '''
        history: ['P1:msg1', 'P2:msg2'..]
        msg_attr: ['witty', 'funny'...]
        reply_to: P1/P2
        '''
        self.prof1 = prof1
        self.prof2 = prof2
        self.prompt = "There are two persons meeting on a dating platform:"
        self.history = None
        self.msg_attr = msg_attr
        self.sender = sender
        if not self.sender:
            raise Exception("Please specify sender")

    def _add_profiles(self):
        self.prompt += ('\nPerson P1:\n') +\
                        ('\n'.join([f'{str(k)}:{str(v)}' for k,v in self.prof1.items()]))
        self.prompt += ('\n\nPerson P2:\n') + \
                         ('\n'.join([f'{str(k)}:{str(v)}' for k,v in self.prof2.items()]))

    def _add_history(self):
        history_seq_as_str = [f"{msg_obj.sender}: {msg_obj.msg}" for msg_obj in self.history]
        self.prompt += ("\n\nP1 and P2's conversations so far:\n") +\
                         ('\n'.join(history_seq_as_str))
    
    def _add_sender_and_receiver_info(self):
        #Generate 3 witty, funny replies to p<1|2> by using p<1|2>'s profile.
        self.prompt += f"\n\nGenerate  3 " +\
             (', '.join(self.msg_attr)) +\
             f""" replies to {'P1' if self.sender=='P2' else 'P2'} by using{" new facts from " if len(self.history) == 3 else " "}{'P1' if self.sender=='P2' else 'P2'}'s profile""" +\
             ':\n1) '
    
    def update_prompt(self, history: List[Msg]=None, msg_attr: List[str]=None, sender: str=None):
        self.history = history
        self.msg_attr = msg_attr
        self.sender = sender
    
    def construct(self):
        self._add_profiles()
        if self.history:
            self._add_history()
            self._add_sender_and_receiver_info()
        else:
            #Suggest 3 creative, witty, interesting, poetic, short pick-up lines for p1 using the profile from p2.
            self.prompt += f"\n\nSuggest 3 " +\
                (", ".join(self.msg_attr)) +\
                f" pick-up lines for {self.sender} using the profile from {'P1' if self.sender=='P2' else 'P2'}" +\
                ": \n1) "
        print(self.prompt)        
        return self.prompt
