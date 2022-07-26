import re

#
class DT_Manager:
    #
    def __init__(self):
        pass

    # 
    def dateConvert(self, value, from_mode, to_mode):
        d = ""
        m = ""
        y = ""

        # mode = it|en|iso
        if from_mode == "it":
            d = value[0:2]
            m = value[3:5]
            y = value[6:10] 
        elif from_mode == "en":
            d = value[3:5]
            m = value[0:2]
            y = value[6:10] 
        elif from_mode == "iso":
            d = value[8:10]
            m = value[5:7]
            y = value[0:4] 
        else:
            # Nessuna conversione
            pass
    
        if to_mode == "it":
            return d + "-" + m + "-" + y
        elif to_mode == "en":
            return m + "-" + d + "-" + y
        elif to_mode == "iso":
            return y + "-" + m + "-" + d
        else:
            # Nessuna conversione
            pass

    #
    def date_validator(self, value, mode):
        if len(value) != 10: 
            return False

        if mode == "it": # DD-MM-YYYY 
            r = '^[0-9]{2}\-[0-9]{2}\-[0-9]{4}$'
            if not re.search(r, value):
                return False
            d = int(value[0:2])
            m = int(value[3:5])
            y = int(value[6:10])
        elif mode == "en": # MM-DD-YYYY 
            r = '^[0-9]{2}\-[0-9]{2}\-[0-9]{4}$'
            if not re.search(r, value):
                return False 
            d = int(value[3:5])
            m = int(value[0:2])
            y = int(value[6:10])
        elif mode == "iso": # YYYY-MM-DD 
            r = '^[0-9]{4}\-[0-9]{2}\-[0-9]{2}$'
            if not re.search(r, value):
                return False 
            d = int(value[8:10])
            m = int(value[5:7])
            y = int(value[0:4])           
        else:
            return False 
    
        if d < 1 or d > 31:
            return False
        if m < 1 or m > 12: 
            return False
        if m in [4, 6, 9, 11] and d > 30: 
            return False
        if m == 2:
            if d > 29: 
                return False
            if d == 29 and y % 4 > 0: 
                return False
    
        return True

    # Formato (tempo): hh:mm:ss
    def time_validator(self, value):
        r = '^[0-9]{2}:[0-9]{2}:[0-9]{2}$'
        if not re.search(r, value):
            return False 
        h = int(value[0:2])
        m = int(value[3:5])
        s = int(value[6:8])
        if h < 0 or h > 23: 
            return False
        if m < 0 or m > 59: 
            return False
        if s < 0 or s > 59: 
            return False
        return True

#
class Form_Validator:
    #
    def __init__(self):
        pass

# Date (e orari)

    # pars[0] = mode (it|eng|iso)
    def isDate(self, value, pars):
        dtm = DT_Manager()
        return dtm.date_validator(value, pars[0])

    # pars[0] = mode (it|eng|iso)
    def isDateTime(self, value, pars):
        dtm = DT_Manager()
        date = value[0:10]
        time = value[11:19]

        if not dtm.date_validator(date, pars[0]):
            return False
        if not dtm.time_validator(time):
            return False
        return True

    # 
    def isTime(self, value, pars):
        dtm = DT_Manager()
        if not dtm.time_validator(value):
            return False
        return True

    # pars = mode (it|eng|iso), from (date; iso mode), to (date; iso mode)
    def isDateInRange(self, value, pars=["","",""]):
        dtm = DT_Manager()
        if not dtm.date_validator(value, pars[0]): 
            return False

        v = dtm.dateConvert(value, pars[0], 'iso')

        date1 = int(pars[1][0:4] + pars[1][5:7] + pars[1][8:10])
        date2 = int(pars[2][0:4] + pars[2][5:7] + pars[2][8:10])
        dateV = int(v[0:4] + v[5:7] + v[8:10])

        if dateV >= date1 and dateV <= date2:
            return True
        return False 

    # pars = from (time; iso mode), to (time; iso mode)
    def isTimeInRange(self, value, pars=["","",""]):
        dtm = DT_Manager()
        if not dtm.time_validator(value):
            return False

        time1 = int(pars[0][0:2]) * 3600 + int(pars[0][3:5]) * 60 + int(pars[0][6:8])
        time2 = int(pars[1][0:2]) * 3600 + int(pars[1][3:5]) * 60 + int(pars[1][6:8])
        timeV = int(value[0:2]) * 3600 + int(value[3:5]) * 60 + int(value[6:8])

        if timeV >= time1 and timeV <= time2:
            return True
        return False 

# Booleani

    #
    def isBool(self, value, pars):
        if str(value) == '0' or str(value) == '1':
            return True
        return False

