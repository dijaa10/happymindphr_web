
from app.rules.qol_test_rule import rule
def calculate_test(question_data=None):
    """
    Calculates and interprets the quality of life results across four domains.

    This function processes a dictionary of question data, passing it to separate
    domain-specific calculation functions. It then uses the results to produce
    an interpreted score for each domain based on a defined rule.

    Args:
        question_data (dict, optional): A dictionary containing the raw question
            data. Defaults to None.

    Returns:
        dict: A dictionary containing the calculated and interpreted results for
            each of the four domains. The structure is as follows:
            {
                "domain_1": {
                    "result": <calculated_score>,
                    "interpreted_result": <interpreted_score>
                },
                "domain_2": {
                    "result": <calculated_score>,
                    "interpreted_result": <interpreted_score>
                },
                "domain_3": {
                    "result": <calculated_score>,
                    "interpreted_result": <interpreted_score>
                },
                "domain_4": {
                    "result": <calculated_score>,
                    "interpreted_result": <interpreted_score>
                }
            }
    """
    total,transform_d1_total = calculate_domain_1(question_data)
    total,transform_d2_total = calculate_domain_2(question_data)
    total,transform_d3_total = calculate_domain_3(question_data)
    total,transform_d4_total = calculate_domain_4(question_data)
    qol_result = {
        "domain_1":{
            "result":transform_d1_total,
            "interpreted_result":rule(transform_d1_total)
        },
        "domain_2":{
            "result":transform_d2_total,
            "interpreted_result":rule(transform_d2_total)
        },
        "domain_3":{
            "result":transform_d3_total,
            "interpreted_result":rule(transform_d3_total)
        },
        "domain_4":{
            "result":transform_d4_total,
            "interpreted_result":rule(transform_d4_total)
        },
    }
    return qol_result


def calculate_domain_1(question_data):
    """
    Take the question and calculate [3,4,10,15,16,17,18]
    Additional note: Q3 & Q4 must minus by 6 before sum all of value
    """
    domain_1_q = [3, 4, 10, 15, 16, 17, 18]
    minus_1_q = [3, 4]
    domain_1_q_total = 0
    for item in question_data:
        if item["question_no"] in domain_1_q:
            if item["question_no"] in minus_1_q:
                minus = 6 - item["answer_value"]
                domain_1_q_total += minus
            else:
                domain_1_q_total += item["answer_value"]
    transform_data = domain_1_transformation(domain_1_q_total)
    return domain_1_q_total, transform_data


def calculate_domain_2(question_data):
    """
    Take the question and calculate [5,6,7,11,19,26]
    Additional note: Q26 must minus by 6 before sum all of value
    """
    domain_2_q = [5,6,7,11,19,26]
    minus_2_q = [6]
    domain_2_q_total = 0
    for item in question_data:
        if item["question_no"] in domain_2_q:
            if item["question_no"] in minus_2_q:
                minus = 6 - item["answer_value"]
                domain_2_q_total += minus
            else:
                domain_2_q_total += item["answer_value"]
    transform_data = domain_2_transformation(domain_2_q_total)
    return domain_2_q_total, transform_data


def calculate_domain_3(question_data):
    """
    Take the question and calculate [20,21,22]
    """
    domain_3_q = [20,21,22]
    domain_3_q_total = 0
    for item in question_data:
        if item["question_no"] in domain_3_q:
            domain_3_q_total += item["answer_value"]
    transform_data = domain_3_transformation(domain_3_q_total)
    return domain_3_q_total, transform_data


def calculate_domain_4(question_data):
    """
    Take the question and calculate [8,9,12,13,14,23,24,25]
    """
    domain_4_q = [8,9,12,13,14,23,24,25]
    domain_4_q_total = 0
    for item in question_data:
        if item["question_no"] in domain_4_q:
            domain_4_q_total += item["answer_value"]
    transform_data = domain_4_transformation(domain_4_q_total)
    return domain_4_q_total, transform_data


def domain_1_transformation(total_score: int):
    # TODO Implement the transformation
    transformation_data = [
        {"score": 7, "transform_value": 0},
        {"score": 8, "transform_value": 6},
        {"score": 9, "transform_value": 6},
        {"score": 10, "transform_value": 13},
        {"score": 11, "transform_value": 13},
        {"score": 12, "transform_value": 19},
        {"score": 13, "transform_value": 19},
        {"score": 14, "transform_value": 25},
        {"score": 15, "transform_value": 31},
        {"score": 16, "transform_value": 31},
        {"score": 17, "transform_value": 38},
        {"score": 18, "transform_value": 38},
        {"score": 19, "transform_value": 44},
        {"score": 20, "transform_value": 44},
        {"score": 21, "transform_value": 50},
        {"score": 22, "transform_value": 56},
        {"score": 23, "transform_value": 56},
        {"score": 24, "transform_value": 63},
        {"score": 25, "transform_value": 63},
        {"score": 26, "transform_value": 69},
        {"score": 27, "transform_value": 69},
        {"score": 28, "transform_value": 75},
        {"score": 29, "transform_value": 81},
        {"score": 30, "transform_value": 81},
        {"score": 31, "transform_value": 88},
        {"score": 32, "transform_value": 88},
        {"score": 33, "transform_value": 94},
        {"score": 34, "transform_value": 94},
        {"score": 35, "transform_value": 100},
    ]
    transform_value = search_transformation_value(transformation_data,total_score)
    return transform_value


