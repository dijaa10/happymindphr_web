def rule_depression_level(value):
    match (value):
        case num if num in range(0,10):
            return "Normal"
        case num if num in range(10,14):
            return "Ringan"
        case num if num in range(14,21):
            return "Sedang"
        case num if num in range(21,28):
            return "Parah"
        case (_):
            return "Sangat Parah"

def rule_anxiety_level(value):
    match (value):
        case num if num in range(0,8):
            return "Normal"
        case num if num in range(8,10):
            return "Ringan"
        case num if num in range(10,15):
            return "Sedang"
        case num if num in range(15,20):
            return "Parah"
        case (_):
            return "Sangat Parah"

def rule_stress_level(value):
    match (value):
        case num if num in range(0,15):
            return "Normal"
        case num if num in range(15,19):
            return "Ringan"
        case num if num in range(19,26):
            return "Sedang"
        case num if num in range(26,34):
            return "Parah"
        case (_):
            return "Sangat Parah"