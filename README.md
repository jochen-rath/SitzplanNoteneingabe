# SitzplanNoteneingabe
Android App zur Noteneingabe in einem Sitzplan


## Beschreibung
Diese APP ermöglicht es, einen Sitzplan zu einer Klasse zu erstellen und dann bei jedem Schüler eine Note einzutragen. Die Noten werden dann in einer CSV-Datei gespeichert, die einfach in eine Excel oder Calc Tabelle importiert werden kann.


## Voraussetzungen
Die App ist in Python geschrieben und benötigt Kivy. Installiere es mit
```
pip3 install kivy
```

## Android App erstellen
In der Datei buildozer.spec sind die Voraussetzungen zur Erzeugung der Android App gegeben. Erzeuge die App mit dem Befehl
```
buildozer android debug
```

## Nutzung
Auf einem Linux/Windows Computer kann die App direkt genutzt werden:
```
python main.py
```
Der Ziel ist es aber, die App auf einem Android Smartphone zu nutzen.

 1. Erstelle im Home-Verzeichnis den Ordner "sitzplanNoten".
 2. Die App greift auf dem Pfad "os.path.join(os.getenv('EXTERNAL_STORAGE'),'sitzplanNoten')" zu.
 3. Installiere die App auf deinem Gerät
 4. Gib der App die Berechtigung, auf den Externen-Speicher zuzugreifen. Dies wird noch nicht abgefragt.
 5. Erstelle eine Komma getrennte Datei im Format (Vorname, Nachname). Speicher die Datei mit dem Namen Noten_Klasse.csv (siehe Noten_Test7a.csv) im Android-Ordner "sitzplan/Noten"
 6. Starte die App auf dem Smartphone
 7. Es folgt eine Übersicht aller Dateien mit dem Namensformate Noten_Klasse.csv.
 8. Wähle die gewünschte Klasse. Beim ersten Aufruf wird die Klasse in einem Gitter angeordnet dargestellt. Verschiebe die Schüler auf die gewünschte Position.
 9. Beim Speichern wird die aktuelle Position und Note in der CSV-Datei gespeichert. Außerdem wird gespeichert, wenn auf Beenden gedrückt wird.
 10. Gib für jeden Schüler eine Note von 1-6 ein oder ein nT für nicht teilgenommen. 
 11. Auswertung: Kopiere die csv Datei auf den PC. Importiere die Datei in Calc oder Excel.

