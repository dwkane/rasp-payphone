import os
import queue
import signal
import sys
# import yaml

from threading import Timer
from modules.Ringtone import Ringtone
from modules.KeypadDial import KeypadDial
from modules.linphone import Wrapper
# alternative SIP-implementation
# from modules.pjsip.SipClient import SipClient

callback_queue = queue.Queue()


class TelephoneDaemon:
    # Number to be dialed
    dial_number = ""

    # On/off hook state
    offHook = False

    # Off hook timeout
    offHookTimeoutTimer = None

    KeypadDial = None
    SipClient = None

    config = None

    def __init__(self):
        print("[START UP]")

        self.config = yaml.load(file("configuration.yml", 'r'))

        signal.signal(signal.SIGINT, self.on_signal)

        # Ring tone
        self.Ringtone = Ringtone(self.config)

        # This is to indicate boot complete. Not very realistic, but fun.
        # self.Ringtone.playfile(config["soundfiles"]["startup"])

        # Rotary dial
        self.KeypadDial = KeypadDial()
        self.KeypadDial.RegisterCallback(NumberCallback=self.got_digit, OffHookCallback=self.off_hook,
                                         OnHookCallback=self.on_hook, OnVerifyHook=self.on_verify_hook)

        self.SipClient = Wrapper.Wrapper()
        self.SipClient.StartLinphone()
        self.SipClient.SipRegister(self.config["sip"]["username"], self.config["sip"]["hostname"],
                                   self.config["sip"]["password"])
        self.SipClient.RegisterCallbacks(OnIncomingCall=self.on_incoming_call, OnOutgoingCall=self.on_outgoing_call,
                                         OnRemoteHungupCall=self.on_remote_hangup_call,
                                         OnSelfHungupCall=self.on_self_hangup_call)

        # Start SipClient thread
        self.SipClient.start()

        input("Waiting.\n")

    def on_hook(self):
        print("[PHONE] On hook")
        self.offHook = False
        self.Ringtone.stophandset()
        # Hang up calls
        if self.SipClient is not None:
            self.SipClient.SipHangup()

    def off_hook(self):
        print("[PHONE] Off hook")
        self.offHook = True
        # Reset current number when off hook
        self.dial_number = ""

        self.offHookTimeoutTimer = Timer(5, self.on_off_hook_timeout)
        self.offHookTimeoutTimer.start()

        # TODO: State for ringing, don't play tone if ringing :P
        print("Try to start dial tone")
        self.Ringtone.starthandset(self.config["soundfiles"]["dialtone"])

        self.Ringtone.stop()
        if self.SipClient is not None:
            self.SipClient.SipAnswer()

    def on_verify_hook(self, state):
        if not state:
            self.offHook = False
            self.Ringtone.stophandset()

    def on_incoming_call(self):
        print("[INCOMING]")
        self.Ringtone.start()

    def on_outgoing_call(self):
        print("[OUTGOING] ")

    def on_remote_hangup_call(self):
        print("[HANGUP] Remote disconnected the call")
        # Now we want to play busy-tone..
        self.Ringtone.starthandset(self.config["soundfiles"]["busytone"])

    def on_self_hangup_call(self):
        print("[HANGUP] Local disconnected the call")

    def on_off_hook_timeout(self):
        print("[OFF HOOK TIMEOUT]")
# TODO add Off Hook timeout sound
        # self.Ringtone.stophandset()
        # self.Ringtone.starthandset(self.config["soundfiles"]["timeout"])

    def got_digit(self, digit):
        print("[DIGIT] Got digit: %s" % digit)
        self.Ringtone.stophandset()
        self.dial_number += str(digit)
        print("[NUMBER] We have: %s" % self.dial_number)

        # Shutdown command, since our filesystem isn't read only (yet?)
        # This hopefully prevents data loss.
        # TODO: stop rebooting..
        if self.dial_number == "0666":
            self.Ringtone.playfile(self.config["soundfiles"]["shutdown"])
# TODO add GPIO pin cleanup
            os.system("halt")

        if len(self.dial_number) == 11:
            if self.offHook:
                print("[PHONE] Dialing number: %s" % self.dial_number)
                self.SipClient.SipCall(self.dial_number)
                self.dial_number = ""

    def on_signal(self, sig, frame):
        print("[SIGNAL] Shutting down on %s" % sig)
        self.KeypadDial.StopVerifyHook()
        self.SipClient.StopLinphone()
# TODO add GPIO pin cleanup
        sys.exit(0)


def main():
    t_daemon = TelephoneDaemon()


if __name__ == "__main__":
    main()
