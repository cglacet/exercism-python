"""This is an exercise from https://exercism.io/my/tracks/python"""
from app_skeleton import Application

DEFAULT_APP = Application()
DEFAULT_APP.add_tables_index({'users': 'name'})


@DEFAULT_APP.route("/users", method="GET")
def users(database, arguments):
    """Returns the list of `users` details. The argument `users` could be a list
    of names or a single user name."""
    if not arguments:
        return filter_by_index(database, 'users')
    try:
        user_names = arguments['users']
        if isinstance(user_names, list):
            return filter_by_index(database, 'users', *user_names)
        else:
            return filter_by_index(database, 'users', user_names)
    except KeyError:
        return {'error': 'malformed request'}


@DEFAULT_APP.route("/add", method="POST")
def add_user(database, arguments):
    """Create a new user."""
    username = arguments['user']
    new_user = {
        'name': username,
        'owes': {},
        'owed_by': {},
        'balance': 0
    }
    # database['users'][username] = new_user # Wouldn't seem very usefull.
    return new_user


@DEFAULT_APP.route("/iou", method="POST")
def iou(database, arguments):
    """Returns updated balances after `lender` lended `amount` to `borrower`
    all these three arguments are mendatory.
    """
    table = database['users']
    try:
        l_name = arguments['lender']
        b_name = arguments['borrower']
        amount = arguments['amount']
    except KeyError as key:
        return {'error': f"Missing argument: {key}"}
    try:
        lender = table[l_name]
        borrower = table[b_name]
    except KeyError as key:
        return {'error': f"user {key} deosn't seem to appear in table {table.name}"}
    try:
        if b_name not in lender['owed_by']:
            lender['owed_by'][borrower['name']] = 0

        if l_name not in borrower['owes']:
            borrower['owes'][l_name] = 0

        borrower['owes'][l_name] += amount
        borrower['balance'] -= amount
        lender['owed_by'][b_name] += amount
        lender['balance'] += amount

        cancel_debts(lender, borrower)
        cancel_debts(borrower, lender)

        return filter_by_index(database, 'users', l_name, b_name)

    except KeyError as key:
        return {'error': f"malformed database: no such column {key}"}


def cancel_debts(person, other_person):
    """If two person mutually owes something to the other, then they resolve part
    of their debts. This function cancel debts so only one person owes the other."""
    does_owe = other_person['name'] in person['owes']
    is_owed = other_person['name'] in person['owed_by']
    if does_owe and is_owed:
        balance = person['owed_by'][other_person['name']] - person['owes'][other_person['name']]
        if balance > 0:
            person['owed_by'][other_person['name']] = balance
            del person['owes'][other_person['name']]
        else:
            person['owes'][other_person['name']] = -balance
            del person['owed_by'][other_person['name']]


def filter_by_index(database, table_name, *keys):
    """Return the given table with filtered rows. A row is part of the result if
    its index match one of the keys."""
    rows = [database[table_name][k] for k in keys]
    sort_column = database[table_name].index
    return {table_name: sorted(rows, key=lambda row: str.lower(row[sort_column]))}


# Uggly hack, but I couldn't find a cleaner solution (PART 2),
# you thought 'RestAPI' was a class? Well, I'm sorry :D
RestAPI = DEFAULT_APP


if __name__ == "__main__":
    import json
    db = {'users': []}
    api = RestAPI(db)
    print(isinstance(api, RestAPI))
    for name in 'Alice', 'Bob', 'Chris':
        new_user = json.loads(api.post('/add', json.dumps({'user': name})))
        db['users'].append(new_user)

    api = RestAPI(db)
    payload = json.dumps({
        'lender': 'Alice',
        'borrower': 'Bob',
        'amount': 4.0
    })
    response = json.loads(api.post('/iou', payload))

    def index(array, value, key=lambda x: x):
        for i, v in enumerate(array):
            if key(v) == value:
                return i

    for user in response['users']:
        user_db_index = index(db['users'], user['name'], key=lambda u: u['name'])
        db['users'][user_db_index] = user

    print(db)
