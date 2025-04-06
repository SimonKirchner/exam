# Abandoned Space Station

Ein konsolenbasiertes Abenteuerspiel, bei dem Spieler eine gefährliche, verlassene Raumstation vorsichtig scannen und erkunden müssen. Deine Mission ist es, alle sicheren Bereiche zu identifizieren, ohne dabei Gefahrenherde auszulösen.

## Spielbeschreibung

In "Abandoned Space Station" spielst du einen Entdecker, der eine verlassene Raumstation untersucht. Die Station enthält zahlreiche Gefahren, die vermieden werden müssen. Dein Ziel ist es, erfolgreich alle sicheren Bereiche zu scannen, um die Station zu sichern. Dabei musst du logisch denken und Rückschlüsse ziehen, um herauszufinden, wo sich die Gefahren befinden.

Die Spielmechanik ist von Minesweeper inspiriert:
- Jeder sichere Bereich zeigt die Anzahl der angrenzenden Gefahren an
- Du musst anhand dieser Zahlen ableiten, wo sich Gefahren befinden
- Scanne alle sicheren Bereiche, um zu gewinnen, aber löse eine einzige Gefahr aus, und das Spiel ist vorbei!

## Installation

1. Repository klonen:
   ```
   git clone <repository-url>
   cd abandoned-space-station
   ```

2. Abhängigkeiten installieren:
   ```
   pip install -r requirements.txt
   ```

## Spielanleitung

Starte das Spiel:
```
python source/main.py
```

### Spielregeln

- Das Spiel präsentiert ein Raster, das die Bereiche der Raumstation darstellt
- Gib Koordinaten im Format "x y" ein, um einen Bereich zu scannen
- Wenn du einen sicheren Bereich scannst, wird die Anzahl der Gefahren in angrenzenden Bereichen angezeigt
- Wenn du eine Gefahr scannst, endet das Spiel
- Scanne alle sicheren Bereiche, um die Mission abzuschließen

### Steuerung

- Gib Koordinaten im Format "x y" ein (z.B. "2 3")
- Gib "q" ein, um das Spiel zu beenden

## Anpassung

Du kannst das Spiel mit verschiedenen Rastergrößen und Gefahrenzahlen anpassen:
- Rasterbreite (mindestens 5)
- Rasterhöhe (mindestens 5)
- Anzahl der Gefahren (mindestens 1)

## Entwicklung

### Projektstruktur

```
abandoned-space-station/
├── __init__.py
├── requirements.txt
├── mypy.ini
├── .pylintrc
├── source/
│   ├── __init__.py
│   ├── game.py
│   ├── helpers.py
│   └── main.py
└── tests/
    ├── __init__.py
    ├── test_game.py
    ├── test_helpers.py
    └── test_main.py
```

### Codequalität

Das Projekt verwendet folgende Werkzeuge zur Qualitätssicherung:
- Pylint für Code-Linting
- Mypy für statische Typprüfung
- Coverage für Testabdeckungsanalyse

Qualitätsprüfungen ausführen:
```
pylint exam/
mypy exam/
```

### Tests

Tests ausführen:
```
python -m unittest discover
```

Mit Coverage ausführen:
```
coverage run -m unittest discover
coverage report
```

## Funktionen

- Zufällig generierte Gefahrenpositionen für hohen Wiederspielwert
- Dynamisches Spielraster mit konfigurierbaren Dimensionen
- System zur Zählung angrenzender Gefahren
- Statistik-Tracking (Abschlussprozentwert, durchgeführte Aktionen)
- Plattformübergreifende Terminal-Unterstützung

## Anforderungen

- Python 3.9 oder höher
- Abhängigkeiten in requirements.txt aufgelistet

## Mitwirken

Beiträge sind willkommen! Bitte reiche gerne einen Pull Request ein.

1. Forke das Repository
2. Erstelle deinen Feature-Branch (`git checkout -b feature/TollesFunktion`)
3. Committe deine Änderungen (`git commit -m 'Tolle Funktion hinzugefügt'`)
4. Pushe zum Branch (`git push origin feature/TollesFunktion`)
5. Eröffne einen Pull Request

## Lizenz

Dieses Projekt ist Open Source.