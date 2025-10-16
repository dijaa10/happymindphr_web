from collections import Counter
from sqlalchemy import inspect
def object_as_dict(obj):
    """object_as_dict 
    Change object data to dict
    Keyword arguments:
    obj -- Object data to convert
    Return: dict
    """
    
    return {c.key: getattr(obj, c.key) for c in inspect(obj).mapper.column_attrs}


def get_string_word_total(message=str):
    word_list = message.lower().split()
    word_count = len(word_list)
    word_frequencies = Counter(word_list)
    return word_frequencies