# Numeri

    #
    def isDecimal(self, value, pars):
        value = str(value)
        # -1.0, 10.52, ...
        r = '(^\-{0,1}0{1}\.[0-9]+$)|(^\-{0,1}[1-9]+[0-9]*\.[0-9]+$)'
        if re.search(r, value):
            return True
        return False 

    #
    def isEuroMoney(self, value, pars):
        value = str(value)
        # 0.00, 1.20, 19.50, ...
        r = '(^0{1}\.[0-9]{2}$)|(^[1-9]+[0-9]*\.[0-9]{2}$)'
        if re.search(r, value):
            return True
        return False  

    #
    def isHexValue(self, value, pars):
        # #fa0 OR #99ffaa
        r = '^#?([a-f0-9]{6}|[a-f0-9]{3})$'
        if re.search(r, value):
            return True
        return False 

    #
    def isInteger(self, value, pars):
        value = str(value)
        # 0, 1, -2, -123, 456, ...
        r = '(^0$)|(^\-[1-9]+[0-9]*$)|(^[1-9]+[0-9]*$)'
        if re.search(r, value):
            return True
        return False 

    #
    def isNegativeInt(self, value, pars):
        value = str(value)
        # -1, -10, -123, ...
        r = '^\-[1-9]+[0-9]*$'
        if re.search(r, value):
            return True
        return False 

    #
    def isPositiveInt(self, value, pars):
        value = str(value)
        # 1, 10, 123, ...
        r = '^[1-9]+[0-9]*$'
        if re.search(r, value):
            return True
        return False 

    #
    def isZeroNegativeInt(self, value, pars):
        value = str(value)
        # 0, -1, -10, -123, ...
        r = '(^[0]{1}$)|(^\-[1-9]+[0-9]*$)'
        if re.search(r, value):
            return True
        return False 

    #
    def isZeroPositiveInt(self, value, pars):
        value = str(value)
        # 0, 1, 10, 123, ...
        r = '(^[0]{1}$)|(^[1-9]+[0-9]*$)'
        if re.search(r, value):
            return True
        return False 

# Comparazione

    #
    def isDecimalInRange(self, value, pars=[0,0]):
        if float(value) >= pars[0] and float(value) <= pars[1]:
             return True
        return False

    #
    def isIntInRange(self, value, pars=[0,0]):
        if int(value) >= pars[0] and int(value) <= pars[1]:
            return True
        return False

    #
    def isLower(self, value, pars=[0]):
        if float(value) < pars[0]:
            return True
        return False 

    #
    def isLowerEqual(self, value, pars=[0]):
        if float(value) <= pars[0]:
            return True
        return False

    #
    def isGreater(self, value, pars=[0]):
        if float(value) > pars[0]:
            return True
        return False

    #
    def isGreaterEqual(self, value, pars=[0]):
        if float(value) >= pars[0]:
            return True
        return False

# Stringhe

    #
    def allowedChars(self, value, pars):
        if len(value) == 0:
            return True
        r = '^[' + pars[0] + ']*$'
        if re.search(r, value):
            return True
        return False

    #
    def forbiddenChars(self, value, pars):
        if len(value) == 0:
            return True
        r = '^[^' + pars[0] + ']*$'
        if re.search(r, value):
            return True
        return False

    #
    def isStringEqual(self, value, pars):
        if value == pars[0]:
            return True
        return False 

    #
    def isLength(self, value, pars=[0]):
        if len(value) == pars[0]:
            return True
        return False 

    #
    def isLengthInRange(self, value, pars=[0,0]):
        if len(value) >= pars[0] and len(value) <= pars[1]:
            return True
        return False

    #
    def isMaxLength(self, value, pars=[0]):
        if len(value) <= pars[0]:
            return True
        return False  

    #
    def isMinLength(self, value, pars=[0]):
        if len(value) >= pars[0]:
            return True
        return False 

    #
    def isPassword(self, value, pars):
        mode = {}
        # https:#stackoverflow.com/questions/19605150/regex-for-password-must-contain-at-least-eight-characters-at-least-one-number-a
        # A
        # Minimum eight characters, at least one letter and one number:
        mode['A'] = "^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$";
        # B
        # Minimum eight characters, at least one letter, one number and one special character:
        mode['B'] = "^(?=.*[A-Za-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,}$";
        # C
        # Minimum eight characters, at least one uppercase letter, one lowercase letter and one number:
        mode['C'] = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$";
        # D
        # Minimum eight characters, at least one uppercase letter, one lowercase letter, one number and one special character:
        mode['D'] = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$";
        #
        value = str(value)
        r = mode[ pars[0] ]
        if re.search(r, value):
            return True
        return False 

    #
    def isRegex(self, value, pars):
        if re.search(pars[0], value):
            return True
        return False

# Internet

    #
    def isEmail(self, value, pars):
        r = '^[-0-9a-zA-Z.+_]+@[-0-9a-zA-Z.+_]+\.[a-zA-Z]{2,}$'
        if re.search(r, value):
            return True
        return False

    #
    def isIPV4(self, value, pars):
        r = '^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$'
        if re.search(r, value):
            return True
        return False

    #
    def isURL(self, value, pars):
        r = '^(https?:\/\/)?([\da-zA-Z\.-]+)\.([a-zA-Z\.]{2,6})([\/\w\.-]*)*\/?$'
        if re.search(r, value):
            return True
        return False

# Altro
        
    #
    def isInSet(self, value, pars):
        if value in pars:
            return True
        return False 

    # http:#www.icosaedro.it/cf-pi/vedi-codice.cgi?f=cf-php.txt

    def isCodiceFiscale(self, value, pars):
        r = '/^[0-9A-Z]{16}\$/sD'
        if not re.search(r, value):
            return False
        s = 0
        even_map = "BAFHJNPRTVCESULDGIMOQKWZYX"

        i = 0
        while i < 15:
            c = value[i]
            if c in ['0','1','2','3','4','5','6','7','8','9']:
                n = ord(c) - ord("0")
            else:
                n = ord(c) - ord("A")
            if i & 1 == 0:
                n = ord(even_map[n]) - ord("A")
            s += n
            if s % 26 + ord("A") != ord(value[15]):
                return False
            i += 1
        return True