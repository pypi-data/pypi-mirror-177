from aqua_cli.database import execute_query

def check_intake():
    query = get_queries()
    day = query[0]
    intake = query[1]
    goal = query[2]
    
    if intake >= goal:
        skip_day(day, intake, goal)

def skip_day(day, intake, goal):
    print(f'Reached your goal!\n {intake}/{goal}ml.')
    execute_query.execute_query(
            query='INSERT INTO aqua (day, intake, goal) VALUES(?, ?, ?)',
            parameters=[day + 1, 0, intake]
        )
    
    print(f'You are now on day {day + 1}!')

def get_queries():
    query = execute_query.execute_query(
        query='SELECT * FROM aqua ORDER BY day DESC',
        return_value=True,
    )
    
    return query