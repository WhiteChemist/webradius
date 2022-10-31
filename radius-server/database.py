import psycopg2
import configparser

def SearchNas(config: configparser.ConfigParser(),nas_ip: str,nas_name: str):
    sql = "SELECT FROM public.nas WHERE ip_address={} AND short_name={}".format(nas_ip,nas_name)
    connection = psycopg2.connect(
        database=config["database"]["dbname"],
        user=config["database"]["username"],
        password=config["database"]["password"],
        host=config["database"]["host"],
        port=config["database"]["port"],
    )
    initer = connection.cursor()
    initer.fetchone()
    initer.close()

def fillNases():
    try:
        config = configparser.ConfigParser()
        config.read('radius.ini')
        sql = 'SELECT * FROM public.nas;'
        connection = psycopg2.connect(
            database=config['database']['dbname'],
            user=config['database']['username'],
            password=config['database']['password'],
            host=config['database']['host'],
            port=config['database']['port'],
        )
        initer = connection.cursor()
        result = initer.fetchall()
        initer.close()
        return result    
    except Exception as ex:
        print(ex)



fillNases()
