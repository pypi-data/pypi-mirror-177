from random import randint

class abn: #Source: https://abr.business.gov.au/Help/AbnFormat   
    weighting = [10,1,3,5,7,9,11,13,15,17,19]
    
    def __init__ (self) -> None:
        pass
        
    def validate (number):
        def is_number (number):
            try:
                int(number)
            except:
                return False
            return True
    
        def len_number(number):
            stringNumber = str(number)
            if len(stringNumber) != 11:
                return False
            return True
        
        def sum_remainder (number):
            number = int(number)
            number = number - 10_000_000_000
            number = str(number)
            i = 0
            total = 0
            for element in number:
                element = int(element)
                total += element * abn.weighting[i]
                i+=1
            return total

        if is_number (number) is False or len_number (number) is False:
            return False
        else:
            remainder = sum_remainder (number) % 89
            if remainder == 0:
                return True
            else:
                return False
            
    def generate ():
        while True:
            number = randint(10_000_000_000, 99_999_999_999)
            if abn.validate (number) is True:
                return str(number)
            else:
                continue

class acn: #Source: https://asic.gov.au/for-business/registering-a-company/steps-to-register-a-company/australian-company-numbers/australian-company-number-digit-check/
    weighting = [8,7,6,5,4,3,2,1]
    def __init__ (self) -> None:
        pass
    
    def validate (number):
        def is_number (number):
            try:
                int(number)
            except:
                return False
            return True
    
        def len_number(number):
            stringNumber = str(number)
            if len(stringNumber) != 9:
                return False
            return True
        
        def sum_remainder (number):
            number = str(number)
            i = 0
            total = 0
            for element in number:
                try:
                    acn.weighting[i]
                except:
                    break
                element = int(element)
                total += element * acn.weighting[i]
                i+=1
            return total

        checkDigit = (str(number))[-1]
        if is_number (number) is False or len_number (number) is False:
            return False
        else:
            remainderDeductByTen = 10 - (sum_remainder (number) % 10)
            if remainderDeductByTen == int(checkDigit):
                return True
            else:
                return False
            
    def generate ():
        while True:
            number = randint(100_000_000, 999_999_999)
            if acn.validate (number) is True:
                return str(number)
            else:
                continue

class tfn:
    weighting = [1,4,3,7,5,8,6,9,10]

    def __init__(self) -> None:
        pass

    def validate (number):
        def is_number (number):
            try:
                int(number)
            except:
                return False
            return True
    
        def len_number(number):
            stringNumber = str(number)
            if len(stringNumber) != 9:
                return False
            return True
        
        def sum_remainder (number):
            number = str(number)
            i = 0
            total = 0
            for element in number:
                try:
                    tfn.weighting[i]
                except:
                    break
                element = int(element)
                total += element * tfn.weighting[i]
                i+=1
            return total

        if is_number (number) is False or len_number (number) is False:
            return False
        else:
            sumAllNum = sum_remainder (number) 
            if sumAllNum % 11 == 0:
                return True
            else:
                return False
            
    def generate ():
        while True:
            number = randint(100_000_000, 999_999_999)
            if tfn.validate (number) is True:
                return str(number)
            else:
                continue
