import flask_login

def convert_to_dict(cur):
    dictio = [dict(line) for line in
    [zip([column[0] for column in cur.description], row) for row in cur.fetchall()]]
    return dictio


def add_quote_to_str(param):
    if type(param) is str:
        param = "'" + param + "'"
    return param