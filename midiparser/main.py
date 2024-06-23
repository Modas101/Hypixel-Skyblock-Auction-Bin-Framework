from MIDI import MIDIFile

Map = {
    "C": 1,
    "D": 3,
    "E": 5,
    "F": 6,
    "G": 8,
    "A": 10,
    "B": 12
}

def parse(file):
    c = MIDIFile(file)
    c.parse()
    print(str(c))
    for idx, track in enumerate(c):
        track.parse()
        print(f'---------Track {idx}:')

        for event in track.events:
            if event.__class__.__name__ == "MIDIEvent":
                if event.message.__class__.__name__ == "NoteMessage":
                    if event.message.onOff == "ON":
                        Note = event.message.note
                        NumNote = Map[Note.note[0].upper()] + Note.octave * 12

                        if len(Note.note) > 1:
                            NumNote += 1

                        print("{",f"{event.time/1000}, {NumNote}","},")


parse("midi.mid")
