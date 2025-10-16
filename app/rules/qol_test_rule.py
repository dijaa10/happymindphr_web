def rule(value):
    match (value):
        case num if num in range(0,26):
            return "Poor QoL/Kurang"
        case num if num in range(26,51):
            return "Cukup"
        case num if num in range(51,76):
            return "Baik"
        case (_):
            return "Sangat Baik"
            