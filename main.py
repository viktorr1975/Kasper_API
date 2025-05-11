from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI import Updates
from datetime import timedelta

import urllib3

username = 'administrator'
password = '1qazXSW@'

KSC_LIST = {
    'WINDOWS': 'https://192.168.122.181:13299', # VM win2k16-3
#    'LINUX': 'https://IP_KSC_LINUX:13299'
}

def ConnectKSC(ip):
    while True:
        try:
            connect = KlAkAdmServer.Create(ip, username, password, verify=False, vserver='')

            if connect:
                print('Успешно подключился к {}'.format(ip))
            else:
                print('Ошибка подключения к {}'.format(ip))
                exit()

            return connect
        except Exception as e:
            print(e)
            return None

def get_status_hosts(server, ip):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        params = []
        if server is not None:
            straccessor = Updates.KlAkUpdates(server).GetUpdatesInfo(pFilter=params)
            ncount = straccessor.RetVal()
            if ip == KSC_LIST['WINDOWS']:
                data = ncount[1]
                print('')
                print('KSC ======== [ {} ] ========'.format(KSC_LIST['WINDOWS']))
                print('Дата создания: {}'.format(data['Date'] + timedelta(hours=3)))
                print('Дата получения: {}'.format(data['KLUPDSRV_BUNDLE_DWL_DATE'] + timedelta(hours=3)))
                print('============================')
            elif ip == KSC_LIST['LINUX']:
                data = ncount[2]
                print('')
                print('KSC ======== [ {} ] ========'.format(KSC_LIST['LINUX']))
                print('Дата создания: {}'.format(data['Date'] + timedelta(hours=3)))
                print('Дата получения: {}'.format(data['KLUPDSRV_BUNDLE_DWL_DATE'] + timedelta(hours=3)))
                print('============================')
        else:
            print('Ошибка доступа к серверу')

if __name__ == '__main__':
    for ip in KSC_LIST.values():
        server = ConnectKSC(ip)
        get_status_hosts(server, ip)