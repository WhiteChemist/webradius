from genericpath import isfile
import psycopg2
import configparser
from radserver import RadServer
from pyrad.server import RemoteHost
import logging

logging.basicConfig(
    filename="pyrad.log",
    level="DEBUG",
    format="%(asctime)s [%(levelname)-8s] %(message)s",
)


def SearchNas(config: configparser.ConfigParser(), nas_ip: str, nas_name: str):
    try:
        IsFound = False
        convert_ip = "".join(nas_ip)
        convert_name = "".join(nas_name)
        sql = "SELECT * FROM website_nas WHERE ip_address='{}' AND short_name='{}'".format(
            convert_ip, convert_name
        )
        connection = psycopg2.connect(
            database=config["database"]["dbname"],
            user=config["database"]["username"],
            password=config["database"]["password"],
            host=config["database"]["host"],
            port=config["database"]["port"],
        )
        initer = connection.cursor()
        initer.execute(sql)
        initer.close()
        if initer.rowcount == 0:
            raise Exception("Не найдено такого NAS")
            return IsFound
        elif initer.rowcount >= 1:
            IsFound = True
            return IsFound
    except psycopg2.Error as error:
        logging.error(error)
        print(error)
    except Exception as ex:
        logging.error(ex)
        print(ex)


def FillNases(config: configparser.ConfigParser(), server: RadServer):
    try:
        sql = 'SELECT ip_address, short_name, secret_key FROM "website_nas"'
        connection = psycopg2.connect(
            database=config["database"]["dbname"],
            user=config["database"]["username"],
            password=config["database"]["password"],
            host=config["database"]["host"],
            port=config["database"]["port"],
        )
        initer = connection.cursor()
        initer.execute(sql)
        if initer.rowcount == 0:
            logging.warning("Не найдено сетевых устройств в базе данных!")
        for row in initer:
            server.hosts[row[0]] = RemoteHost(
                row[0], bytes(row[2], encoding="utf=8"), row[1]
            )
        initer.close()
    except psycopg2.Error as error:
        logging.error(error)
        print(error)
    except Exception as ex:
        logging.error(ex)
        print(ex)


def CheckAccessNetworkDevices(
    config: configparser.ConfigParser(), login: str
) -> dict[bool, str]:
    IsFound = False
    IsGroup = "none"

    try:
        IsFound = False
        sql = "SELECT wland.type_level_access FROM public.website_users as wu INNER JOIN public.website_user_groups as ug ON ug.id_user_group = wu.id_user_group_id INNER JOIN public.website_level_access_network_devices as wland ON ug.id_level_access_network_devices_id=wland.id_level_access_network_devices AND wu.network_login='{}';".format(
            login
        )
        connection = psycopg2.connect(
            database=config["database"]["dbname"],
            user=config["database"]["username"],
            password=config["database"]["password"],
            host=config["database"]["host"],
            port=config["database"]["port"],
        )
        initer = connection.cursor()
        initer.execute(sql)
        if initer.rowcount == 0:
            IsFound = False
            UGroup = "none"
            return {"IsFound": IsFound, "UGroup": UGroup}
        else:
            for item in initer:
                IsFound = True
                UGroup = item[0]
            return {"IsFound": IsFound, "UGroup": UGroup}

        initer.close()
    except psycopg2.Error as error:
        logging.error(error)
        print(error)
    except Exception as ex:
        logging.error(ex)
        print(ex)


def CheckAccessWifi(config: configparser.ConfigParser(), wifi_mac: str):
    try:
        IsFound = False
        sql = """SELECT wlan.type_level_access 
                 FROM public.website_users as wu 
                INNER JOIN public.website_user_groups as ug 
                ON ug.id_user_group = wu.id_user_group_id 
                INNER JOIN public.website_level_access_network as wlan 
                ON ug.id_level_access_network_id=wlan.id_level_access_network 
                INNER JOIN public.website_mac_addresses as wma
                ON wu.id_mac_id=wma.id_user_mac AND (wma.mac_address_eth='{}' 
                OR wma.mac_address_wifi='{}' 
                OR wma.mac_address_add_1='{}'
                OR wma.mac_address_add_2='{}')""".format(
            wifi_mac, wifi_mac, wifi_mac, wifi_mac
        )
        connection = psycopg2.connect(
            database=config["database"]["dbname"],
            user=config["database"]["username"],
            password=config["database"]["password"],
            host=config["database"]["host"],
            port=config["database"]["port"],
        )
        initer = connection.cursor()
        initer.execute(sql)
        for item in initer:
            if item[0] == "All" or item[0] == "Only Wireless":
                IsFound = True
                return IsFound
            else:
                return IsFound
        initer.close()
    except psycopg2.Error as error:
        logging.error(error)
        print(error)
    except Exception as ex:
        logging.error(ex)
        print(ex)


