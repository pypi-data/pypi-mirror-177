from pyssl._makecode import (
    makessl,
    default_value as DV
)

from pyssl._pyssl import (
    PySSL,
    default_backend
)

import subprocess
import sys, os

def inputvalue(cast = str):
    while True:
        tmp = input('>>')
        if tmp == "": return 'ENT'
        else:
            try: 
                return cast(tmp)
            except:
                print('It\'s only supported for %s'%cast.__name__)
                exit(0)

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

def echooff(): os.system('echo off')
def clsr(pause : bool = False): 
    if pause: input('Press any key to continue . . .')
    os.system('cls')
def settitle(name): os.system(f'title {name}')



def arr_InfoOf(text):
    tmp_arr = []
    info(text)
    while True:
        tmp = IPut('$>>')
        if tmp == '^enter^' or tmp == '^exit^':break
        tmp_arr.append(tmp)
    ed = 's' if len(tmp_arr) > 1 else ''
    success(f'{arrow2}Appended your data successful! With {len(tmp_arr)} value{ed}', sep=False)
    return tmp_arr

def dict_InfoOf(text, **key_appear):
    tmp_dict = {}
    MAX_LENGHT_LEFT = 0
    MAX_LENGHT_RIGHT = 0
    info(text)
    for key in key_appear:
        t = f'${key_appear[key]}>>'
        tmp = IPut(t)
        if tmp != '^exit^' and tmp != '^enter^': 
            tmp_dict[key] = tmp
            tmp_len =  len(key) + len(key_appear[key]) + 2 , len(tmp)
            MAX_LENGHT_LEFT = tmp_len[0] if tmp_len[0] > MAX_LENGHT_LEFT else MAX_LENGHT_LEFT
            MAX_LENGHT_RIGHT = tmp_len[1] if tmp_len[1] > MAX_LENGHT_RIGHT else MAX_LENGHT_RIGHT
        elif tmp == '^exit^':
            break
    for i in tmp_dict:
        success('OK', end='')
        setvalue(
            f'{key_appear[i]}({i})', 
            tmp_dict[i], 
            fmttext=f'set %{MAX_LENGHT_LEFT}s {arrow2} %{MAX_LENGHT_RIGHT}s')
    return tmp_dict

def select_InfoOf(text, list_value):
    info(text)
    for i in range(len(list_value)):
        O(f'{i}.{list_value[i]}')
    tmp = IPut('$>>', int)
    return list_value[tmp]


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
    while tmpk:
        O(f'{"configure the encrypto":=^50}')
        rsa_information.update(**dict_InfoOf('RSA configure', **tmpk))
        try:
            tmp = rsa_information['KS']
            warning('CHECK key size', end="")
            if int(tmp) >= 2048: 
                success('OK', sep=False)
                tmpk.pop('KS')
                rsa_information['KS'] = int(tmp)
            else:
                dangerous('NOT SECURE', sep=False)
            pass
        except:            
            rsa_information['KS'] = 2048
            tmpk.pop('KS')
        try:
            tmp = rsa_information['PE']
            warning('CHECK public exponent', end="")
            if int(tmp) >= 2**16+1: 
                success('OK', sep=False)
                tmpk.pop('PE')
                rsa_information['PE'] = int(tmp)
            else:
                dangerous('NOT SECURE', sep=False)
        except:
            rsa_information['PE'] = 2**16 + 1
            tmpk.pop('PE')
            
        try:
            tmp = rsa_information['BE']
            warning('CHECK backend file', end="")
            if os.path.isfile(tmp):
                setvalue('$databackend', f'reader({tmp})', 
                        fmttext=f'set $s {arrow2} %s', end=":")
                success('OK', sep=False)                
                tmpk.pop('BE')
            else:
                dangerous('NOT EXIST', sep=False)
        except: 
            rsa_information['BE'] = default_backend()
            tmpk.pop('BE')
        if tmpk:
            tmp = input('Press enter to re-text; type "!exit" to exit the program: ')
            if tmp == '!exit':
                O(RS())
                exit(1)
            clsr(True)
    clsr(True)
    typeSHA = shaenc[select_InfoOf('SHA TYPE', list(shaenc.keys()))]
    O(RS())
    clsr(True)
    O(f'{"setting":=^50}')
    try:serialnum = IPut('$serial number>>', int)
    except: serialnum = 1000
    O(RS())
    try: days = IPut('$days>>', int)
    except: days = 365
    kwargs = {}
    O(RS())
    if issuedto: kwargs['issueto'] = issuedto
    if issuedby: kwargs['issueby'] = issuedby
    if serialnum: kwargs['serialnumber'] = serialnum
    kwargs['public_exponent'] = rsa_information['PE']
    kwargs['backend']= rsa_information['BE']
    kwargs['key_size'] = rsa_information['KS']
    kwargs['typeSHA'] = typeSHA
    kwargs['days'] = days
    warning('Check infomation', end="")
    try:
        a = PySSL(**kwargs)
        success('OK', sep=False)
    except:
        dangerous('FAIL', sep=False)
        exit(0)
    clsr(True)
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
        a.makealtname()
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
        a.makealtname()
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
    info('Status builded')
    success('Finished all', end='')

    filecertio = IPut('$file cert>>')
    if filecertio == '^enter^':
        filecertio = issuedto['CN']+ '.crt'
    filekeyio = IPut('$file key>>')
    if filekeyio == '^enter^':
        filekeyio = issuedto['CN']+ '_pri.pem'
    info('export file', end='')
    
    try:
        a.exportfile(filecertio, filekeyio)
        success('OK', sep=False)
    except: 
        dangerous('FAIL', sep=False)
        exit(0)
    input('Enter to close')
    clsr()
    O('Check it at: ')
    O(ColourText(os.path.abspath(filecertio), (255, 255, 14)))
    O(ColourText(os.path.abspath(filekeyio), (255, 255, 14)))

runcmd()