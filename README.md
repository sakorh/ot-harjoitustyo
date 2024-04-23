## Ohjelmistotekniikka, harjoitustyö
Sovelluksessa voi pelata kaksin pelattavaa shakkia.

### Dokumentaatio
- [Vaatimusmäärittely](https://github.com/sakorh/ot-harjoitustyo/blob/master/dokumentaatio/vaatimusmaarittely.md)
- [Arkkitehtuurikuvaus](https://github.com/sakorh/ot-harjoitustyo/blob/master/dokumentaatio/arkkitehtuuri.md)
- [Työaikakirjanpito](https://github.com/sakorh/ot-harjoitustyo/blob/master/dokumentaatio/tuntikirjanpito.md)
- [Changelog](https://github.com/sakorh/ot-harjoitustyo/blob/master/dokumentaatio/changelog.md)

### Release
- [Release](https://github.com/sakorh/ot-harjoitustyo/releases/tag/viikko5)

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
