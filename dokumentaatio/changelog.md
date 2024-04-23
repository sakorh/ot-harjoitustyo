## Viikko 3

- Peli käynnistyy shakin aloitusasetelmaan
    - (Nappuloiden kuvat: https://pixabay.com/vectors/chess-pieces-chessboard-board-game-6084642/)
- Nappulan valitessa klikkaamalla pelilaudalla näkyy sen liikkumisvaihtoehdot
- Jokaiselle erilaiselle nappulalle oma luokka sprites-alihakemistossa, joka luo kunkin nappula-olion
- Board-luokka, joka vastaa pelilaudan piirtämisestä ja nappuloiden alustuksesta ja siirroista
- GameLoop-luokka vastaa pelisilmukasta ja pelin näkymän päivittämisestä pelaajien syötteiden mukaisesti
- Vain valkoinen voi aloittaa pelin ja vain yhtä nappulaa voi siirtää yhden vuoron aikana
- Testattu, että sotilasnappuloiden siirrot onnistuvat ja ettei nappulaa voi siirtää samaan ruutuun toisen nappulan kanssa


## Viikko 4
- Erotettu nappuloiden kuvien lataus, pygamen tapahtumajono, pelinäkymän piirtäminen ja aika omiksi ohjelmiksi
- Pelajaat voivat syödä toistensa nappuloita shakin sääntöjen mukaisesti
- Parannettu nappuloiden liikkumista vastaamaan shakin sääntöjä
- Jos kuningas on shakissa, ainoat liikkumisvaihtoehdot ovat pois shakista
- Peli päättyy jos kuningas on shakissa eikä laillisia siirtoja ole
- Sovelluslogiikka siirretty ChessService luokkaan
- Käyttöliittymä siirretty ui-hakemistoon
- Testattu, että torneilla ei voi liikkua muiden nappuloiden yli, ja että shakkitilanteessa kuningasta ei voi siirtää ruutuun, jossa se olisi shakissa

## Viikko 5
- Nyt myös vastustajan syötävät nappulat näkyvät liikkumisvaihtoehtoina nappulan valitessa
- Peli päättyy pattitilanteessa shakin sääntöjen mukaisesti
- Pelin päätyttyä voi aloittaa uuden pelin
- Testattu, että sotilasnappulalla voi syödä vastustajan nappulan
- Testattu, että pattiasetelma ja tilanne, jossa kuningas ei pääse liikkumaan pois shakista päättävät pelin
- Refaktoroitu sovelluslogiikan koodia ChessService-luokassa, käyttöliittymään liittyvää koodia Board-luokassa ja siirretty pelinäkymän piirtoon liittyvä koodi GameLoop-luokasta Renderer-luokkaan


