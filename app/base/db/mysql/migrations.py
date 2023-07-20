import database


class Migration01:

    def __init__(self):
        db = database.Mysql()
        self.connect = db.connection
        self.cursor = db.cursor

    def up(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS person_info(
            chat_id INT PRIMARY KEY,
            first_name VARCHAR(50),
            last_name VARCHAR(50),
            type VARCHAR(30),
            username VARCHAR(255),
            date DATETIME,
            title VARCHAR(255))
            """
        )

    def down(self):
        self.cursor.execute(
            """
                DROP TABLE IF EXISTS person_info
            """
        )


connection = Migration01()
try:
    connection.up()
    print("Query executing succeeded")
except Exception as e:
    print(f"Query error execution: {e}\n")
    print('Rollback')
    #connection.down()