def domain_2_transformation(total_score: int):
    transformation_data = [
        {"score": 6, "transform_value": 0},
        {"score": 7, "transform_value": 6},
        {"score": 8, "transform_value": 6},
        {"score": 9, "transform_value": 13},
        {"score": 10, "transform_value": 19},
        {"score": 11, "transform_value": 19},
        {"score": 12, "transform_value": 25},
        {"score": 13, "transform_value": 31},
        {"score": 14, "transform_value": 31},
        {"score": 15, "transform_value": 38},
        {"score": 16, "transform_value": 44},
        {"score": 17, "transform_value": 44},
        {"score": 18, "transform_value": 50},
        {"score": 19, "transform_value": 56},
        {"score": 20, "transform_value": 56},
        {"score": 21, "transform_value": 63},
        {"score": 22, "transform_value": 69},
        {"score": 23, "transform_value": 69},
        {"score": 24, "transform_value": 75},
        {"score": 25, "transform_value": 81},
        {"score": 26, "transform_value": 81},
        {"score": 27, "transform_value": 88},
        {"score": 28, "transform_value": 94},
        {"score": 29, "transform_value": 94},
        {"score": 30, "transform_value": 100},
    ]
    transformation_val = 0
    for item in transformation_data:
        if item["score"] == total_score:
            transform_value = item["transform_value"]
    return transform_value


def domain_3_transformation(total_score: int):
    transformation_data = [
        {"score": 3, "transform_value": 0},
        {"score": 4, "transform_value": 6},
        {"score": 5, "transform_value": 19},
        {"score": 6, "transform_value": 25},
        {"score": 7, "transform_value": 31},
        {"score": 8, "transform_value": 44},
        {"score": 9, "transform_value": 50},
        {"score": 10, "transform_value": 56},
        {"score": 11, "transform_value": 69},
        {"score": 12, "transform_value": 75},
        {"score": 13, "transform_value": 81},
        {"score": 14, "transform_value": 94},
        {"score": 15, "transform_value": 100},
    ]
    transformation_val = 0
    for item in transformation_data:
        if item["score"] == total_score:
            transform_value = item["transform_value"]
    return transform_value


def domain_4_transformation(total_score: int):
    transformation_data = [
        {"score": 8, "transform_value": 0},
        {"score": 9, "transform_value": 6},
        {"score": 10, "transform_value": 6},
        {"score": 11, "transform_value": 13},
        {"score": 12, "transform_value": 13},
        {"score": 13, "transform_value": 19},
        {"score": 14, "transform_value": 19},
        {"score": 15, "transform_value": 25},
        {"score": 16, "transform_value": 25},
        {"score": 17, "transform_value": 31},
        {"score": 18, "transform_value": 31},
        {"score": 19, "transform_value": 38},
        {"score": 20, "transform_value": 38},
        {"score": 21, "transform_value": 44},
        {"score": 22, "transform_value": 44},
        {"score": 23, "transform_value": 50},
        {"score": 24, "transform_value": 50},
        {"score": 25, "transform_value": 56},
        {"score": 26, "transform_value": 56},
        {"score": 27, "transform_value": 63},
        {"score": 28, "transform_value": 63},
        {"score": 29, "transform_value": 69},
        {"score": 30, "transform_value": 69},
        {"score": 31, "transform_value": 75},
        {"score": 32, "transform_value": 75},
        {"score": 33, "transform_value": 81},
        {"score": 34, "transform_value": 81},
        {"score": 35, "transform_value": 88},
        {"score": 36, "transform_value": 88},
        {"score": 37, "transform_value": 94},
        {"score": 38, "transform_value": 94},
        {"score": 39, "transform_value": 100},
        {"score": 40, "transform_value": 100},
    ]
    transformation_val = 0
    for item in transformation_data:
        if item["score"] == total_score:
            transform_value = item["transform_value"]
    return transform_value


def search_transformation_value(transformation_data,total_score):
    """sumary_line"""
    transformation_val = 0
    for item in transformation_data:
        if item["score"] == total_score:
            transform_value = item["transform_value"]
    return transform_value
