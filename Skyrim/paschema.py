import re
from marshmallow import Schema, fields, validate, ValidationError
from pacrypto import EncryptPassword, \
                     VerifyPassword


class UserSchema(Schema):
     def validate_Data(new_user, **kwargs):

         #validate format for first name
          match = re.search("[A-Za-z]", new_user["Fname"])
          if match:
               capF = new_user["Fname"].capitalize();
               new_user.update({'Fname' : capF})
          else:
               raise ValidationError("Incorrect values for first name")

          #validate format for last name
          match = re.search("[A-Za-z]", new_user["Lname"])
          if match:
              capL = new_user["Lname"].capitalize();
              new_user.update({'Lname' : capL})
          else:
               raise ValidationError("Incorrect values for last name")

          #validate format for birthdate date 00/00/0000
          match = re.search("^(\d{2})[-/]?(\d{2})[-/]?(\d{4})$", new_user["Birthdate"])
          if match:
               newDate = ("{}/{}/{}".format(match.group(1),match.group(2),match.group(3)))
               new_user.update({'Birthdate' : newDate})
          else:
               raise ValidationError("Incorrect birthdate formatting.")

          #validate format for phone number 000-000-0000
          match = re.search("^\(?(\d{3})\)?\-?(\d{3})\-?(\d{4})$", new_user["Phone"])
          if match:
               newNum = ("({})-{}-{}".format(match.group(1),match.group(2),match.group(3)))
               new_user.update({'Phone' : newNum})
          else:
               raise ValidationError("Incorrect phone number formatting.")

          #validate username format
          match = re.search("[a-zA-Z0-9]", new_user["Username"])
          if not match:
               raise ValidationError("Incorrect username formatting.")

          #TODO check to see if username already exists

          #validate password format and hash it
          match = re.search("[a-zA-Z0-9_]", new_user["Password"])
          if match:
              hashedPassword = EncryptPassword(new_user["Password"])
              new_user.update({'Password' : hashedPassword})
          else:
               raise ValidationError("Not a valid password")

          
          return new_user

     #Define the schema 
     Fname = fields.String(validate=validate.Length(min=2, max=12),required=True)
     Lname = fields.String(validate=validate.Length(min=2, max=12),required=True)
     Birthdate = fields.String(required=True)
     Email = fields.Email(required=True)
     Phone = fields.String(required=True)
     League = fields.Boolean(required=True)
     Username = fields.String(validate=validate.Length(min=3, max=12),required=True)
     Password = fields.String(validate=validate.Length(min=6, max=12),required=True)
     Token = fields.String(required=True)
     Points = fields.Integer(required=True)
