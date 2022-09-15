import random

from kivy.properties import  ObjectProperty
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.core.window import Window
from kivy.utils import platform
import csv
import datetime
import os


class NotenDropDown(BoxLayout):
    pass

class MultiButton(Button):
    pass
class MenuButton(Button):
    pass


class NamenUndNotenInBox(BoxLayout):
    def aenderName(self,name):
        self.ids.namensLabel.ids.labelVorname.text = name[1]
        self.ids.namensLabel.ids.labelNachname.text = name[0]
    def setzePosition(self,pos):
        self.pos = pos
    def setzeNote(self,note):
        self.ids.notenAuswahl.ids.btn.text=note
    def getPosition(self):
        return self.pos
    def getNamen(self):
        return [self.ids.namensLabel.ids.labelNachname.text,self.ids.namensLabel.ids.labelVorname.text]
    def getNote(self):
        return self.ids.notenAuswahl.ids.btn.text
    pass

class LabelTouch(BoxLayout):
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            touch.grab(self) # Grab touch for move and up
            return True
        return super(LabelTouch,self).on_touch_down(touch) # pass touch to the parent class
    def on_touch_move(self, touch):
        if touch.grab_current is self:
            self.parent.center = touch.pos
            return True
        return super(LabelTouch,self).on_touch_move(touch)
    def on_touch_up(self, touch):
        if touch.grab_current is self:
            touch.ungrab(self)
            return True
        return super(LabelTouch,self).on_touch_up(touch)

class Pult(Widget):
    def aenderName(self,name):
        self.ids.pultLabel.ids.labelVorname.text = name[0]
        self.ids.pultLabel.ids.labelNachname.text = name[1]
    def setzePosition(self,pos):
        self.pos = pos
    def getPosition(self):
        return self.pos
    pass



class Sitzplan(Widget):
    schuelerDaten = []
    schuelerWidget=[]
    tage=[]
    klasse=''
    p=[]
    sitze=[]
    altePos=[]
#Diese Klasse erzeugt eine Sitzplan, in dem die Noten eingegeben werden können.
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.schuelerDaten = []
        self.schuelerWidget=[]
        self.tage=[]
        self.klasse=''
        app=App.get_running_app()
        root=FloatLayout()
        self.sitze=[]
        self.leseConfigDatei()
        for schueler in self.schuelerDaten:
            self.sitze.append(NamenUndNotenInBox())
            self.sitze[-1].aenderName(schueler[0:2])
            self.sitze[-1].setzePosition(schueler[2:4])
            self.altePos.append(list(schueler[2:4]))
            if len(self.tage)>0:
                if self.tage[-1]==datetime.date.today().strftime("%Y.%m.%d"):
                    self.sitze[-1].setzeNote(schueler[-1])
            root.add_widget(self.sitze[-1])
        self.p=Pult()
        self.p.aenderName(['Pult',self.klasse[1]])
        self.p.setzePosition(self.klasse[2:])
        root.add_widget(self.p)
        save=MultiButton(text='Speichern')
        save.bind(on_press=lambda  x:self.speicherNoten(self.sitze))
        save.pos=[app.breite-save.size[0],0]
        root.add_widget(save)
        exit=MultiButton(text='Beenden',pos=[0,0])
        exit.bind(on_press=lambda  x:self.speicherNoten(self.sitze,ende=True))
        root.add_widget(exit)
        zufall=MultiButton(text='Zufall')
        zufall.bind(on_press=lambda  x:self.zufallSitzplan())
        zufall.pos=[app.breite-save.size[0]-zufall.size[0],0]
        root.add_widget(zufall)
        alleNT=MultiButton(text='Alles:')
        alleNT.bind(on_press=lambda  x:self.allesNT())
        alleNT.size[1]=app.schriftgroesse*2
        alleNT.pos=[0,app.hoehe-alleNT.size[1]]
        root.add_widget(alleNT)
        dropDown=NotenDropDown()
        dropDown.pos=[alleNT.size[0],app.hoehe-alleNT.size[1]]
        root.add_widget(dropDown)
        self.ids['AlleNoten']=dropDown
        rueckgaengig=MultiButton(text='Auf Anfang')
        rueckgaengig.bind(on_press=lambda  x:self.rueckgaengig())
        rueckgaengig.pos=[exit.size[0],0]
        root.add_widget(rueckgaengig)
        self.add_widget(root)
    def allesNT(self):
        for sitz in self.sitze:
            sitz.setzeNote(self.ids.AlleNoten.ids.btn.text)
    def zufallSitzplan(self):
        positionen=[list(x.getPosition()) for x in self.sitze]
        random.shuffle(positionen)
        for i,pos in enumerate(positionen):
            self.sitze[i].setzePosition(pos)
    def rueckgaengig(self):
        for i,pos in enumerate(self.altePos):
            self.sitze[i].setzePosition(pos)
    def leseConfigDatei(self):
        app = App.get_running_app()
        schuelerNamenPos = []
        with open(app.configDatei) as csvfile:
            #Format:  Nachname,Vorname,Posx,Poxy,Note1,Note2
            #    Klasse,Ph8e,122,0,2021.12.24,2021.12.25,...
            #    Mustermann,Max,0,234,1,6,...
            #    Musterfrau,Märthe,240,234,3,2,...
            s = csv.reader(csvfile, delimiter=',')
            klasseInDatei=False
            for i, l in enumerate(s):
                if l[0]=='Klasse':
                    klasseInDatei=True
                    if len(l) < 4:
                    # Es existiert keine Position, gib sie an
                        l = l + [int(app.breite/ 2),app.schriftgroesse]
                    self.klasse=l[0:4]
                    if len(l)>4:
                        self.tage=l[4:]
                else:
                    # Existiert keine Position, verteile die Schueler in einem Raster auf dem Bildschirm.
                    # Berechne deren Position mit dem modulo.
                    if len(l) < 4:
                        l = l + [int(app.breite * (i % 5) / 5),
                             (app.hoehe - app.schriftgroesse * 10) * int(i / 5) / 5 + app.schriftgroesse * 5]
                    #Eventuell wurde ein neuer Schüler eingepflegt. Dann müssen seine Tage mit nicht erteilt
                    #aufgefüllt werden.
                    if not (len(l[4:])==len(self.tage)):
                        l=l+['nT']*len(self.tage)
                    self.schuelerDaten.append(l)
            if not klasseInDatei:
                self.klasse = ['Klasse',(app.configDatei.split('_')[1]).split('.')[0],int(app.breite/ 2),app.schriftgroesse]
        return schuelerNamenPos
    def speicherNoten(self,sitze,ende=False):
        # Erstelle für jeden Schüler einen Datensatz der Form
        # daten=['nachname','vorname','mHa-pTr','mAschr-mTr',...] usw.
        app = App.get_running_app()
        heute=datetime.date.today().strftime("%Y.%m.%d")
        if len(self.tage)==0 or not self.tage[-1]==heute:
            self.tage.append(heute)
            for i,schueler in enumerate(self.schuelerDaten):
                self.schuelerDaten[i][2:4]=sitze[i].getPosition()
                self.schuelerDaten[i].append(sitze[i].getNote())
        else:
            for i,schueler in enumerate(self.schuelerDaten):
                self.schuelerDaten[i][2:4]=sitze[i].getPosition()
                self.schuelerDaten[i][-1]=sitze[i].getNote()
        self.schreibeConfigDatei()
        if ende:
            app.entferneSitzplanLadeMenu()
    def schreibeConfigDatei(self):
        app=App.get_running_app()
        with open(app.configDatei, mode='w') as csvfile:
            file = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            self.klasse[2:4]=self.p.getPosition()
            file.writerow(self.klasse+self.tage)
            for daten in self.schuelerDaten:
                file.writerow(daten)

