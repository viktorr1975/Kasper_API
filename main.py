from KlAkOAPI.AdmServer import KlAkAdmServer
from KlAkOAPI import Updates
from KlAkOAPI import HostGroup
from KlAkOAPI import ChunkAccessor
from datetime import timedelta

import urllib3
import socket
import struct
import csv
#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
username = 'administrator'
password = '1qazXSW@'
#!!!!!!!!!!!!!!!!!!!!!!!!!


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

def convert_int_to_ip(n):
# convert integer to IP4 address
# IP4 addresses can be represented in big-endian byte order,
    return socket.inet_ntoa(struct.pack('<I', n))

def save_to_csv(lstHostsData, strFileName="hosts.csv"):
# сохраняем список с данными хостов в файл формата CSV
    # список заголовков для данных хоста
    replacements = {
        "KLHST_WKS_DN": 'Имя',
        "KLHST_WKS_IP": 'IP',
        "KLHST_WKS_GROUPID": 'Группа'}
    # Extract all unique keys (headers)
    fieldnames = set()
    for entry in lstHostsData:
        fieldnames.update(entry.keys())
    fieldnames = list(fieldnames)
    # For replace the field names (headers)
#    fieldnames = ["KLHST_WKS_DN", "KLHST_WKS_IP", "KLHST_WKS_GROUPID"]
    headers = {x:replacements.get(x) for x in fieldnames}

#my_list = list(map(lambda x: new_value if x == old_value else x, my_list))
    # Writing to CSV
    with open(strFileName, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(headers)    # write the header
        #writer.writeheader(headers)  # Write header row
        writer.writerows(lstHostsData)  # Write data rows

def get_host_info(server, strQueryString):
#получение информации об устройстве
# strQueryString - Host display name
# примеры strQueryString: "*Name*", "nAME",
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    params = []
    if server is not None:
        oHostGroup = HostGroup.KlAkHostGroup(server)
        strAccessor = oHostGroup.FindHosts(
            'KLHST_WKS_DN = "' + strQueryString + '"', ["KLHST_WKS_GROUPID", "KLHST_WKS_DN", "KLHST_WKS_IP"],
            [], {'KLGRP_FIND_FROM_CUR_VS_ONLY': True},
            lMaxLifeTime=60 * 60 * 3).OutPar('strAccessor')

        nStart = 0
        nStep = 100
        oChunkAccessor = ChunkAccessor.KlAkChunkAccessor(server)
        nCount = oChunkAccessor.GetItemsCount(strAccessor).RetVal()
#        print("Found hosts count:", nCount)
        result = []
        while nStart < nCount:
            oChunk = oChunkAccessor.GetItemsChunk(strAccessor, nStart, nStep)
            parHosts = oChunk.OutPar('pChunk')['KLCSP_ITERATOR_ARRAY']
            for oObj in parHosts:
                host = {}
                host["KLHST_WKS_DN"] = oObj['KLHST_WKS_DN']
                host["KLHST_WKS_IP"] = convert_int_to_ip(oObj['KLHST_WKS_IP'])
                host["KLHST_WKS_GROUPID"] = oHostGroup.GetGroupInfo(oObj['KLHST_WKS_GROUPID']).retval.GetValue('name')
                result.append(host)
#                print('Found host: ' + oObj['KLHST_WKS_DN'])
#                print('Host IPv4 address with network byte order: ',  convert_int_to_ip(oObj['KLHST_WKS_IP']))
#                print('Group : ' + oHostGroup.GetGroupInfo(oObj['KLHST_WKS_GROUPID']).retval.GetValue('name'))
            nStart += nStep
        return result
    else:
        print('Ошибка доступа к серверу')

if __name__ == '__main__':
    for ip in KSC_LIST.values():
        server = ConnectKSC(ip)
        hosts = get_host_info(server, "*wIN*")
        save_to_csv(hosts, "hosts1.csv")