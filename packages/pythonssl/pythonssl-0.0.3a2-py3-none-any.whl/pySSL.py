# Version 0.0.3a0 (TV)
# Fixing: Interface Console and DNS-IP problems
# Pre-version: 0.0.2a0
# Author: Phuc Bao (Samson)
# Date: 19/11/22

# Feature:
# - Using RSA encrypto algorithm for generate key
# - The SHA encrypto algorithms supported by pythonssl to make the sign:
#     + SHA11
#     + SHA224
#     + SHA256
#     + SHA384
#     + SHA3_224
#     + SHA3_256
#     + SHA3_384
#     + SHA3_512
#     + SHA512512
#     + SHA512_256
#     + SHA512_224

from pyssl._pyssl import (
    PySSL,
    default_backend
)

import subprocess
import sys, os

#Verion 0.0.2:
import winreg as wr

def checkVT100():
    try:
        console_hk_ex =wr.OpenKeyEx(wr.HKEY_CURRENT_USER, 'console\\')
        value = wr.QueryValueEx(console_hk_ex, 'VirtualTerminalLevel')
        if value[0] != 1:
            wr.SetValueEx(console_hk_ex, 'VirtualTerminalLevel', 0, wr.REG_DWORD, 1)
        return True
    except:
        return False

from color import *
from color import (
    ExitCommandActivity,
    EnterActivity
)


def echooff(): os.system('echo off')
def clsr(pause : bool = False): 
    if pause: input('Press any key to continue . . .')
    os.system('cls')
def settitle(name): os.system(f'title {name}')



def arr_InfoOf(text):
    tmp_arr = []
    info(text)
    while True:
        try:
            tmp = IPut('$>>')
            tmp_arr.append(tmp)
        except EnterActivity or ExitCommandActivity: break
    if tmp_arr:
        ed = 's' if len(tmp_arr) > 1 else ''
        success(f'{arrow2}Appended your data successful! With {len(tmp_arr)} value{ed}', sep=False)
        return tmp_arr
    else:
        from socket import (gethostbyname as GHBN, gethostname as GHN)
        return ['0.0.0.0', '127.0.0.1', GHBN(GHN())]

def dict_InfoOf(text, **key_appear):
    tmp_dict = {}
    MAX_LENGHT_LEFT = 0
    MAX_LENGHT_RIGHT = 0
    info(text)

    for key in key_appear:
        try:
            t = f'${key_appear[key]}>>'
            tmp_dict[key] = IPut(t)
            tmp_len =  len(key) + len(key_appear[key]) + 2 , len(tmp_dict[key])
            MAX_LENGHT_LEFT = max([tmp_len[0], MAX_LENGHT_LEFT])
            MAX_LENGHT_RIGHT =  max([tmp_len[1], MAX_LENGHT_RIGHT])
        except ExitCommandActivity: break
        except EnterActivity: continue

    for i in tmp_dict:
        success('OK', end='')
        setvalue(
            f'{key_appear[i]}({i})', tmp_dict[i], 
            fmttext=f'set %{MAX_LENGHT_LEFT}s {arrow2} %{MAX_LENGHT_RIGHT}s')
    if tmp_dict: return tmp_dict
    else:
        if 'CN' in key_appear: return {'CN' : 'FullstackMqtt certificate', 'C' : 'Vi'}
        return {}

def select_InfoOf(text, option):
    info(text)
    if type(option) is dict: option = list(option.keys())
    elif type(option) is list: option = option
    else: raise Exception('Data type must be iterator or dictionary')
    # Print selections
    for i in range(len(option)): O(f'{i}.{option[i]}')

    try: tmp = IPut('$>>', int)
    except EnterActivity or ExitCommandActivity:tmp = 2
    except ValueError: raise Exception('I don\'t have any idea what you wanting')
    finally: O(RS(), end='')
    return option[tmp]


namedict = {
    'CN' : "common_name",
    'C' : "country_name",
    'L': "locality_name",
    'ST' : "state_or_province_name",
    'BC' : "business_category",
    "DNQ": "dn_qualifier",
    'O': "organization_name",
    'OU': "organizational_unit_name",
    'EMAIL' : "email_address",
    'DC' : "domain_component",
    'SERIALNUM': "serial_number",
    'TITLE': "title",
    'SN' : "surname",
    'GN' : "given_name",
    'PDN ': "pseudonym",
    'GQ': "generation_qualifier",
    'INN': "inn",
    "JC" : "jurisdiction_country_name",
    'JST' : "jurisdiction_state_or_province_name",
    'JL': "jurisdiction_locality_name"
}

shaenc = {
    'SHA1' : '1' ,
    'SHA224' :'244',
    'SHA256' :'256',
    'SHA384' :'384',
    'SHA3_224' :'3_224',
    'SHA3_256' :'3_256',
    'SHA3_384' :'3_384',
    'SHA3_512' :'3_512',
    'SHA512' : '512',
    'SHA512_256' :'512_256',
    'SHA512_224' : '512_2'
}

