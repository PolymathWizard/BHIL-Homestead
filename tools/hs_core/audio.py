"""WAV and Standard MIDI File writers.

HOMESTEAD renders click-to-play tracks from note lists: a square-wave WAV
that every browser can play, plus a .mid file that sits in View Source the
way background MIDI did. Tunes are public-domain compositions sequenced
fresh, or originals (ADR-004).
"""

import struct

NOTE_NAMES = {"C": 0, "C#": 1, "D": 2, "D#": 3, "E": 4, "F": 5, "F#": 6, "G": 7, "G#": 8, "A": 9, "A#": 10, "B": 11}


def note_number(name):
    """Convert names like C4, F#5, or R (rest) to a MIDI note number or None."""
    if name.upper() == "R":
        return None
    pitch, octave = name[:-1], int(name[-1])
    return 12 * (octave + 1) + NOTE_NAMES[pitch.upper()]


def frequency(midi_note):
    return 440.0 * (2.0 ** ((midi_note - 69) / 12.0))


def render_wav(notes, bpm=120, rate=8000, volume=0.28, duty=0.5):
    """notes is a list of (name, beats). Returns 8-bit mono WAV bytes."""
    beat_seconds = 60.0 / bpm
    samples = bytearray()
    for name, beats in notes:
        count = int(round(beats * beat_seconds * rate))
        midi = note_number(name)
        if midi is None:
            samples += bytes([128]) * count
            continue
        period = rate / frequency(midi)
        attack = max(1, int(rate * 0.01))
        release = max(1, int(rate * 0.04))
        for i in range(count):
            phase = (i % period) / period
            wave = 1.0 if phase < duty else -1.0
            env = 1.0
            if i < attack:
                env = i / attack
            elif i > count - release:
                env = max(0.0, (count - i) / release)
            value = int(round(128 + 127 * volume * env * wave))
            samples.append(max(0, min(255, value)))
    header = b"RIFF" + struct.pack("<I", 36 + len(samples)) + b"WAVE"
    fmt = b"fmt " + struct.pack("<IHHIIHH", 16, 1, 1, rate, rate, 1, 8)
    data = b"data" + struct.pack("<I", len(samples)) + bytes(samples)
    return header + fmt + data


def _varlen(value):
    out = [value & 0x7F]
    value >>= 7
    while value:
        out.insert(0, (value & 0x7F) | 0x80)
        value >>= 7
    return bytes(out)


def render_midi(notes, bpm=120, program=80, ticks=96):
    """Write a format 0 Standard MIDI File. Program 80 is a square lead."""
    track = bytearray()
    tempo = int(round(60000000 / bpm))
    track += b"\x00\xFF\x51\x03" + struct.pack(">I", tempo)[1:]
    track += b"\x00\xC0" + bytes([program & 0x7F])
    pending_rest = 0
    for name, beats in notes:
        length = int(round(beats * ticks))
        midi = note_number(name)
        if midi is None:
            pending_rest += length
            continue
        track += _varlen(pending_rest) + bytes([0x90, midi, 96])
        track += _varlen(length) + bytes([0x80, midi, 0])
        pending_rest = 0
    track += _varlen(pending_rest) + b"\xFF\x2F\x00"
    header = b"MThd" + struct.pack(">IHHH", 6, 0, 1, ticks)
    return header + b"MTrk" + struct.pack(">I", len(track)) + bytes(track)


def duration_seconds(notes, bpm=120):
    return sum(beats for _n, beats in notes) * 60.0 / bpm


def silence_check(wav_bytes):
    """Return peak deviation from midpoint; used by tests."""
    data = wav_bytes[44:]
    return max(abs(b - 128) for b in data) if data else 0

