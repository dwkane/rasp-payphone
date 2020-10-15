from threading import Timer
import time
import wave


class Ringtone:
    should_ring = 0
    ringtone = None
    ring_file = None
    device = None

    ring_start = 0

    should_play_handset = 0
    handset_file = None
    timerHandset = None

    config = None

    def __init__(self, config):
        self.config = config

    def start(self):
        self.should_ring = 1
        self.ringtone = Timer(0, self.do_ring)
        self.ringtone.start()
        self.ring_start = time.time()

    def stop(self):
        self.should_ring = 0
        if self.ringtone is not None:
            self.ringtone.cancel()

    def start_handset(self, file):
        self.should_play_handset = 1
        self.handset_file = file
        if self.timerHandset is not None:
            print("[RINGTONE] Handset already playing?")
            return

        self.timerHandset = Timer(0, self.play_handset)
        self.timerHandset.start()

    def stop_handset(self):
        self.should_play_handset = 0
        if self.timerHandset is not None:
            self.timerHandset.cancel()
            self.timerHandset = None

    def play_handset(self):
        print("Starting dial tone")
        wv = wave.open(self.handset_file)
        device = alsaaudio.PCM(card="plug:external")
        # device.set_channels(wv.getnchannels())
        # device.set_rate(wv.getframerate())
        # device.set_period_size(320)

        data = wv.readframes(320)
        while data and self.should_play_handset:
            device.write(data)
            data = wv.readframes(320)
        wv.rewind()
        wv.close()

    def play_file(self, file):
        wv = wave.open(file)
        self.device = alsaaudio.PCM(card="pulse")
        self.device.setchannels(wv.getnchannels())
        self.device.setrate(wv.getframerate())
        self.device.setperiodsize(320)

        data = wv.readframes(320)
        while data:
            self.device.write(data)
            data = wv.readframes(320)
        wv.rewind()
        wv.close()

    def do_ring(self):
        if self.ring_file is not None:
            self.ring_file.rewind()
        else:
            self.ring_file = wave.open(self.config["soundfiles"]["ringtone"], 'rb')
            self.device = alsaaudio.PCM(card="pulse")
            self.device.setchannels(self.ring_file.getnchannels())
            self.device.setrate(self.ring_file.getframerate())
            self.device.setperiodsize(320)

        while self.should_ring:
            data = self.ring_file.readframes(320)
            while data:
                self.device.write(data)
                data = self.ring_file.readframes(320)

            self.ring_file.rewind()
            time.sleep(2)
            if time.time() - 60 > self.ring_start:
                self.stop()
