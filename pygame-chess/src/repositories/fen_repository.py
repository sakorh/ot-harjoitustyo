from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from database_connection import session, initialize_database
from models import FEN


class FENRepository:
    """Luokka tietokantaoperaatioille.
    """

    def __init__(self):
        """Luokan konstruktori. Alustaa tietokannan.
        """
        initialize_database()
        self._session = session

    def select_fen(self, name):
        """
        Valitsee parametrina annettua nimeä vastaavan FEN-asetelman tietokannasta.

        Args:
            name: asetelman nimi, joka tietokannasta halutaan hakea.

        Returns:
            Palauttaa nimeä vastaavan FEN-asetelman merkkijonona.
        """
        with self._session() as s:
            statement = select(FEN.fen).filter_by(name=name)
            row = s.execute(statement).one_or_none()

        return row[0]

    def get_fens(self):
        """
        Hakee ja palauttaa kaikki tietokantaan tallennetut FEN-asetelmat.
        """
        with self._session() as s:
            statement = select(FEN.name, FEN.fen)
            rows = s.execute(statement).all()

        fens = [row[0] for row in rows]
        return fens

    def save_fen(self, fen, name):
        """
        Tallentaa pelilaudalla tallennushetkellä olevan asetelman tietokantaan.
        Käyttäjä voi itse määrittää asetelmalle nimen.

        Args:
            fen: tallennettava asetelma.
            name: asetelman nimi.

        Returns:
            Virheilmoituksen, jos käyttäjän syöttämällä nimellä on jo asetelma tallennettuna
            tietokantaan.
            Muuten None.
        """
        with self._session() as s:
            try:
                new_fen = FEN(name=name, fen=fen)
                s.add(new_fen)
                s.commit()
            except IntegrityError:
                s.rollback()
                return f"'{name}' already in database."
        return None

    def delete_fen(self, name):
        """Postaa parametrina annettua nimeä vastaavan asetelman tietokannasta.

        Args:
            name: sen asetelman nimi, joka halutaan poistaa.
        """
        with self._session() as s:
            statement = delete(FEN).where(FEN.name == name)
            s.execute(statement)
            s.commit()

    def delete_all(self):
        """Poistaa kaikki asetelmat tietokannasta.
        """
        with self._session() as s:
            statement = delete(FEN)
            s.execute(statement)
            s.commit()


fen_repository = FENRepository()
