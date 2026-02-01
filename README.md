# Opiskelukalenteri

*Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
*Käyttäjä pystyy lisäämään, muokkaamaan ja poistamaan kalenterimerkintöjä.
*Käyttäjä näkee sovellukseen lisätyt kalenterimerkinnät.
*Käyttäjä pystyy etsimään kalenterimerkintöjä hakusanalla tai muulla perusteella.
*Käyttäjäsivu näyttää tilastoja ja käyttäjän lisäämät kalenterimerkinnät.
*Käyttäjä pystyy valitsemaan kalenterimerkinnälle yhden tai useamman luokittelun.
*Käyttäjä pystyy lisäämään kalenterimerkintään toissijaisia merkintöjä.


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

Luo projektin juureen tiedosto config.py, ja lisää oma salainen avain

```
secret_key= "oma-salainen-avain"
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
