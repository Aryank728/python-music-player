from tkinter import *
import pygame
import os
from tkinter import filedialog
from ttkthemes import themed_tk as tk
from PIL import Image, ImageTk

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Player")
        self.root.geometry("1200x600")
        pygame.init()
        pygame.mixer.init()
        self.track = StringVar()
        self.status = StringVar()
        self.album_art = None

        self.root.set_theme("breeze")  # Set the theme to "breeze"

        trackframe = Frame(self.root, bg="white")
        trackframe.place(x=10, y=10, width=780, height=100)
        
        self.album_art_label = Label(trackframe, bg="grey")
        self.album_art_label.pack(side=LEFT, padx=20)
        
        songtrack = Label(trackframe, textvariable=self.track, width=40, font=("Helvetica", 16),
                          bg="white", fg="navy")
        songtrack.pack(side=LEFT, padx=20)
        
        trackstatus = Label(trackframe, textvariable=self.status, font=("Helvetica", 16), bg="white",
                            fg="navy")
        trackstatus.pack(side=LEFT, padx=20)

        buttonframe = Frame(self.root, bg="white")
        buttonframe.place(x=5, y=150, width=780, height=80)
        
        playbtn = Button(buttonframe, text="Play", command=self.playsong, width=10, height=1,
                         font=("Helvetica", 14, "bold"), fg="white", bg="navy")
        playbtn.pack(side=LEFT, padx=20)
        
        pausebtn = Button(buttonframe, text="Pause", command=self.pausesong, width=10, height=1,
                          font=("Helvetica", 14, "bold"), fg="white", bg="navy")
        pausebtn.pack(side=LEFT, padx=20)
        
        unpausebtn = Button(buttonframe, text="Unpause", command=self.unpausesong, width=10, height=1,
                            font=("Helvetica", 14, "bold"), fg="white", bg="navy")
        unpausebtn.pack(side=LEFT, padx=20)
        
        stopbtn = Button(buttonframe, text="Stop", command=self.stopsong, width=10, height=1,
                         font=("Helvetica", 14, "bold"), fg="white", bg="navy")
        stopbtn.pack(side=LEFT, padx=20)
        
        add_button = Button(buttonframe, text="Add Song/Folder", command=self.add_song_folder,
                            font=("Helvetica", 14, "bold"),
                            fg="white", bg="navy")
        add_button.pack(side=RIGHT, padx=20)

        songsframe = Frame(self.root, bg="white")
        songsframe.place(x=10, y=220, width=780, height=150)
        
        scrol_y = Scrollbar(songsframe, orient=VERTICAL)
        self.playlist = Listbox(songsframe, yscrollcommand=scrol_y.set, selectbackground="navy", selectmode=SINGLE,
                                font=("Helvetica", 12), bg="white", fg="navy", bd=5, relief=GROOVE)
        scrol_y.pack(side=RIGHT, fill=Y)
        scrol_y.config(command=self.playlist.yview)
        self.playlist.pack(fill=BOTH)
        os.chdir("Songs")
        songtracks = os.listdir()
        for track in songtracks:
            self.playlist.insert(END, track)

    def playsong(self):
        self.track.set(self.playlist.get(ACTIVE))
        self.status.set("-Playing")
        pygame.mixer.music.load(self.playlist.get(ACTIVE))
        pygame.mixer.music.play()
        self.display_album_art()

    def stopsong(self):
        self.status.set("-Stopped")
        pygame.mixer.music.stop()
        self.clear_album_art()

    def pausesong(self):
        self.status.set("-Paused")
        pygame.mixer.music.pause()

    def unpausesong(self):
        self.status.set("-Playing")
        pygame.mixer.music.unpause()

    def add_song_folder(self):
        file_paths = filedialog.askopenfilenames(title="Select Audio Files or Folders",
                                                 filetypes=[("Audio Files", "*.mp3 *.wav")],
                                                 initialdir="./")

        for path in file_paths:
            if os.path.isdir(path):
                songtracks = [f for f in os.listdir(path) if f.endswith(".mp3") or f.endswith(".wav")]
                for track in songtracks:
                    self.playlist.insert(END, os.path.join(path, track))
            else:
                self.playlist.insert(END, path)

    def display_album_art(self):
        self.clear_album_art()
        song_path = self.playlist.get(ACTIVE)
        try:
            audio = MP3(song_path)
            tags = mutagen.File(song_path, easy=True)
            if "APIC:" in tags:
                album_art_data = tags["APIC:"].data
                img = Image.open(io.BytesIO(album_art_data))
                img = img.resize((80, 80), Image.ANTIALIAS)
                self.album_art = ImageTk.PhotoImage(img)
                self.album_art_label.config(image=self.album_art)
        except Exception as e:
            print("Error:", e)

    def clear_album_art(self):
        if self.album_art:
            self.album_art_label.config(image="")
            self.album_art = None

# Create themed TK Container
root = tk.ThemedTk()
root.get_themes()
root.set_theme("breeze")
MusicPlayer(root)
root.mainloop()
