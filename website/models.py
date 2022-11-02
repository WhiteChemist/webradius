from curses import meta
from email.policy import default
from ipaddress import ip_address
from tabnanny import verbose
from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class nas(models.Model):

    class Meta:
        verbose_name = 'Сервер сетевого доступа'
        verbose_name_plural = 'Сервер сетевого доступа'

    id_nas = models.BigAutoField(primary_key=True)
    ip_address = models.GenericIPAddressField(null=False,verbose_name="IP адрес")
    short_name = models.TextField(max_length=30, null=False,verbose_name="Имя")
    secret_key = models.TextField(max_length=30, null=False,verbose_name="Секретный ключ")

    def __str__(self):
        return f"{self.short_name}"

class nas_port_type(models.Model):

    class Meta:
        verbose_name = 'Порт подключения'
        verbose_name_plural = 'Порт подключения'

    id_nas_port_type = models.BigAutoField(primary_key=True)
    port_type = models.TextField(max_length=20, null=False,verbose_name="Тип порта NAS")

    def __str__(self):
        return f"{self.port_type}"

class level_access_network(models.Model):

    class Meta:
        verbose_name = 'Уровень доступа к сети'
        verbose_name_plural = 'Уровень доступа к сети'

    id_level_access_network = models.BigAutoField(primary_key=True)
    type_level_access = models.TextField(max_length=20, null=False,verbose_name="Тип разрешения доступа к сети")

    def __str__(self):
        return f'{self.type_level_access}'


class level_access_network_devices(models.Model):

    class Meta:
        verbose_name = 'Уровень доступа к сетевому оборудованию '
        verbose_name_plural = 'Уровень доступа к сетевому оборудованию'
    
    id_level_access_network_devices = models.BigAutoField(primary_key=True)
    attribute = models.TextField(max_length=25,default="Mikrotik-Group",verbose_name="Аттрибут")
    type_level_access = models.TextField(max_length=20, null=False,verbose_name="Тип разрешения доступа к сетевому оборудованию")

    def __str__(self):
        return f"{self.type_level_access}"


class user_groups(models.Model):

    class Meta:
        verbose_name = 'Группы пользователей '
        verbose_name_plural = 'Группы пользователей'

    id_user_group = models.BigAutoField(primary_key=True)
    group = models.TextField(max_length=40, null=False,verbose_name="Группа")
    id_level_access_network = models.ForeignKey(
        level_access_network, on_delete=models.CASCADE,verbose_name="Тип разрешения доступа к сети"
    )
    id_level_access_network_devices = models.ForeignKey(
        level_access_network_devices, on_delete=models.CASCADE,verbose_name="Тип разрешения доступа к сетевому оборудованию"
    )

    def __str__(self):
        return f"{self.group}"


class mac_addresses(models.Model):
    class Meta:
        verbose_name = 'Таблица мак адресов пользователей'
        verbose_name_plural = 'Таблица мак адресов пользователей'

    id_user_mac = models.BigAutoField(primary_key=True,default=0)
    mac_address_eth = models.TextField(
        max_length=17,
        verbose_name="Мак адрес сетевой карты ethernet",
        validators=[
            RegexValidator(
                regex="^[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){5}$",
                message="Неизвестный тип мак адреса",
            )
        ],
        null=True,
    )
    mac_address_wifi = models.TextField(
        max_length=17,
        verbose_name="Мак адрес сетевой карты WiFi",
        validators=[
            RegexValidator(
                regex="^[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){5}$",
                message="Неизвестный тип мак адреса",
            )
        ],
        null=True,
    )
    mac_address_add_1 = models.TextField(
        max_length=17,
        verbose_name="Мак адрес сетевого адаптера",
        validators=[
            RegexValidator(
                regex="^[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){5}$",
                message="Неизвестный тип мак адреса",
            )
        ],
        null=True,
        help_text="Дополнительный мак адрес (Необязательно)",
        blank=True
    )
    mac_address_add_2 = models.TextField(
        max_length=17,
        verbose_name="Мак адрес сетевого адаптера",
        validators=[
            RegexValidator(
                regex="^[a-fA-F0-9]{2}(:[a-fA-F0-9]{2}){5}$",
                message="Неизвестный тип мак адреса",
            )
        ],
        null=True,
        help_text="Дополнительный мак адрес (Необязательно)",
        blank=True
    )

class users(models.Model):

    class Meta:
        verbose_name = 'Пользователи'
        verbose_name_plural = 'Пользователи'

    id_users = models.BigAutoField(primary_key=True)
    username = models.TextField(max_length=40, null=True,verbose_name="Фамилия")
    uname = models.TextField(max_length=20, null=True,verbose_name="Имя",blank=True)
    ulast_name = models.TextField(max_length=30, null=True,verbose_name="Отчество",blank=True)
    id_user_group = models.ForeignKey(user_groups, on_delete=models.CASCADE,verbose_name="Группа пользователя")
    id_mac = models.ForeignKey(mac_addresses, on_delete=models.CASCADE,verbose_name="Мак адреса",default=0)
    email = models.EmailField(null=False,verbose_name="Электронный адрес",default="user@mail.com")
    level_access_network = models.ForeignKey(
        level_access_network, on_delete=models.CASCADE,verbose_name="Тип разрешения доступа к сети"
    )
    id_level_access_network_devices = models.ForeignKey(
        level_access_network_devices, on_delete=models.CASCADE,verbose_name="Тип разрешения доступа к сетевому оборудованию"
    )
    network_login = models.TextField(max_length=30,null=False,default="",verbose_name="Логин для подключения к сетевому оборудованию",help_text="Логин для подключения к сетевому оборудованию (Необязательно)")
     
    def __str__(self):
        return f"{self.username}"

class fail_tries(models.Model):

    class Meta:
        verbose_name = 'Неуспешные попытки подключения'
        verbose_name_plural = 'Неуспешные попытки подключения'

    id_fail_try = models.BigAutoField(primary_key=True)
    id_user = models.ForeignKey(nas_port_type, on_delete=models.CASCADE)
    id_nas_connect = models.ForeignKey(nas, on_delete=models.CASCADE,verbose_name="На каком NAS произошла ошибка")
    id_nas_port = models.ForeignKey(nas_port_type, on_delete=models.CASCADE,related_name='%(class)s_requests_created',verbose_name="Тип доступа")

