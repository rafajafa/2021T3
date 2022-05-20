import jwt
SECRET = 'comp1531'

def decode_jwt():
    jwt = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTIzNDUifQ.lBTAPFU1xxDAi2Vrusfo67ypBai0vBr6O7KOt6CJf1s'
    print(jwt.decode(jwt, SECRET, algorithms = ['HS256']))
    
