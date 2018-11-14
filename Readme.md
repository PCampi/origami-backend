# READ ME Progetto Origami

## 1 - Componenti gruppo

Il gruppo di lavoro risulta composto da:
- Pietro Mattia Campi, 794156
- Marta Giltri, 795267

## 2 - Obiettivi del Progetto e Background
Il progetto nasce dall'idea di una artista giapponese, appassionata di origami e famosa suonatrice di arpa. L'artista ha proposto di realizzare un'app per permettere ai bambini ricoverati negli ospedali pediatrici di Bergamo e Milano di giocare, su un tablet fornito dall'associazione, con una specie di "libro game": una storia che parte da un ben definito punto iniziale e può seguire diverse diramazioni che portano a finali diversi.

Ogni "pagina" della storia è una schermata in cui i bambini interagiscono con immagini animate di origami giapponesi, mentre la voce narrante legge il testo della storia accompagnata dall'arpa dell'artista stessa. Alcune pagine includono anche video, e tutte presentano due o più scelte che i bambini possono compiere.
Ogni bambino si registra con nome, età e genere e può giocare anche più di una volta. Alla fine di ogni storia, fatte tutte le scelte sta a lui o lei scrivere un finale.

Le storie giocate dai bambini vengono poi raccolte in un portale (che esula da questo progetto), montate in video per essere fruite da utenti esterni all'associazione.

Al fine di realizzare l'applicazione, si necessita anche un backend che eroghi le funzionalità di autenticazione, salvataggio delle storie, fornitura della traccia principale della storia (scelte, media associati a ogni scelta, scelte future). In un secondo momento, verrà anche aggiunta un'interfaccia di amministrazione per permettere agli utenti interni alla Onlus di caricare nuovi media (immagini, video, musiche e testi) e nuove storie giocabili in modo semplificato attraverso una interfaccia *drag'n drop*.

Per l'assignment si è quindi scelto di restringere lo scope e realizzare il backend con le seguenti funzionalità:

