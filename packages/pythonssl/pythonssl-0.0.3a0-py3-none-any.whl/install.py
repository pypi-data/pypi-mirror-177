
import winreg as wr

def enableVT100():
    console_hk_ex = wr.OpenKeyEx(wr.HKEY_CURRENT_USER, 'console\\', access=wr.KEY_SET_VALUE)
    wr.SetValueEx(console_hk_ex, 'VirtualTerminalLevel', 0, wr.REG_DWORD, 1)

def checkadminsistrator():
    import ctypes
    return ctypes.windll.shell32.IsUserAnAdmin() != 0
if __name__ == '__main__':
    if checkadminsistrator(): enableVT100()
    else: print("Run it as adminsistrator!")