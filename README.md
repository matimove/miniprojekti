# miniprojekti
Ohtu miniprojekti - Ryhmä: OhtuWarriors

[Backlog](https://helsinkifi-my.sharepoint.com/:x:/g/personal/toniemin_ad_helsinki_fi/EYYROFDfQ69EogVpHdGNgz4BX9Zb_ViC6bIx5EghfRbXNg?e=fH4cX5)

## Definition of done

Vaatimus on valmis, jos se on analysoitu, suunniteltu, ohjelmoitu, testattu, testaus automatisoitu, dokumentoitu, integroitu muuhun ohjelmistoon ja viety tuotantoympäristöön.

## Ohjeet sovelluksen käynnistämiseen paikallisesti
Kloonaa repositorio ja luo juurihakemistoon seuraavanlainen .env tiedosto
```
DATABASE_URL=postgresql://xxx
SECRET_KEY=satunnainen_merkkijono
```
Salaisen avaimen voi luoda esimerkiksi [secrets](https://docs.python.org/3/library/secrets.html#secrets.token_hex) kirjaston avulla.

Asenna sovelluksen riippuvuudet ja siirry virtuaaliympäristöön
```
poetry install
poetry shell
```
Varmista, että PostgreSQL tietokanta on päällä. Luo tietokannan taulut ja käynnistä sovellus
```
python3 src/db_helper.py
python3 src/index.py
```
