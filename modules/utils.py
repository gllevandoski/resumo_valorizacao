def load_config(cfg_type, config) -> dict:
    from json import loads
    with open("modules/coordinates.json") as f:
        file = f.read()
    return loads(file)[cfg_type][config]


def str_to_float(string) -> float:
    try:
        return float(string.replace(".", "").replace(",", "."))
    except Exception:
        return "error"


def return_last_empty_row(spreadsheet) -> int:
    for row in spreadsheet.iter_rows(min_row=3, min_col=2, max_col=2):
        if row[0].value is None:
            return row[0].row


def cleanse_digits_list(dirty_list) -> list:
    from string import digits
    clean_list = list()

    for item in dirty_list:
        for digit in digits:
            if digit in item:
                clean_list.append(str_to_float(item))
                break

    return clean_list
