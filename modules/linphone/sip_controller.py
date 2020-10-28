import sys
from pexpect import spawn
import threading
import time


class SipController(threading.Thread):
    linphone = None
    linphone_cmd = ["linphonec"]

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
            self.linphone = spawn(self.linphone_cmd, encoding='utf-8', timeout=None)
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
            if line.find("is contacting you") != -1:
                print("Incoming Call")
                self.incoming_call = True
                # TODO: Start Ringer
                # self.OnIncomingCall()
            if line.find("Call terminated") != -1:
                print("Remote Hangup")
                self.call_connected = False
                self.incoming_call = False
                # self.OnRemoteHungupCall()
            if line.find("Call ended") != -1:
                print("Self Hangup")
                self.call_connected = False
                self.incoming_call = False
                # self.OnSelfHungupCall()
            if line.find("Call answered by") != -1:
                print("Call Active")
                self.call_connected = True
                self.incoming_call = False
                time.sleep(5)
                self.collect_money = True
                # self.OnSelfHungupCall()

    def SendCmd(self, cmd):
        if self.IsRunning():
            self.linphone.sendline(cmd)

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
            self.SendCmd("terminate")

    def SipAnswer(self):
        if self.IsRunning():
            # TODO: Stop Ringer
            self.SendCmd("answer")

    def is_call_connected(self):
        return self.call_connected

    def is_call_incoming(self):
        return self.incoming_call