def CheckAccessEthernet(config: configparser.ConfigParser(), ethernet_mac: str):
    try:
        IsFound = False
        sql = """SELECT wlan.type_level_access 
                 FROM public.website_users as wu 
                INNER JOIN public.website_user_groups as ug 
                ON ug.id_user_group = wu.id_user_group_id 
                INNER JOIN public.website_level_access_network as wlan 
                ON ug.id_level_access_network_id=wlan.id_level_access_network 
                INNER JOIN public.website_mac_addresses as wma
                ON wu.id_mac_id=wma.id_user_mac AND (wma.mac_address_eth='{}' 
                OR wma.mac_address_wifi='{}' 
                OR wma.mac_address_add_1='{}'
                OR wma.mac_address_add_2='{}')""".format(
            ethernet_mac, ethernet_mac, ethernet_mac, ethernet_mac
        )
        connection = psycopg2.connect(
            database=config["database"]["dbname"],
            user=config["database"]["username"],
            password=config["database"]["password"],
            host=config["database"]["host"],
            port=config["database"]["port"],
        )
        initer = connection.cursor()
        initer.execute(sql)
        for item in initer:
            if item[0] == "All" or item[0] == "Only Ethernet":
                IsFound = True
                return IsFound
            else:
                return IsFound
        initer.close()
    except psycopg2.Error as error:
        logging.error(error)
        print(error)
    except Exception as ex:
        logging.error(ex)
        print(ex)


def CreateAcct(
    config: configparser.ConfigParser(),
    service_type: str,
    nas_port_type: str,
    username: str,
    acct_session_id: str,
    calling_station_id: str,
    called_station_id: str,
    acct_authentic: str,
    acct_status_type: str,
    nas_identifier: str,
    acct_delay_time: str,
):
    try:
        sql = """INSERT INTO public.website_accounting(
	             id_user_name_id, acct_authentic, acct_delay_time, acct_session_id, acct_status_type, called_station_id, calling_station_id, dateinfo, id_nas_identifier_id, id_nas_port_type_id, service_type)
	             VALUES ((SELECT id_users FROM public.website_users as wu INNER JOIN website_mac_addresses as wma ON wu.id_mac_id=wma.id_user_mac AND (wma.mac_address_eth='{}' OR wma.mac_address_wifi='{}' OR wma.mac_address_add_1='{}' OR wma.mac_address_add_2='{}') ), 
                '{}', 
                '{}', 
                '{}', 
                '{}',
                '{}',
                '{}', 
                (SELECT now()),
                (SELECT id_nas FROM public.website_nas WHERE short_name='{}'),
                (SELECT id_nas_port_type FROM public.website_nas_port_type WHERE port_type='{}'),
                '{}');""".format(username,username,username,username,acct_authentic,acct_delay_time,acct_session_id,acct_status_type,called_station_id,calling_station_id,nas_identifier,nas_port_type,service_type)
        connection = psycopg2.connect(
            database=config["database"]["dbname"],
            user=config["database"]["username"],
            password=config["database"]["password"],
            host=config["database"]["host"],
            port=config["database"]["port"],
        )
        initer = connection.cursor()
        initer.execute(sql)
        connection.commit()
        count = initer.rowcount
        print(count,"Record inserted successfully into table")
    except psycopg2.Error as error:
        logging.error(error)
        print(error)
    except Exception as ex:
        logging.error(ex)
        print(ex)
    finally:
        # closing database connection.
        if connection:
            initer.close()
            connection.close()
            logging.info("Postgres was closed connection")