def runcmd():
    if not checkVT100():
        print('Run file install.py to setup enviroment!')
        exit(0)

    #Setting Interface
    echooff()
    settitle('PySSL Tools')

    clsr()
    dns_ip = arr_InfoOf('Type DNS/IP supported by certificate (press enter when property is empty to finished)')
    clsr(True)
    issuedto = dict_InfoOf('Issued to', **namedict)
    clsr(True)
    issuedby = dict_InfoOf('Issued by', **namedict)
    clsr(True)
    tmpk = {'KS': "key_size", 'PE': 'public_exponent', "BE": "backendfile"}
    rsa_information = {}
    def Check(text, dict_data, key, default, dict_need_to_get, func_test):
        try:
            tmp = dict_data[key]
            warning(text, end="")
            try:
                if func_test(tmp): 
                    success('OK', sep=False)
                    dict_need_to_get.pop(key)
                    dict_data[key] = int(tmp)
                else: dangerous('NOT SECURE', sep=False)
            except ValueError:
                dangerous('VALID VALUE', sep=False)
        except:            
            dict_data[key] = default
            dict_need_to_get.pop(key)
        return dict_data, dict_need_to_get

    while tmpk:
        O(f'{"configure the RSA encrypto":=^50}')
        rsa_information.update(**dict_InfoOf('RSA configure', **tmpk))
        rsa_information, tmpk = Check('Check key size', rsa_information, 'KS', 2048, tmpk, lambda x : int(x) >= 2048)
        rsa_information, tmpk = Check('Check public exponent', rsa_information, 'PE', 2**16 + 1, tmpk, lambda x: int(x) >= 2**16+1)
        rsa_information, tmpk = Check('Check backend file', rsa_information, 'BE', default_backend(), tmpk, lambda x: os.path.isfile(x))
        
        if tmpk:
            try: tmp = input('$press enter to re-input; type "!exit" to exit the program>>')
            except ExitCommandActivity:
                O(RS(), end='')
                exit(1)
            except EnterActivity:
                clsr(True)
                continue
    
    clsr(True)
    typeSHA = shaenc[select_InfoOf('SHA TYPE', list(shaenc.keys()))]
    clsr(True)

    O(f'{"setting":=^50}')
    serialnum = IPut('$serial number>>', int, default=1000)
    days = IPut('$days>>', int, default= 365)
    
    kwargs = {}
    if issuedto: kwargs['issueto'] = issuedto
    if issuedby: kwargs['issueby'] = issuedby
    if serialnum: kwargs['serialnumber'] = serialnum
    kwargs['public_exponent'] = rsa_information['PE']
    kwargs['backend']= rsa_information['BE']
    kwargs['key_size'] = rsa_information['KS']
    kwargs['typeSHA'] = typeSHA
    kwargs['days'] = days

    clsr(True)
    warning('Check infomation', end="")
    try:
        a = PySSL(**kwargs)
        success('OK', sep=False)
    except:
        dangerous('FAIL', sep=False)
        exit(0)
    O(f'{"make":=^50}')

    info('Make key', end='')
    try:
        a.generatekey()
        success('OK', sep=False)
    except: 
        dangerous('FAIL', sep=False)
        exit(0)

    info('Make name', end='')
    try:
        a.makename()
        success('OK', sep=False)
    except: 
        dangerous('FAIL', sep=False)
        exit(0)

    info('Make alternate name', end='')
    try:
        a.makealtname(*dns_ip)
        success('OK', sep=False)
    except: 
        dangerous('FAIL', sep=False)
        exit(0)

    info('Make basic constraint', end='')
    try:
        a.makebasicconstraint()
        success('OK', sep=False)
    except: 
        dangerous('FAIL', sep=False)
        exit(0)
        
    info('Make certificate', end='')

    a.makecertificate()
    try:
        a.makecertificate()
        success('OK', sep=False)
    except: 
        dangerous('FAIL', sep=False)
        exit(0)
    info('Status builded', end='')
    success('Finished all', sep=False)

    try: filecertio = IPut('$file cert>>')
    except EnterActivity: filecertio = issuedto['CN']
    except ExitCommandActivity: filekeyio = issuedto['CN']+ '_pri'
    try: filekeyio = IPut('$file private key>>')
    except EnterActivity: filekeyio = issuedto['CN']+ '_pri'
    except ExitCommandActivity: filekeyio = issuedto['CN']+ '_pri'
    info('Export file', end='')
    
    try:
        a.exportfile(filecertio, filekeyio)
        success('OK', sep=False)
    except: 
        dangerous('FAIL', sep=False)
        exit(0)
    input('Enter to end')
    clsr()
    O('Check it at: ')
    O(ColourText(os.path.abspath(filecertio+'.crt'), (255, 255, 14)))
    O(ColourText(os.path.abspath(filekeyio + '.pem'), (255, 255, 14)))

if __name__ == "__main__": runcmd()