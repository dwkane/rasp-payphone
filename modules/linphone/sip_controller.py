import sys
from pexpect import spawn
import threading
import time
import hardware
import tone_generator


class SipController(threading.Thread):
    linphone = None
    linphone_cmd = 'linphonec'
    linphone_cmd_args = []  # ['-c', '~/.linphonerc']

    call_connected = False
    incoming_call = False
    collect_money = False

    sip_username = None
    sip_hostname = None
    sip_password = None

    def __init__(self):
        threading.Thread.__init__(self)

    def IsRunning(self):
        try:
            return self.linphone.isalive()
        except AttributeError:
            return False

    def StartLinphone(self):
        if not self.IsRunning():
            self.linphone = spawn(self.linphone_cmd, args=self.linphone_cmd_args, encoding='utf-8', timeout=None)
            self.linphone.logfile_read = sys.stdout

    def StopLinphone(self):
        if self.IsRunning():
            self.linphone.terminate()

    def RegisterCallbacks(self, OnIncomingCall, OnOutgoingCall, OnRemoteHungupCall, OnSelfHungupCall):
        self.OnIncomingCall = OnIncomingCall
        self.OnOutgoingCall = OnOutgoingCall
        self.OnRemoteHungupCall = OnRemoteHungupCall
        self.OnSelfHungupCall = OnSelfHungupCall

    def run(self):
        while self.IsRunning():
            # line = self.linphone.stdout.readline().rstrip()
            line = self.linphone.readline()
            # print("[LINPHONE] %s" % line)
            if "Receiving new incoming call" in line:
                print("Incoming Call")
                self.incoming_call = True
                self.OnIncomingCall()
            if "Call" in line and "ended" in line:
                print("Hangup")
                self.call_connected = False
                self.incoming_call = False
                self.SipHangup()
            if "Call" in line and "connected" in line:
                print("Call Active")
                self.call_connected = True
                self.incoming_call = False
                time.sleep(5)
                self.collect_money = True

    def OnIncomingCall(self):
        if self.IsRunning():
            while self.incoming_call and not hardware.is_off_hook():
                hardware.ringer_relay.on()
                time.sleep(2)
                hardware.ringer_relay.off()
                time.sleep(4)

    def SendCmd(self, cmd):
        if self.IsRunning():
            self.linphone.sendline(str(cmd))

    def SipRegister(self, username, hostname, password):
        if self.IsRunning():
            self.sip_username = username
            self.sip_hostname = hostname
            self.sip_password = password
            self.SendCmd("register sip:%s@%s %s %s" % (username, hostname, hostname, password))
            # self.SendCmd("codec disable 4")
            # self.SendCmd("codec disable 5")

    def SipCall(self, number):
        if self.IsRunning():
            self.SendCmd("call %s" % number)

    def SipHangup(self):
        if self.IsRunning():
            if self.is_call_connected():
                self.SendCmd("terminate")
            if hardware.is_off_hook():
                time.sleep(2)
                tone_generator.play_dial_tone()

    def SipAnswer(self):
        if self.IsRunning():
            self.incoming_call = False
            self.SendCmd("answer")

    def is_call_connected(self):
        return self.call_connected

    def is_call_incoming(self):
        return self.incoming_call
