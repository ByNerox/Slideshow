import tkinter as tk
import os
from PIL import ImageTk, Image
from pygame import mixer
from mutagen.wave import WAVE
from rename import renameImages
from win32api import GetSystemMetrics

class Slideshow(tk.Tk):
    def __init__(self):
        super().__init__()
        renameImages("img")
        self.screenWidth = GetSystemMetrics(0)
        self.screenHeight = GetSystemMetrics(1)
        self.paths = self.getMusicPaths()
        self.musicLength = self.getMusicLength()

        self.currentImage = 0
        self.imgList = []

        self.title("Slideshow")
        self.configure(background="#242628")
        self.attributes("-fullscreen", True)
        self.bind("<F4>", self.closeWindow)

        self.label = tk.Label(self, background="#242628", highlightthickness=0)
        self.label.place(relx=0.5, rely=0.5, anchor="center")

        self.imgSetup()
        self.playMusic()

        self.displayImage()
        self.timeToChange = int(self.musicLength / len(self.imgList)) * 1000
        print(self.timeToChange)
        self.after(self.timeToChange, self.nextImage)

        self.mainloop()

    def playMusic(self):
        mixer.init()
        mixer.music.load(self.paths[0])
        mixer.music.set_volume(0.2)
        mixer.music.play(0)
        mixer.music.queue(self.paths[1])
        self.after(self.musicLength * 1000, self.playMusic)


    def getMusicPaths(self):
        paths = []
        directory = os.fsencode("sound")

        for file in os.listdir(directory):
            f = os.path.join(directory, file)
            if os.path.isfile(f):
                paths.append(f)

        return paths


    def getMusicLength(self):
        length = 0
        for f in self.paths:
            audio = WAVE(f)
            audio_info = audio.info
            length += int(audio_info.length)


        return length


    def closeWindow(self, event):
        self.destroy()

    def imgSetup(self):
        directory = "img"

        for file in os.listdir(directory):
            f = os.path.join(directory, file)
            if os.path.isfile(f):
                image = Image.open(f)
                # Überprüft, ob das Bild größer als 1920x1080 ist
                if image.width > self.screenWidth or image.height > self.screenHeight:
                    # Berechne das Verhältnis für die Größenänderung
                    ratio = min(self.screenWidth / image.width, self.screenHeight / image.height)
                    # Berechnet die neuen Abmessungen
                    new_width = int(image.width * ratio)
                    new_height = int(image.height * ratio)
                    # Verkleinert das Bild
                    image = image.resize((new_width, new_height), Image.LANCZOS)
                tkimage = ImageTk.PhotoImage(image)
                self.imgList.append(tkimage)

    def displayImage(self):
        current_image = self.imgList[self.currentImage]
        self.label.config(image=current_image)
        self.label.image = current_image

    def nextImage(self):
        if self.currentImage == len(self.imgList) - 1:
            self.currentImage = 0
        else:
            self.currentImage += 1

        self.displayImage()

        self.after(self.timeToChange, self.nextImage)

Slideshow = Slideshow()