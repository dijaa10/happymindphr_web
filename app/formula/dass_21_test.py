from app.config import session
from app.models.Dass21Answer import Dass21Answer
import pprint
from app.rules.dass_21_test_rule import *

def test_result(question_data=None):
    """
    Calculates the DASS-21 scores for depression, anxiety, and stress
    based on the provided question data.

    This function first separates the questions into three categories: depression,
    anxiety, and stress. It then calculates a raw score for each category by
    summing the answer values and multiplying by two. Finally, it determines
    the severity level for each category based on the calculated scores.

    Args:
        question_data (list, optional): A list of dictionaries, where each
            dictionary contains a 'question_no' and an 'answer_value'.
            Example: [{"answer_no": 1, "answer_value": 1, "question_no": 1}, ...].

    Returns:
        dict: A dictionary containing the calculated scores and severity
            levels for depression, anxiety, and stress.
            Example:
            {
                "depression": {
                    "d_score": 10,
                    "level": "mild"
                },
                "anxiety": {
                    "a_score": 8,
                    "level": "normal"
                },
                "stress": {
                    "s_score": 12,
                    "level": "moderate"
                }
            }
    """
    question_data, depression_questions = get_depresion(question_data)
    question_data, anxiety_questions = get_anxiety(question_data)
    stres_questions = question_data
    dass21_total = {
       "depression":{
         "d_score": calculate_test(depression_questions),
         "level": rule_depression_level(calculate_test(depression_questions))
       },
       "anxiety":{
         "a_score": calculate_test(anxiety_questions),
         "level": rule_anxiety_level(calculate_test(anxiety_questions))
       },
       "stress":{
         "s_score": calculate_test(stres_questions),
         "level": rule_stress_level(calculate_test(stres_questions))
       }   
    }
    return dass21_total


def get_depresion(question_data=None):
    """Get D Question (3, 5, 10, 13, 16, 17, 21)"""
    depression_questions = [3, 5, 10, 13, 16, 17, 21]
    d_score = []
    for item in question_data:
        if item['question_no'] in depression_questions:
            d_score.append(item)
            question_data.remove(item)

    return question_data, d_score

def get_anxiety(question_data=None):
    """Get A Question (2, 4, 7, 9, 15, 19, 20)"""
    anxiety_questions = [2, 4, 7, 9, 15, 19, 20]
    a_score = []
    for item in question_data:
        if item['question_no'] in anxiety_questions:
            a_score.append(item)
            question_data.remove(item)

    return question_data, a_score

def calculate_test(category):
    """Calculate the test """
    category_sum = sum(item['answer_value'] for item in category)
    return category_sum * 2
    
