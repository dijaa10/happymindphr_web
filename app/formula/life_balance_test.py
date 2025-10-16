def calculate_test(question_data):
    """
    Calculates a burnout score based on a list of answers and provides
    a corresponding explanation.

    This function sums the 'answer_value' from each item in the provided list,
    divides the total by 12, and then uses the resulting score to determine
    a level of burnout. It returns a dictionary containing the calculated
    score and a human-readable explanation in Indonesian.

    Args:
        question_data (list): A list of dictionaries, where each dictionary
            contains a key 'answer_value' with an integer value.

    Returns:
        dict: A dictionary with two keys:
            - 'result' (float): The calculated burnout score.
            - 'explanation' (str): A message explaining the burnout level.

    Raises:
        TypeError: If 'question_data' is not a list of dictionaries.
        KeyError: If a dictionary in 'question_data' does not contain the
                  'answer_value' key.
    """
    sum_question_data = sum(item["answer_value"] for item in question_data)
    calculate = sum_question_data / 12
    result = {}
    if calculate >= 1.00 or calculate <= 2.53:
        result = {
            "result": round(calculate,2),
            "explanation": "Burnout kemungkinan besar bukan masalah bagi Anda.",
        }
    elif calculate >= 2.54 or calculate <= 2.95:
        result = {
            "result": round(calculate,2),
            "explanation": "Anda mungkin akan mendapatkan manfaat jika mencari bantuan (atau mencoba sesuatu yang berbeda).",
        }
    else:
         result = {
            "result": round(calculate,2),
            "explanation": "Anda sangat disarankan untuk mencari bantuan.",
        }
    return result
