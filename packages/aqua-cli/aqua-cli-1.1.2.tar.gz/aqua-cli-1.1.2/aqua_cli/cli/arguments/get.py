from aqua_cli.database import execute_query

def get(target):
    db_data = get_queries()

    if target == 'get':
        get_intake(db_data)
    elif target == 'get-all':
        get_all(db_data)

def get_all(db_data):
    print('Intake history:')
    for value in db_data:
        day = value[0]
        intake = value[1]
        goal = value[2]

        print(f' DAY {day}: {intake}/{goal}ml')

def get_intake(db_data):
    day = db_data[0][0]
    intake = db_data[0][1]
    goal = db_data[0][2]
        
    print(f'Your intake [DAY {day}]: {intake}/{goal}ml')

def get_queries():
    db_data = execute_query.execute_query(
        query='SELECT * FROM aqua ORDER BY day DESC',
        return_value=True,
        return_all=True
    )
    
    return db_data