__author__ = 'ashahab'
import random
from src.joinhour.models.token import Token
class TokenGenerator(object):
    RANDOM_RANGE_FROM = 99999
    RANDOM_RANGE_TO = 999999
    @classmethod
    def generate_tokens(cls, number_of_tokens):
        list_of_tokens = set();
        random.seed()
        while len(list_of_tokens) < number_of_tokens:
            newToken = random.randint(cls.RANDOM_RANGE_FROM, cls.RANDOM_RANGE_TO)
            matchedToken = Token.match(newToken)
            if matchedToken:
                continue
            list_of_tokens.add(newToken)
        return list_of_tokens


    @classmethod
    def create_tokens(cls, number_of_tokens):
        list_of_tokens = cls.generate_tokens(number_of_tokens)
        for t in list_of_tokens:
            token = Token(value=t)
            token.put()

    @classmethod
    def create_tokens_for_group(cls, number_of_tokens, group_name):
        list_of_tokens = cls.generate_tokens(number_of_tokens)
        for t in list_of_tokens:
            token = Token(value=t, belongs_to_group=group_name)
            token.put()