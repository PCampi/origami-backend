# Definizione degli URL e delle collezioni

## Utenti

Azioni:

- aggiungere nuovo admin
- aggiungere nuovo giocatore

Vanno separati in due:

## Utenti giocatori

Attributi:

```javascript
player = {
	id: int, autoincrement, server
	name: String
	age: int > 0
}
```

### Azioni:

- aggiungi nuovo: POST a `/vN/players`
- recupera lista giocatori: GET a `/vN/players`
- recupera dati di un giocatore: GET a `/vN/players/<id:int>`

## Utenti admin

Attributi:

```javascript
admin = {
	id: int, autoincrement, server
	email: String
	password: String (how to save?)
}
```

### Azioni:

**Tutte richiedono autenticazione come admin**

- aggiungi nuovo: POST a `/vN/admin_users`
- ritorna lista amministratori: GET a `vN/admin_users`
- recupera dati di un amministratore: GET a `/vN/admin_users/<id:int>`
- modifica dati di un amministatore: PUT a `/vN/admin_users/<id:int>`
- cancella amministratore: DELETE a `/vN/admin_users/<id:int>`

## Storie possibili

Attributi:

```javascript
story = {
	root: StoryNode
}

StoryNode = {
	node_id: int, server
	resources: [Resource]
	children: [StoryNode]
	final_text: String
}

Resource = {
	id: int, server
	type: String in (audio, video, image)
	url: url dove si trova il media contenuto nella risorsa
}
```

### Azioni

Le storie possibili vengono aggiornate solo da utenti admin. Le azioni sono:

- crea nuova storia: POST a `/vN/playable_stories`
- ottieni storia: GET a `/vN/playable_stories/<story_id:int>` *ce n'è sempre e solo una?*
- ottieni tutte le storie: GET a `/vN/playable_stories`
- modifica storia: PUT a `/vN/playable_stories/<story_id:int>`

## Storie giocate

Attributi:

```javascript
playedStory = {
	id: int, server
	player_id: int
	choices: [node_id] list of int
}
```

### Azioni

- crea nuova storia a fine gioco: POST a `/vN/played_stories`
- ottieni lista di storie giocate: GET a `/vN/played_stories`
- ottieni dettagli di una storia: GET a `/vN/played_stories/<story_id:int>`

## Media: immagini, audio, video

Questi endpoint identificano una risorsa media che l'app o il client può scaricare.

La root è `/vN/media`, coi sottopercorsi

- `/vN/media/images` per le immagini
- `/vN/media/audios` per gli audio
- `/vN/media/videos` per i video

Ognuno di questi endpoint supporta le seguenti azioni.

### Azioni

Visto che i media possono essere salvati ovunque, usiamo il formato di risorsa generica `Resource` già definito

```javascript
resource = {
	id: int
	type: String in (image, audio, video)
	url: url dove trovare il media
}
```

Il generico endpoint è `/vN/media/type/`

- aggiungi nuovo media: POST a `/vN/media/type`
- ritorna il contenuto di un media: GET a `/vN/media/type/<media_id:int>`
- ritorna la lista dei media disponibili: GET a `/vN/media/type`
- modifica un media: PUT a `/vN/media/type/<media_id:int>`