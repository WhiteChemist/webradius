from __future__ import print_function
import configparser
from pyrad import dictionary, packet, server
from pyrad.server import ServerPacketError
import logging
import db_rad

logging.basicConfig(
    filename="pyrad.log",
    level="DEBUG",
    format="%(asctime)s [%(levelname)-8s] %(message)s",
)


class RadServer(server.Server):

    __config = configparser.ConfigParser()

    def initConfig(self, config: configparser.ConfigParser()):
        self.__config = config

    def HandleAuthPacket(self, pkt):
        try:
            for attr in pkt.keys():
                print("%s: %s" % (attr, pkt[attr]))
            if (db_rad.SearchNas(self.__config, pkt["NAS-IP-Address"], pkt["NAS-Identifier"])== True):
                if "".join(pkt["Service-Type"]) == "Login-User" :
                    info=db_rad.CheckAccessNetworkDevices(self.__config,"".join(pkt["User-Name"]))
                    UGroup=info["UGroup"]
                    if info["IsFound"]==True:    
                        reply = self.CreateReplyPacket(pkt, **{
                            "Service-Type": "Framed-User",
                            "Mikrotik-Group": f"{UGroup}"
                        })
                        reply.code=packet.AccessAccept
                        self.SendReplyPacket(pkt.fd, reply)
                        logging.info("Получен запрос на аутентификацию: Аутентификатор {}-{} . Аппликант: {}-{} Result: {}".format(
                            pkt["NAS-Identifier"],
                            pkt["NAS-IP-Address"],
                            pkt["User-Name"],
                            pkt["Calling-Station-Id"],
                            "Accept"      
                        ))
                    else:
                        reply = self.CreateReplyPacket(pkt, **{})
                        reply.code=packet.AccessReject
                        self.SendReplyPacket(pkt.fd, reply)
                        logging.info("Получен запрос на аутентификацию: Аутентификатор {}-{} . Аппликант: {}-{} Result: {}".format(
                            pkt["NAS-Identifier"],
                            pkt["NAS-IP-Address"],
                            pkt["User-Name"],
                            pkt["Calling-Station-Id"],
                            "Reject"))                              
                elif "".join(pkt["NAS-Port-Type"]) == "Wireless-802.11" and "".join(pkt["Service-Type"]) == "Framed-User":
                    if db_rad.CheckAccessWifi(self.__config,"".join(pkt["User-Name"])) == True:
                        reply = self.CreateReplyPacket(pkt, **{
                            "Framed-Pool": "dhcp_pool2"
                        })
                        reply.code=packet.AccessAccept
                        self.SendReplyPacket(pkt.fd, reply)
                elif "".join(pkt["NAS-Port-Type"]) == "Ethernet" and "".join(pkt["Service-Type"]) == "Framed-User":
                    if db_rad.CheckAccessEthernet(self.__config,"".join(pkt["User-Name"]))==True:
                        reply = self.CreateReplyPacket(pkt, **{
                            "Framed-Pool": "dhcp_pool2"
                        })
                        reply.code=packet.AccessAccept
                        self.SendReplyPacket(pkt.fd, reply)
            else:
                reply = self.CreateReplyPacket(pkt, **{})
                reply.code=packet.AccessReject
                self.SendReplyPacket(pkt.fd, reply)                        

        except ServerPacketError as spe:
            logging.error(spe)
            print(spe)

    def HandleAcctPacket(self, pkt):
        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)

    def HandleCoaPacket(self, pkt):
        reply = self.CreateReplyPacket(pkt)
        self.SendReplyPacket(pkt.fd, reply)

    def HandleDisconnectPacket(self, pkt):
        reply = self.CreateReplyPacket(pkt)
        # COA NAK
        reply.code = 45
        self.SendReplyPacket(pkt.fd, reply)
