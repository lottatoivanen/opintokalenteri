# Opiskelukalenteri

Tämä sovellus on web pohjainen kalenterisovellus, jossa käyttäjä pystyy helpommin hallita omien opintojen aikataulutusta.

## Sovelluksen ominaisuudet

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.

* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan kalenterimerkintöjä.

* Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan kursseja.

* Käyttäjä näkee sovellukseen lisätyt kalenterimerkinnät sekä kurssit.

* Käyttäjä pystyy etsimään kalenterimerkintöjä hakusanalla.

* Käyttäjä näkee käyttäjäsivuilta lisätyt kalenterimerkinnät sekä tilastoja.

* Käyttäjä pystyy valitsemaan kalenterimerkinnälle yhden tai useamman luokittelun (esim. "tentti" tai "harjoitustyö").

* Käyttäjä pystyy lisäämään kalenterimerkintään toissijaisia merkintöjä (esim. merkinnän ajankohdan tai siihen liittyvän kurssin).


## Asennus- ja käyttöohjeet

Kloonaa repositorio tietokoneellesi komennolla

```
git clone git@github.com:lottatoivanen/opintokalenteri.git
```

Tämän jälkeen siirry hakemistoon

```
cd opintokalenteri
```

Kun olet hakemiston sisällä, luo tietokanta ja taulut

```
sqlite3 database.db < schema.sql
```
```
sqlite3 database.db < init.sql
```

Luo projektin juureen tiedosto config.py, ja lisää oma salainen avain

```
secret_key = "oma-salainen-avain"
```

Luo hakemistoon Pythonin virtuaaliympäristö

```
python3 -m venv venv
```

Aktivoi virtuaaliympäristo

```
source venv/bin/activate
```

Kun olet virtuaaliympäristössä, asenna flask kirjasto

```
pip install flask
```

Käynnistä sovellus komennolla

```
flask run
```

## Pylint raportti

Koodin palautteeseen käytettiin Pylint työkalua, joka suoritettiin tiedostoihin app.py, db.py, comments.py, user.py, entries.py ja courses.py.

Pylint antoi koodille arvosanaksi 8.65/10. Korjaamattomat palautteet jätettiin loogisuuden ja koodin helppouden takia.

Lisätietoja raporttiin liittyen löytyy tiedostosta pylint_report.txt.
