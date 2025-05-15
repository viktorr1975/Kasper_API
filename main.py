from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI import Updates
from KlAkOAPI import HostGroup
from KlAkOAPI import ChunkAccessor
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
#получение информации о датах обновлений
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

def get_host_info(server, strQueryString):
#получение информации об устройстве
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    params = []
    if server is not None:
        oHostGroup = HostGroup.KlAkHostGroup(server)
        strAccessor = oHostGroup.FindHosts(
            strQueryString, ["KLHST_WKS_HOSTNAME", "KLHST_WKS_DN"],
            [], {'KLGRP_FIND_FROM_CUR_VS_ONLY': True},
            lMaxLifeTime=60 * 60 * 3).OutPar('strAccessor')

        nStart = 0
        nStep = 100
        oChunkAccessor = ChunkAccessor.KlAkChunkAccessor(server)
        nCount = oChunkAccessor.GetItemsCount(strAccessor).RetVal()
        print("Found hosts count:", nCount)

        while nStart < nCount:
            oChunk = oChunkAccessor.GetItemsChunk(strAccessor, nStart, nStep)
            parHosts = oChunk.OutPar('pChunk')['KLCSP_ITERATOR_ARRAY']
            for oObj in parHosts:
                print('Found host: ' + oObj['KLHST_WKS_DN'])
            nStart += nStep
    else:
        print('Ошибка доступа к серверу')

if __name__ == '__main__':
    for ip in KSC_LIST.values():
        server = ConnectKSC(ip)
        get_host_info(server, 'KLHST_WKS_DN = "WIN*"')