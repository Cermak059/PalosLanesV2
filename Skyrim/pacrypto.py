from passlib.hash import sha256_crypt

#Password hashing method
def EncryptPassword(Password):
    hashedPassword = sha256_crypt.hash(Password)
    return hashedPassword

#Verify stored password with password to be checked
def VerifyPassword(chck_Password, stored_Password):
     return sha256_crypt.verify(chck_Password, stored_Password)

#Taking all uppercase characters A-Z and digits and combining lists
#Picks random item out of list for size times
def GenerateToken(size):
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(size))
