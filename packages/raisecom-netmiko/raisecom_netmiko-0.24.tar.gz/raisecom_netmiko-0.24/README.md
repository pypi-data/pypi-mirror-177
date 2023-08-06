# raisecom-netmiko
## Обзор
Пакет позволяющий взаимодействовать с оборудованием Raisecom  
Библиотека загружена на pypi https://pypi.org/project/raisecom-netmiko/

## Установка
```
pip install raisecom-netmiko
```

## Функционал
Реализованные методы:  
-get_facts  
-get_environment  
-get_lldp_neighbors_detail  
-get_interfaces  
-get_config  

## Процесс обновления пакета с заливанием на pypi
Изменяем setup.py в корне и по необходимости __init__ внутри функциональной директории

Из корня проекта
Билдим:
```
python setup.py sdist
```
Отправляем на pypi
```
twine upload dist/*
```
