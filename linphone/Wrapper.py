import sys
from pexpect import spawnu as spawn
import threading


class Wrapper(threading.Thread):
    linphone = None
    linphone_cmd = ["linphonec"]

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
        print("StartLinPhone: isRunning = " + str(self.IsRunning()))
        if not self.IsRunning():
            self.linphone = spawn(self.linphone_cmd, encoding='utf-8')
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
            pass
            # line = self.linphone.stdout.readline().rstrip()
            # line = self.linphone.readline()
            # print("[LINPHONE] %s" % line)
            # if line.find("is contacting you") != -1:
            #     self.OnIncomingCall()
            # if line.find("Call terminated") != -1:
            #     self.OnRemoteHungupCall()
            # if line.find("Call ended") != -1:
            #     self.OnSelfHungupCall()

    def SendCmd(self, cmd):
        print("SendCmd: isRunning = " + str(self.IsRunning()))
        if self.IsRunning():
            print("Sending Command: " + cmd)
            self.linphone.sendline(cmd)

    def SipRegister(self, username, hostname, password):
        if self.IsRunning():
            self.sip_username = username
            self.sip_hostname = hostname
            self.sip_password = password
            print("registering " + username + "...")
            self.SendCmd("register sip:%s@%s %s %s" % (username, hostname, hostname, password))
            # self.SendCmd("codec disable 4")
            # self.SendCmd("codec disable 5")

    def SipCall(self, number):
        print("SipCall: isRunning = " + str(self.IsRunning()))
        if self.IsRunning():
            print("Calling: " + str(number))
            self.SendCmd("call %s" % number)

    def SipHangup(self):
        print("SipHangup: isRunning = " + str(self.IsRunning()))
        if self.IsRunning():
            self.SendCmd("terminate")

    def SipAnswer(self):
        if self.IsRunning():
            self.SendCmd("answer")
