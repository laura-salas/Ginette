from datetime import datetime as dt, timedelta 
from enum import Enum
from typing import List
import spacy   

nlp = spacy.load("en_core_web_sm") 

class Author(Enum):
    SYSTEM = 1
    USER = 2
    ASSISTANT = 3


class Conversation:
    class Message:
        def __init__(self, content: str, author: Author, token_amount:int = None, date_time: dt=None):
            self.content = content
            self.author_as_enum = author
            self.token_amount = token_amount if token_amount else len(nlp(content))
            self.date_time = date_time
            if author not in Author:
                raise ValueError("Invalid author")
            else:
                if author == Author.SYSTEM:
                    self.author = "system"
                elif author == Author.USER:
                    self.author = "user"
                elif author == Author.ASSISTANT:
                    self.author = "assistant"
        
        def get_time_delta(self, reference_time: dt = dt.now()) -> timedelta:
            if self.date_time:
                return reference_time - self.date_time 

    def __init__(self):
        self.messages: List[self.Message] = []

    def add_message(self, content: str, author: Author, token_amount: int = None, date_time: str = ""):
        self.messages.append(self.Message(content, author, token_amount, date_time))

    def get_last_n_tokens(self, n=1000):
        # if n < current amount of tokens, gets all 
        curr_amt, i = 0, 0
        conversation_excerpt = Conversation() 

        while curr_amt < n:
            if i >= len(self.messages) or self.messages[-i-1].token_amount > n:
                break
            curr_amt += self.messages[-i-1].token_amount
            conversation_excerpt.add_message(self.messages[-i-1].content,
                                    self.messages[-i-1].author_as_enum, 
                                    self.messages[-i-1].token_amount
                                    )
            i+=1 

        # reverse the messages so that they're in chronological order
        conversation_excerpt.messages.reverse()

        return conversation_excerpt
    
    def remove(self, string: str):
        for message in self.messages[::-1]:
            if message.content == string:
                self.messages.remove(message)
    
    def clear(self):
        self.messages: List[self.Message] = []
