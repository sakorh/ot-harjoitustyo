## Ohjelmistotekniikka, harjoitustyö

### Dokumentaatio
- [Vaatimusmäärittely](https://github.com/sakorh/ot-harjoitustyo/blob/master/dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuurikuvaus](https://github.com/sakorh/ot-harjoitustyo/blob/master/dokumentaatio/arkkitehtuuri.md)
- [Työaikakirjanpito](https://github.com/sakorh/ot-harjoitustyo/blob/master/dokumentaatio/tuntikirjanpito.md)
- [Changelog](https://github.com/sakorh/ot-harjoitustyo/blob/master/dokumentaatio/changelog.md)

### Pelin käynnistysohjeet
- Siirry pygame-chess hakemistoon ja asenna tarvittavat riippuvuudet
 ```
poetry install
 ```
- Käynnistä peli
```
poetry run invoke start
```
### Testaus
- Testit voi suorittaa komennolla:
```
poetry run invoke test
```
- Ja testikattavuusraportin saa generoitua komennolla:
```
poetry run invoke coverage-report
```
### Pylint
- Pylint-tarkistukset voi suorittaa komennolla:
 ```
poetry run invoke lint
 ```