- login e autorizzazione utenti: gli utenti registrati (che nell'iterazione successiva saranno gli amministratori) possono registrarsi con username, email e password. Il sistema resituisce un token JWT [JSON Web Token](https://jwt.io) che verrà salvato nell'app per autorizzare i bambini a giocare. Dato che i tablet sono controllati dalla Onlus, non si è ritenuto necessario introdurre un processo di registrazione e autenticazione più complesso;
- upload di storie giocate: una volta giocata la storia, fatte le scelte e scritto il finale, l'app invierà i dati al backend che li salva su database, associando la storia giocata al bambino/giocatore;
- download dei media: il backend fornisce anche un download dei media tramite reindirizzamento (in previsione, file di grosse dimensioni saranno hostati su Amazon S3) oppure download diretto dal server che ospita il backend.

## 3 - Informazioni Tecniche

Per l'esecuzione di questo progetto, abbiamo fatto uso dei seguenti elementi:

1. Linguaggio: Python 3.6
    - Descrizione: Python è un linguaggio di programmazione dinamico orientato agli oggetti. Lo abbiamo scelto per la disponibilità numerosa di librerie web, per la rapidità di sviluppo e la semplicità di sintassi, e la possibilità di interfacciarsi con i più noti database open source. Abbiamo inoltre utilizzato, integrato a Python, lo static type checker Mypy: essendo Python un linguaggio a tipizzazione dinamica e necessitando di un controllo sui tipi degli oggetti più accurato in alcuni passaggi, abbiamo ritenuto opportuno impiegare Mypy.
    - Link utili: [Python Official Site](https://www.python.it/), [Mypy](http://mypy-lang.org/).

2. Framework: Falcon 1.4.1
	- Descrizione: Falcon è un Python web API framework utilizzato per poter progettare molto rapidamente backend e microservizi di applicazioni web che incoraggia l'utilizzo dello stile architetturale REST. Tramite Falcon abbiamo utilizzato il pattern MVC per la costruzione dell'applicazione. Falcon fornisce classi native per l'implementazione del pattern *Face Controller*
	- Link utili: [Falcon Framework](https://falconframework.org/).

3. Database Toolkit: SQLAlchemy 1.2.1
	- Descrizione: SQLAlchemy è un Python SQL Toolkit che consente agli sviluppatori di utilizzare la potenza e la flessibilità di SQL tramite la sua suite completa di pattern di persistenza adattati alla semplicità del linguaggio Python. Abbiamo scelto SQLAlchemy poiché particolarmente noto per il suo Object-Relational Mapper (ORM), un componente che fornisce il data mapper pattern con cui le classi possono essere mappate all'interno del database in modi differenti.
	- Link utili: [SQLAlchemy](https://www.sqlalchemy.org/).

4. Database: PostgreSQL 10.1
	- Descrizione: PostgreSQL è un potente object-relational database system sviluppato open source. Data la presenza di un'interfaccia programmativa nativa per il linguaggio Python e l'utilizzo di SQLAlchemy, la nostra scelta per il database da utilizzare è ricaduta su di questo specifico database open source.
	- Link utili: [PostgreSQL](https://www.postgresql.org/)

Il progetto è stato sviluppato utilizzando i pattern di *Face Controller* (cartella `origami/resources`), *Data Access Object* (cartella `origami/db`) e facendo uso di *Intercepting filters* (cartella `origami/middleware`) per l'autenticazione delle richieste.

## 4 - Istruzioni di installazione

I requisiti per il funzionamento del software sono Python 3.6+, Pip (package manager per Python) e PostgreSQL.

### Installazione di Python
Riferirsi al sito ufficiale [Python Official Site](https://www.python.it/), dove si trovano le versioni per Windows, Mac e Linux.

### Installazione di Pip
Una volta installato python, installare il package manager Pip dal [sito ufficiale Pip](https://pip.pypa.io/en/stable/installing/). Se si dispone di una versione di Python più recente della 3.4, Pip è automaticamente installato.

Per verificare l'installazione di Pip, aprire il terminale e digitare `pip list` che dovrebbe visualizzare l'elenco dei pacchetti installati.

### Installazione del database PostgreSQL
Installare PostgreSQL dal [sito ufficiale](https://www.postgresql.org/), e creare un database con credenziali:

- user: origami_user, deve essere un superuser
- password: origami_password
- nome database: origami_db

### Installazione di virtualenv e creazione di un ambiente virtuale

Virtualenv permette di creare una installazione separata di Python in una specifica cartella. Per installarlo, digitare nel terminale: `pip install virtualenv`

Da terminale, navigare fino alla cartella in cui risiede il progetto, entrare nella prima cartella `origami` (quella in cui sono presenti i file `requirements.txt` e `dev-requirements.txt`) e creare l'ambiente con `bash virtualenv .venv`

Per installare i pacchetti necessari all'esecuzione dei test, attivare l'ambiente virtuale con il seguente comando:
##### Su macOS/Linux:
```bash
source .venv/bin/activate
```

##### Su Windows
```bash
.venv\Scripts\activate
```

Attivato l'ambiente virtuale, installare i requisiti digitando nel terminale:

```bash
pip install -r dev-requirements.txt
```
seguito da

```bash
pip install -r requirements.txt
```

## 5 - Testing utilizzando l'IDE Visual Studio Code

Il progetto è stato sviluppato utilizzando l'IDE [Visual Studio Code](https://code.visualstudio.com/), inclusi i casi di test e il settaggio del test runner. Per questo, si consiglia di scaricare ed installare tale IDE e utilizzarla per i test.

Una volta installata l'IDE, aprirla e aggiungere la prima cartella `origami` cliccando su `Open Folder` nella barra sinistra.

Aprire dal File Explorer la cartella dei test e aprire un file di test a scelta. L'IDE capirà che quello è un file Python e proporrà la scelta dell'interprete Python per il progetto. Selezionare quello situato nella cartella `.venv`, creata in precedenza con virtualenv.

Se l'IDE non proponesse automaticamente la scelta dell'interprete Python, utilizzare la combinazione di tasti `ctrl + shift + p` e digitare `Python: Select Interpreter`. Nel menù a tendina, selezionare l'interprete.

**Assicurarsi che il database sia in esecuzione.**

Aprire la palette comandi con lo shortcut `ctrl + shift + p` e digitare `Python: Run All Unit Tests`. L'IDE proporrà di configurare un testing framework, selezionare `unittest` dal menù a tendina, poi `. root directory` nella scelta della directory e il pattern `*_test.py` per abilitare la discovery automatica dei test.

A questo punto, l'IDE lancia i test e riporta il risultato nella barra inferiore. Ci sono 26 test passati in totale.
