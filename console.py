# содержание справки для вывода в командной строке
# версия 1.0 умеет получать данные одного устройства по имени
helpme = '''Применение скрипта: 
main.py -s KSCip -n HostName [-i] [-o]
    Если задан параметр -n в командной строке, скрипт ищет информацию о хосте с именем HostName
на сервере с адресом IP, заданном в параметре -s.
    Если задан параметр -o в командной строке, то сведения об устройстве выводится в указанный файл. Если опция -o не 
задана, результат выводится в файл hostesdata.csv
    Если задан параметр -l в командной строке, то сведения о выполнении скрипта и итоговые результаты поиска данных
об устройстве выводится в указанный файл. Если опция -l не задана, информация сохранится в файл log.txt
'''
#     Если задан параметр -i в командной строке, то имена хостов берутся из указанного файла.Если не задан
# параметр -i в командной строке, скрипт читает из файла hostesnames.txt имена хостов и ищет информацию о них
# на сервере с адресом IP, заданном в параметре -s.
# описание аргумента -s
help_s = 'Обязательный аргумент. IP адрес сервера KSC на котором ищется информация'
# описание аргумента -n
help_host_name = 'Обязательный аргумент. Имя хоста по которому ищется информация'
# описание аргумента -i
help_in = 'Необязательный аргумент. Имя файла со списком имён хостов. Имя файла по умолчанию "hostesnames"'
# значение по умолчанию аргумента -i
default_in = "hostesnames.txt"
# описание аргумента -o
help_out = 'Необязательный аргумент. Имя файла сведений об устройстве. Имя файла по умолчанию "hostesdata.csv"'
# значение по умолчанию аргумента -o
default_out = "hostesdata.csv"
help_log = 'Необязательный аргумент. Имя файла лога. Имя файла по умолчанию "log.txt"'
# значение по умолчанию аргумента -o
default_log = "log.txt"
#  `type` может вам помогать в качестве валидатора, кроме как для приведения значения в тот вид что вам нужен
#
# import os
# import argparse
#
# def validate_path(path: str) -> str:
#     if not os.path.isabs(path):
#         raise argparse.ArgumentTypeError(f'Absolute path required, got "{path}"')
#
#     return os.path.normpath(path)
#
# parser.add_argument('--path', metavar='PATH', type=validate_path)


# parser = argparse.ArgumentParser()
# parser.add_argument('infile', nargs='?', type=argparse.FileType('r'),
#                     default=sys.stdin)
# parser.add_argument('outfile', nargs='?', type=argparse.FileType('w'),
#                     default=sys.stdout)
# parser.parse_args(['input.txt', 'output.txt'])
# Namespace(infile=<_io.TextIOWrapper name='input.txt' encoding='UTF-8'>,
#           outfile=<_io.TextIOWrapper name='output.txt' encoding='UTF-8'>)
# parser.parse_args([])
# Namespace(infile=<_io.TextIOWrapper name='<stdin>' encoding='UTF-8'>,
#           outfile=<_io.TextIOWrapper name='<stdout>' encoding='UTF-8'>)