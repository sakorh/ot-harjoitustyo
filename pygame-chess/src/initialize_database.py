from database_connection import get_database_connection


def drop_tables(connection):
    cursor = connection.cursor()

    cursor.execute("""
        drop table if exists Fen;
    """)
    connection.commit()


def create_tables(connection):
    db = \
    """
    CREATE TABLE Fen (
        name text PRIMARY KEY,
        fen text
    );
    INSERT INTO Fen VALUES('Starting Position','rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w');
    """
    connection.cursor().executescript(db)
    connection.commit()

def initialize_database():
    connection = get_database_connection()

    drop_tables(connection)
    create_tables(connection)

if __name__ == "__main__":
    initialize_database()
