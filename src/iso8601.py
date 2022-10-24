Debug = False

def from_iso8601(date_iso8601: str, out_pattern= 'D/', lang = 0) -> list:
    '''
        date_input in iso8601 (f5) format: 'YYYY-MM-DDThh:mm 

        out_pattern in format: 'X+separator' X: D or M or Y

        Return: [bool, str, weekday]

        if operation was ok return[0] is True

        ie:
        out_pattern= 'D/' return[1] = 'DD/MM/YYYY hh:mm'
        out_pattern= 'M-' return[1] = 'MM-DD-YYYY hh:mm'
        
        lang= 0 (pt), lang= 1 (en), etc...

        return[2] = weekday
    '''
    if len(date_iso8601) != 16 or not date_iso8601[0:4].isnumeric() or date_iso8601[4] != '-' or not date_iso8601[5:7].isnumeric() or date_iso8601[7] != '-' or not date_iso8601[8:10].isnumeric() or date_iso8601[10] !='T' or not date_iso8601[11:13].isnumeric() or date_iso8601[13] != ':' or not date_iso8601[14:].isnumeric() : return [False,['dd/mm/aaaa','mm-dd-yyyy'][lang]]
    if len(out_pattern) != 2 or not out_pattern[0].isalpha() or out_pattern[1].isalpha(): return [False, ['Padrão de saída errado','Wrong out pattern'][lang]]
    sep = out_pattern[1]
    match out_pattern[0]:
        case 'D' | 'd':
            return [True, date_iso8601[8:10] + sep + date_iso8601[5:7] + sep + date_iso8601[0:4] + ' ' + date_iso8601[11:], weekday(date_iso8601[0:4],date_iso8601[5:7],date_iso8601[8:10],lang)]
        case 'M' | 'm':
            return [True, date_iso8601[5:7] + sep + date_iso8601[8:10] + sep + date_iso8601[0:4] + ' ' + date_iso8601[11:], weekday(date_iso8601[0:4],date_iso8601[5:7],date_iso8601[8:10],lang)]
        case 'Y' | 'y':
            return [True, date_iso8601[0:4] + sep + date_iso8601[5:7] + sep + date_iso8601[8:10] + ' ' + date_iso8601[11:], weekday(date_iso8601[0:4],date_iso8601[5:7],date_iso8601[8:10],lang)]

def to_iso8601(date_entry: str, pattern: str, lang = 0) -> list:
    '''
    date entries:
                      
        pattern 'D': 'DDsMMsYYYYshhsmm' or 'DDsMMsYYYY' s: any separator
        pattern 'M': 'MMsDDsYYYYshhsmm' or 'MMsDDsYYYY' s: any separator
        pattern 'Y': 'YYYYsMMsDDshhsmm' or 'YYYYsMMsDD' s: any separator

    As above, the patterns can be: 'D' or 'M' or 'Y'
    
    if date entries format was, return[0]: True, else: False.

    return[1]:
        if hhsmm exists: 'YYYY-MM-DDThh:mm'
        else:            'YYYY-MM-DDT00:00'    
    '''
     
    f = ['Erro, use: dd/mm/aaaa','Wrong, use: mm-dd-yyyy'][lang]
    r =  [False, f]

    if pattern.upper() == 'D' or pattern.upper() == 'M':   
        if len(date_entry) == 16 and date_entry[:2].isnumeric() and date_entry[3:5].isnumeric() and date_entry[6:10].isnumeric() and date_entry[11:13].isnumeric() and date_entry[14:].isnumeric():
            if pattern.upper() =='D':
                f = date_entry[6:10]+'-'+date_entry[3:5]+'-'+date_entry[:2]+'T'+date_entry[11:13]+':'+date_entry[14:]
            else:
                f = date_entry[6:10]+'-'+date_entry[:2]+'-'+date_entry[3:5]+'T'+date_entry[11:13]+':'+date_entry[14:]
            r =[True,f]        
        if len(date_entry) == 10 and date_entry[:2].isnumeric() and date_entry[3:5].isnumeric() and date_entry[6:].isnumeric():
            if pattern.upper() == 'D':
                f = date_entry[6:]+'-'+date_entry[3:5]+'-'+date_entry[:2]+'T00:00'
            else:
                f = date_entry[6:]+'-'+date_entry[:2]+'-'+date_entry[3:5]+'T00:00'
            r =[True,f] 
    if pattern.upper() == 'Y':   
        if len(date_entry) == 16 and date_entry[:4].isnumeric() and date_entry[5:7].isnumeric() and date_entry[8:10].isnumeric() and date_entry[11:13].isnumeric() and date_entry[14:].isnumeric():
            f = date_entry[:4]+'-'+date_entry[5:7]+'-'+date_entry[8:10]+'T'+date_entry[11:13]+':'+date_entry[14:]
            r =[True,f]        
        if len(date_entry) == 10 and date_entry[:4].isnumeric() and date_entry[5:7].isnumeric() and date_entry[8:10].isnumeric():
            f = date_entry[:4]+'-'+date_entry[5:7]+'-'+date_entry[8:10]+'T00:00'
            r =[True,f]  
    # YYYY-MM-DDThh:mm
    # 0123456789012345
    r[0] = validate_date(int(f[:4]),int(f[5:7]),int(f[8:10]),int(f[11:13]),int(f[14:])) if r[0] == True else ...   
    return r

def validate_date(year: int,month : int,day:int,hour:int,minute:int) ->bool:
    debug = False
    if year > 1900 and year < 2100:
        if month >0 and month <13:
            if (day>0 and day <32) and (month == 1 or month ==3 or month ==5 or month == 7 or month == 8 or month == 10 or month ==12):
                return True
            if (day>0 and day<31) and (month ==4 or month==6 or month==9 or month==11):
                return True
            if (day>0 and day <29) and month ==2:
                return True
            if day==29 and month==2 and (year%40==0 or year%4==0 and year%100 !=0):
                return True
    print(f'validate_date: False -> {year} {month} {day} {hour} {minute}') if debug or Debug else ...
    return False



def weekday(y,m,d,lang=0):
    t = [0,3,2,5,0,3,5,1,4,6,2,4]
    pt = ['Domingo','2a feira','3a feira','4a feira','5a feira','6a feira','Sábado']
    en = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
    wd = (int(y) + int(int(y)/4) - int(int(y)/100) + int(int(y)/400) + t[int(m)-1] +int(d) ) % 7 
    return pt[wd] if lang == 0 else en[wd]


if __name__ == '__main__':    
    if Debug:
        # print(weekday(2022,6,29,1))
        # print(from_iso8601('2022-06-29T00:00','d/'))
        # print(to_iso8601('29/06/2022 13:55','d'))
        # print(to_iso8601('06/29/2022 13:55','m'))
        # print(to_iso8601('2022 06 29','y'))
        print(to_iso8601('30/12/1957','d'))
    else:
        ...