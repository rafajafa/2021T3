def check_password(password):
    '''
    Takes in a password, and returns a string based on the strength of that password.

    The returned value should be:
    * "Strong password", if at least 12 characters, contains at least one number, at least one uppercase letter, at least one lowercase letter.
    * "Moderate password", if at least 8 characters, contains at least one number.
    * "Poor password", for anything else
    * "Horrible password", if the user enters "password", "iloveyou", or "123456"
    ''' 
    strong = "Strong password"
    mod = "Moderate password"
    poor = "Poor password"
    hor = "Horrible password"

    if password == "password" or password == "iloveyou" or password == "123456":
        return hor
    elif len(password) >= 12 and any(chr.isdigit() for chr in password) and any(chr.isupper() for chr in password) and any(chr.islower() for chr in password):
        return strong
    elif len(password) >= 8 and any(chr.isdigit() for chr in password):
        return mod
    else:
        return poor



if __name__ == '__main__':
    print(check_password("ihearttrimesters"))
    # What does this do? should return poor
    print(check_password("Orangeisawesome123"))
    
