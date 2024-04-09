## Viikko 3

- Peli käynnistyy shakin aloitusasetelmaan
    - (Nappuloiden kuvat: https://pixabay.com/vectors/chess-pieces-chessboard-board-game-6084642/)
- Nappulan valitessa klikkaamalla pelilaudalla näkyy sen liikkumisvaihtoehdot
- Jokaiselle erilaiselle nappulalle oma luokka sprites-alihakemistossa, joka luo kunkin nappula-olion
- Board-luokka, joka vastaa pelilaudan piirtämisestä ja nappuloiden alustuksesta ja siirroista
- GameLoop-luokka vastaa pelisilmukasta ja pelin näkymän päivittämisestä pelaajien syötteiden mukaisesti
- Vain valkoinen voi aloittaa pelin ja vain yhtä nappulaa voi siirtää yhden vuoron aikana
- Testattu, että sotilasnappuloiden siirrot onnistuvat ja ettei nappulaa voi siirtää samaan ruutuun toisen nappulan kanssa
