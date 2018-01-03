# Casi d'uso

## 1 - Creazione utente giocatore

1. il giocatore inserisce età, sesso e nome
2. l'app invia al backend i dati
3. il backend salva il giocatore con l'id, nome, età, sesso
4. il backend ritorna un messaggio di conferma

Il formato di scambio sarà:

```javascript
{
	"name": "Giacomino",
	"age": 9,
	"gender": "male"
}
```

## 2 - Salvataggio storia

1. il giocatore crea un utente (caso 1)
2. il giocatore gioca e crea una storia
3. il giocatore scrive il finale nell'app
4. l'app invia la storia al backend
5. il backend registra la storia e risponde con una conferma

