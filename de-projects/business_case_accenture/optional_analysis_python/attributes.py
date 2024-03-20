def is_float_try(num_f:str) -> bool:
    try:
        float(num_f)
        return True
    except ValueError:
        return False


PATH_CLIENTS = '.'
PATH_HOUSEHOLD = '.'
INCOME_PATH = '.'
LOAN_PATH = '.'
PROCESSED_PATH='.'