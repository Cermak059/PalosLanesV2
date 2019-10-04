from passlib.hash import sha256_crypt

#Password hashing method
def EncryptPassword(Password):
    hashedPassword = sha256_crypt.hash(Password)
    return hashedPassword

#Verify stored password with password to be checked
def VerifyPassword(chck_Password, stored_Password):
     return sha256_crypt.verify(chck_Password, stored_Password)
