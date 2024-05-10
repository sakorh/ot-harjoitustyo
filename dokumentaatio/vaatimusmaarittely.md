# Vaatimusmäärittely

## Sovelluksen tarkoitus
Sovelluksessa voi pelata kaksin pelattavaa shakkia. Pelin voi aloittaa normaalisti shakin aloitusasetelmasta tai pelilaudan voi alustaa halutessaan omalla asetelmalla. Sovelluksessa on myös mahdollista tallentaa keskeneräinen peli ja jatkaa sen pelaamista myöhemmin.

## Perustoiminnallisuudet

### Ennen pelin aloitusta
  - Pelin voi käynnistää shakin aloitusasetelmaan
  - Pelaaja voi alustaa pelilaudan syöttämällä oman asetelmansa FEN-notaatiolla
  - Pelaaja voi valita jonkin aiemmin tallennetuista asetelmista ja jatkaa peliä siitä

### Pelin aloituksen jälkeen
- Pelaajat voivat liikuttaa vuorotellen mustia ja valkoisia nappuloita
  - Oman vuoron jälkeen siis ainoastaan vastustajan nappuloita on mahdollista liikuttaa
- Nappuloita voi liikuttaa vain shakin sääntöjen mukaisesti
    - Jotkin erikoissiirrot kuten sotilaiden korotus ja linnoittautuminen puuttuvat
- Valitsemalla jonkin tietyn nappulan peli näyttää kaikki mahdolliset ruudut, joihin nappulan voi siirtää
- Peli päättyy joko shakkimattiin, jossa toinen pelaaja voittaa, tai pattiin eli tasapeliin
  - Sovellus ilmoittaa pelin loppumisesta
- Pelin päätyttyä pelaajilla on mahdollisuus aloittaa uusi peli
- Pelaaja voi keskeyttää meneillään olevan pelin ja aloittaa uuden milloin vain
- Pelaaja voi tallentaa sen hetkisen pelilaudan asetelman tietokantaan

## Mahdollisia jatkokehitysideoita
- Kummankin pelaajan syödyt nappulat näkyvät pelilaudan vieressä
- Peli varoittaa uhattuna olevaa pelaajaa shakkitilanteissa
- Mahdollisuus ajanottoon
- Mahdollisuus luoda erillisiä käyttäjiä, joilla omat tallennetut asetelmat
