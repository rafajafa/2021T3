part 1:
    There are three part of the jwt seperate in dot point but they are all random upper and lower case letters and number. 
part 2:
    The payload has been tampered as the secret doesnot match and fail to decode. 
    Using jwt.io, we can see that when we try to use 'comp1531' as the secret in the verify signature, it said invalid signature.
    the correct payload should be:
    'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1X2lkIjoiMTIzNDUifQ.MByA9mwoKP56SQUi1S-bjzNpRsvHWS7oEIewq-8qVuU'1