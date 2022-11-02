from __future__ import print_function
import configparser
from pyrad import dictionary
import logging
from db_rad import FillNases
from art import tprint

logging.basicConfig(filename="pyrad.log", level="DEBUG",
                    format="%(asctime)s [%(levelname)-8s] %(message)s")



from radserver import RadServer

if __name__ == '__main__':
    tprint("RADIUS-SERVER")
    config = configparser.ConfigParser()
    config.read("radius.ini")
    srv = RadServer(dict=dictionary.Dictionary("","dictionary","dictionary.freeradius","dictionary.mikrotik"), coa_enabled=True)
    srv.initConfig(config=config)
    FillNases(config,srv)
    srv.BindToAddress("0.0.0.0")

    # start server
    srv.Run()
