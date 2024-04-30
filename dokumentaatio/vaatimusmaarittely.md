## Vaatimusmäärittely

### Sovelluksen tarkoitus
Sovelluksessa voi pelata kaksin pelattavaa shakkia.

### Suunnitellut perustoiminnallisuudet
- Peli käynnistyy shakin aloitusasetelmaan - tehty
- Pelaajat voivat liikuttaa vuorotellen mustia ja valkoisia nappuloita - tehty
  - Oman vuoron jälkeen siis ainoastaan vastustajan nappuloita on mahdollista liikuttaa - tehty
- Nappuloita voi liikuttaa vain shakin sääntöjen mukaisesti - tehty osittain (esim. sotilaiden korotus ja linnoittautuminen puuttuu)
- Valitsemalla jonkin tietyn nappulan peli näyttää kaikki mahdolliset ruudut, joihin nappulan voi siirtää - tehty
- Peli päättyy joko shakkimattiin, jossa toinen pelaaja voittaa, tai pattiin eli tasapeliin - tehty
  - Sovellus ilmoittaa pelin loppumisesta - tehty
- Pelin päätyttyä pelaajilla on mahdollisuus aloittaa uusi peli - tehty
- Pelaaja voi keskeyttää pelin meneillään olevan pelin ja aloittaa uuden milloin vain - (oli tehtynä, mutta odottamattomista ongelmista johtuen jouduin viime hetkellä palaamaan vanhempaan versioon projektista)

### Mahdollisia jatkokehitysideoita
- Kummankin pelaajan syödyt nappulat näkyvät pelilaudan vieressä
- Peli varoittaa uhattuna olevaa pelaajaa shakkitilanteissa
- (Mahdollisuus ajanottoon)
- Pelilaudan alustus syöttämällä FEN-asetelma käsin - tehty osittain (koodissa ei ole vielä virheellisten syötteiden tarkistusta)
- Pelilaudan sen hetkisen asetelman tallennus tietokantaan - oli tehtynä osittain, ei toimi vielä
- Pelaaja voi milloin vain valita tallentamansa asetelman ja jatkaa pelaamista siitä - oli tehtynä osittain, ei toimi vielä
