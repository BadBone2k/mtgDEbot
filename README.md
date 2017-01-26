# mtgDEbot

Telegram Bot, der Magickarten von http://magiccards.info inline sucht und verschickt.

## Voraussetzung
### mindestens Python 3.5 mit folgenden Paketen:
  * telepot
  * requests
  * beautifulsoup4

### Bot bei Telegram registrieren
Der Bot muss bei Telegram (@BotFather) registriert werden, um einen API-Token zu erhalten. Außerdem müssen hier /setinline und /setinlinefeedback für den Bot gesetzt werden.

## Ausführung

```
$ python3.5 mtgDEbot.py <token>
```

mtgDEbot.sh zeigt exemplarisch, wie der Bot auf https://uberspace.de/ gestartet werden kann.

## Verwendung

Verwendung des Bots inline in einem Chat:

```
@mtgDEbot <Kartenname> [("." | "," | "/" | "|") <Edition>]
```

Die Suche wurde auf deutsche Karten eingeschränkt.
So lange nichts eingegeben wurde, wird eine zufällige Karte angezeigt.


Die Angabe der Edition ist optional, es gibt verschiedene Trenner,
hinter dem Trenner kann ein Leerzeichen sein, muss aber nicht.

## Credits

Der ganze Code basiert auf Beispielen und Tutorials,
die hier zu finden sind: https://github.com/nickoala/telepot
