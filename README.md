# miniprojekti
Ohtu miniprojekti - Ryhmä: OhtuWarriors

[Backlog](https://helsinkifi-my.sharepoint.com/:x:/r/personal/toniemin_ad_helsinki_fi/_layouts/15/Doc.aspx?sourcedoc=%7B50381186-43DF-44AF-A205-691DD18D833E%7D&file=Ohtuwarriors%20backlog.xlsx&action=default&mobileredirect=true)

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
