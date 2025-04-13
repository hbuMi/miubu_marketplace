# miubu_marketplace
second hand clothing marketplace

- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan ilmoituksia.
- Käyttäjä pystyy lisäämään kuvia ilmoitukseen.
- Käyttäjä näkee sovellukseen lisätyt ilmoitukset.
- Käyttäjä pystyy etsimään ilmoituksia hakusanalla.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät ilmoitukset.
- Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (esim. ilmoituksen osasto, tavaran kunto).
- Käyttäjä pystyy ostamaan ja tarjoamaan hintaa myynnissä olevista tuotteista.

Nykyinen tilanne:
- Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
- Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan ilmoituksia.
- Käyttäjä näkee sovellukseen lisätyt ilmoitukset.
- Käyttäjä pystyy etsimään ilmoituksia hakusanalla.
- Sovelluksessa on käyttäjäsivut, jotka näyttävät tilastoja ja käyttäjän lisäämät ilmoitukset.
- Käyttäjä pystyy valitsemaan ilmoitukselle yhden tai useamman luokittelun (esim. ilmoituksen osasto, tavaran kunto).

Asennusohje:
Luo virtuaaliympäristö:
- python3 -m venv venv

Aktivoi virtuaaliympäristö:
- Windows:
  - venv\Scripts\activate
- Mac/Linux:
  - source venv/bin/activate

Asenna tarvittavat Python-kirjastot:
- pip install flask

Luo tietokannan taulut, sovelluksessa käytetään SQLite-tietokantaa. Luo tietokannan taulut ajamalla seuraava komento:
- python app.py

Suorita sovellus. Kun kaikki on asetettu, voit käynnistää sovelluksen seuraavalla komennolla:
- flask run
