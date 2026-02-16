# Luettelointiohjelma
Ohjelma erilaisten kokoelmien luetteloimiseen

* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään sovellukseen kokoelmia. Lisäksi käyttäjä pystyy muokkaamaan ja poistamaan lisäämiään kokoelmia.
* Käyttäjä näkee sovellukseen lisätyt kokoelmat. Käyttäjä näkee sekä itse lisäämänsä että muiden käyttäjien lisäämät kokoelmat.
* Käyttäjä pystyy etsimään esineitä kokoelmista hakusanalla tai muulla perusteella. Käyttäjä pystyy hakemaan sekä itse lisäämiään että muiden käyttäjien lisäämiä esineitä.
* Sovelluksessa on käyttäjäsivut, jotka näyttävät jokaisesta käyttäjästä tilastoja ja käyttäjän lisäämät esineet.
* Käyttäjä pystyy valitsemaan esineille/kokoelmille yhden tai useamman luokittelun. Mahdolliset luokat ovat tietokannassa.
* Sovelluksessa on pääasiallisen kokoelman lisäksi toissijainen kokoelma, joka täydentää pääasiallista kokoelmaa. Käyttäjä pystyy lisäämään toissijaisia esineitä omiin ja muiden käyttäjien kokoelmiin liittyen.

<h1>Sovelluksen asentaminen:</h1>

Luo virtuaaliympäristö sovelluksen pyörittämiseen

<code>python3 -m venv venv</code>

Käynnistä virtuaaliympäristö komennolla

<code>$ source venv/bin/activate</code>

Asenna flask -kirjasto virtuaaliympäristössä

<code>$ pip install flask</code>

Luo taulut tietokantaan komennolla

<code>$ sqlite3 database.db < schema.sql</code>

Käynnistä ohjelma komennolla ja seuraa komentotulkin ohjeita

<code>$ flask run</code>
