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

Asennusohjeet:

Kloonaa projekti koneelle:
- git clone git@github.com:hbuMi/miubu_marketplace.git

Luo virtuaaliympäristö:
- python3 -m venv venv

Aktivoi virtuaaliympäristö:
- Windows:
  - venv\Scripts\activate
- Mac/Linux:
  - source venv/bin/activate

Asenna riippuvuudet:
- pip install flask

Luo tietokanta:
- sqlite3 database.db < schema.sql
  sqlite3 database.db < init.sql

Käynnistä:
- flask run
