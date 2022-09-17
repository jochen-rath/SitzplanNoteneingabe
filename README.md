# SitzplanNoteneingabe
Android App zur Noteneingabe in einem Sitzplan


##Beschreibung
Diese APP ermöglicht es, einen Sitzplan zu einer Klasse zu erstellen und dann bei jedem Schüler eine Note einzutragen. Die Noten werden dann in einer CSV-Datei gespeichert, die einfach in eine Excel oder Calc Tabelle importiert werden kann.


##Voraussetzungen
Die App ist in Python geschrieben und benötigt Kivy. Installiere es mit
```
pip3 install kivy
```

##Nutzung
Auf einem Linux/Windows Computer kann die App direkt genutzt werden. Der Ziel ist es aber, die App auf einem Android Smartphone zu nutzen.

 1. Erstelle im Home-Verzeichnis den Ordner "sitzplanNoten".
 2. Die App greift auf dem Pfad "os.path.join(os.getenv('EXTERNAL_STORAGE'),'sitzplanNoten')" zu.
 3. Installiere die App auf deinem Gerät
 4. Gib der App die Berechtigung, auf den Externen-Speicher zuzugreifen. Dies wird noch nicht abgefragt.

