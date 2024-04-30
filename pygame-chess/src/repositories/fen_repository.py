from database_connection import get_database_connection
from initialize_database import initialize_database


class FENRepository:
    """Luokka tietokantaoperaatioille.
    """

    def __init__(self):
        initialize_database()
        self._connection = get_database_connection()
        self._cursor = self._connection.cursor()

    def select_fen(self, name):
        """Valitsee parametrina annettua nimeä vastaavan FEN-asetelman tietokannasta.
        """
        self._cursor.execute("select fen from Fen where name=(?)", (name,))
        row = self._cursor.fetchone()

        return row["fen"]

    def get_fens(self):
        """Hakee ja palauttaa kaikki tietokantaan tallennetut FEN-asetelmat.
        """
        self._cursor.execute("select * from Fen")
        rows = self._cursor.fetchall()

        fens = [row["name"] for row in rows]
        return fens

    def save_fen(self, fen, name):
        """Tallentaa pelilaudalla tallennushetkellä olevan asetelman tietokantaan.
        Käyttäjä voi itse määrittää asetelmalle nimen.
        """
        self._cursor.execute(
            "insert into Fen (name, fen) values (?, ?)", (name, fen))
        self._connection.commit()
