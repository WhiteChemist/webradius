# from configparser import ConfigParser
# from pyrad.server import Server as RadServer 
# from configparser import ConfigParser
from __future__ import print_function
from pyrad import dictionary, packet, server
import logging

logging.basicConfig(
    filename="radius.log",
    level="DEBUG",
    format="%(asctime)s [%(levelname)-8s] %(message)s",
)


# class radserver(RadServer):
#     config: ConfigParser()
#     server: RadServer()

#     def __init__(self, config_path,dictionary):
#         self._config = ConfigParser().read(config_path)
#         self._server = RadServer(
#             addresses=self._config["radsettings"]["listen_addr"],
#             acctport=self._config["radsettings"]["acct_port"],
#             coaport=self._config["radsettings"]["coaport"],
#             acct_enabled=self._config["radsettings"]["acct_enabled="],
#             authport=self._config["radsettings"]["auth_port"],
#         )
#         dict=dictionary
    
#     def __init__(self, addresses=..., authport=1812, acctport=1813, coaport=3799, hosts=None, dict=None, auth_enabled=True, acct_enabled=True, coa_enabled=False):
#         super().__init__(addresses, authport, acctport, coaport, hosts, dict, auth_enabled, acct_enabled, coa_enabled)
    
#     def HandleAuthPacket(self, pkt):
#         print("Received an authentication request")
#         print("Attributes: ")
#         for attr in pkt.keys():
#             print("%s: %s" % (attr, pkt[attr]))

#         reply = self.CreateReplyPacket(pkt, **{
#         })

#         reply.code = packet.AccessAccept
#         self.SendReplyPacket(pkt.fd, reply)

#     def HandleAcctPacket(self, pkt):

#         print("Received an accounting request")
#         print("Attributes: ")
#         for attr in pkt.keys():
#             print("%s: %s" % (attr, pkt[attr]))

#         reply = self.CreateReplyPacket(pkt)
#         self.SendReplyPacket(pkt.fd, reply)

#     def HandleCoaPacket(self, pkt):

#         print("Received an coa request")
#         print("Attributes: ")
#         for attr in pkt.keys():
#             print("%s: %s" % (attr, pkt[attr]))

#         reply = self.CreateReplyPacket(pkt)
#         self.SendReplyPacket(pkt.fd, reply)

#     def HandleDisconnectPacket(self, pkt):

#         print("Received an disconnect request")
#         print("Attributes: ")
#         for attr in pkt.keys():
#             print("%s: %s" % (attr, pkt[attr]))

#         reply = self.CreateReplyPacket(pkt)
#         # COA NAK
#         reply.code = 45
#         self.SendReplyPacket(pkt.fd, reply)

# serv = radserver("./radius.ini")

class FakeServer(server.Server):

    def HandleAuthPacket(self, pkt):
        print("Received an authentication request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt, **{
            "Service-Type": "Framed-User",
            "Framed-IP-Address": '192.168.0.1',
            "Framed-IPv6-Prefix": "fc66::1/64"
        })

        reply.code = packet.AccessAccept
        self.SendReplyPacket(pkt.fd, reply)

    def HandleAcctPacket(self, pkt):

        print("Received an accounting request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)

    def HandleCoaPacket(self, pkt):

        print("Received an coa request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)

    def HandleDisconnectPacket(self, pkt):

        print("Received an disconnect request")
        print("Attributes: ")
        for attr in pkt.keys():
            print("%s: %s" % (attr, pkt[attr]))

        reply = self.CreateReplyPacket(pkt)
        # COA NAK
        reply.code = 45
        self.SendReplyPacket(pkt.fd, reply)

if __name__ == '__main__':

    # create server and read dictionary
    srv = FakeServer(dict=dictionary.Dictionary("dictionary"), coa_enabled=True)

    # add clients (address, secret, name)
    srv.hosts["10.250.0.1"] = server.RemoteHost("10.250.0.1", b"mikrotik", "home-router")
    srv.BindToAddress()

    # start server
    srv.Run()