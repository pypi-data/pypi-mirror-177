from aqua_cli.database import execute_query

def change_amount(target, amount):
    day, current_intake = get_queries()
    intake = current_intake
    new_intake = 0

    if amount <= 0:
        print('ERROR: invalid amount.')
        return
    
    if target == 'add':
        new_intake = add(amount, intake)
    elif target == 'remove':
        new_intake = remove(amount, intake)

    execute_query.execute_query(
        query='UPDATE aqua SET intake = ? WHERE day = ?',
        parameters=[new_intake, day]
    )

def add(amount, intake):
    new_intake = intake + amount
    print(f'Added {amount}ml.')

    return new_intake

def remove(amount, intake):
    new_intake = intake - amount
    
    if intake <= 0:
        print('Your intake is currently 0, you can\'t remove.')
        return 0
    if new_intake < 0:
        print('If you remove this amount, your intake will be less than zero.')
        return 0

    print(f'Removed {amount}ml.')
    return new_intake

def get_queries():
    day = execute_query.execute_query(
        query='SELECT day FROM aqua ORDER BY day DESC',
        return_value=True
    )
    
    current_intake = execute_query.execute_query(
        query='SELECT intake FROM aqua ORDER BY day DESC',
        return_value=True
    )
    
    return day[0], current_intake[0]
