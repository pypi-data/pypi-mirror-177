from aqua_cli.database import (create_connection, execute_query)

def setup(age, weight):
    create_connection.create_connection()
    goal = weight * 40

    if age >= 18 and age <= 55:
        goal = weight * 35
    elif age >= 55 and age <= 65:
        goal = weight * 30
    elif age >= 66:
        goal = weight * 25
    
    print(f'Your intake goal: {goal}ml.')
    execute_query.execute_query(
        query='UPDATE aqua SET goal = ?', 
        parameters=[goal]
    )