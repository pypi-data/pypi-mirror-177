import typing as t
arrow2 = '\u2192'

def BG(r, g, b): return '\x1b[48;2;%d;%d;%dm'%(r, g, b)

def FG(r, g, b): return '\x1b[38;2;%d;%d;%dm'%(r, g, b)

def RS(): return '\x1b[0m'

def ColourText(text, fgcolor : tuple, bgcolor : tuple = (0,0,0)):
    return BG(*bgcolor) + FG(*fgcolor) + text + RS()

def O(*mes, sep=None, end=None, file = None, flush = []):
    print(*mes, sep=sep, end=end, file=file, flush=flush)

def dangerous(text: str, sep = True,  end = '\n'):
    text = text.strip()
    text = f'{arrow2 if sep else ""}{text}{":" if sep else ""}'
    O(ColourText(text, (255, 255, 255), (200, 0, 0)), end=end)
    O(RS(), end='')

def warning(text: str, sep = True, end = '\n'):
    text = text.strip()
    text = f'{arrow2 if sep else ""}{text}{":" if sep else ""}'
    O(ColourText(text, (255, 255, 255), (200, 100, 30)), end=end)
    O(RS(), end='')

def info(text: str, sep = True, end = '\n'):
    text = text.strip()
    text = f'{arrow2 if sep else ""}{text}{":" if sep else ""}'
    O(ColourText(text, (50, 50, 50), (200, 200, 200)), end=end)
    O(RS(), end='')

def success(text: str, sep = True, end = '\n'):
    text = text.strip()
    text = f'{arrow2 if sep else ""}{text}{":" if sep else ""}'
    O(ColourText(text, (255, 255, 255), (0, 200, 0)), end=end)
    O(RS(), end='')

def fail(text: str, sep = True, end = '\n'):
    dangerous(text, end)

def setvalue(object : str, value, fmttext : str = ..., sep = True,end='\n'):
    try: text = fmttext%(object, str(value).strip())
    except:
        fmttext = f'set %s {arrow2 if sep else ""} %s'
        text = fmttext%(object, str(value).strip())
    O(ColourText(text, (255, 255, 255), (0, 0, 200)), end=end)
    O(RS(), end='')

def defaultprocess(txt: str):
    return txt.strip()

def IPut(text, cast : type = str, process : t.Callable[..., t.Any] = defaultprocess):
    k = input(RS() + text + FG(255, 255, 0))
    if k == '!exit':
        O(RS(), end='')
        return '^exit^'
    elif k == '':
        O(RS(), end='')
        return '^enter^'
    return cast(process(k))