class StelleMenueDar(Widget):
    def __init__(self):
        super().__init__()
        root=BoxLayout()
        root.orientation='vertical'
        app=App.get_running_app()
        l=Label(text='Übersicht',font_size=app.schriftgroesse,size_hint=[None,None],size=[app.breite, 2*app.schriftgroesse])
        root.add_widget(l)
        g=GridLayout(rows= 3,cols= 6,padding= 20,spacing= 20)
        bten=[]
        for i,file in enumerate(app.configDateien):
            klasse=(file.split('_')[1]).split('.')[0]
            bten.append(MenuButton(text=klasse))
            g.add_widget(bten[-1])
        root.add_widget(g)
        root.pos=[0,app.hoehe-self.size[1]]
        self.add_widget(root)
        exit=MultiButton(text='Exit')
        exit.pos=[0,0]
        exit.bind(on_press=lambda  x:app.stop())
        self.add_widget(exit)
        infobox=BoxLayout(orientation='vertical')
        if os.path.isfile(os.path.join(app.grundpfad,app.infodatei)):
            with open(os.path.join(app.grundpfad,app.infodatei)) as csvfile:
                s = csv.reader(csvfile, delimiter=',')
                for zeile in s:
                    if len(zeile)>1:
                        infobox.add_widget(Label(text=zeile[0]+': '+' '.join(zeile[1:]),font_size=app.schriftgroesse))
                    else:
                        infobox.add_widget(
                            Label(text=str(zeile), font_size=app.schriftgroesse))
        infobox.pos=[0,exit.size[1]]
        infobox.center_x=app.breite/2
        self.add_widget(infobox)


class MainApp(App):
    breite=Window.size[0]
    hoehe=Window.size[1]
#Bei 800 Pixel, Schriftgröße 20, bei 2248 Pixel Schriftgröße 35. Dazwischen lineare interpolieren
    schriftgroesse=int((40-20)/(2248-800)*(breite-800)+20)
    grundpfad='.' if platform != 'android' else os.path.join(os.getenv('EXTERNAL_STORAGE'),'sitzplanNoten')
    if not os.path.exists(grundpfad):
        os.mkdir(grundpfad)
    configDatei=''
    configDateien=[x for x in os.listdir(grundpfad) if x.startswith('Noten_')]
    infodatei='infoDateiListeAusrutcher.csv'
    aktuell=None
    root=None
    def entferneSitzplanLadeMenu(self):
        self.root.remove_widget(self.aktuell)
        self.aktuell=StelleMenueDar()
        self.root.add_widget(self.aktuell)
    def entferneMenuLadeSitzplan(self,klasse):
        self.configDatei=os.path.join(self.grundpfad,[x for x in self.configDateien if (x.split('_')[1]).split('.')[0]==klasse][0],)
        self.root.remove_widget(self.aktuell)
        self.aktuell=Sitzplan()
        self.root.add_widget(self.aktuell)
    def build(self):
        self.configDatei=self.configDateien[0]
        self.root=BoxLayout()
        self.aktuell=StelleMenueDar()
        self.root.add_widget(self.aktuell)
        return self.root

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    MainApp().run()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
