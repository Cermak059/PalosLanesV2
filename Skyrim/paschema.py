import re
from marshmallow import Schema, fields, validate, ValidationError
from pacrypto import EncryptPassword, \
                     VerifyPassword


class UserSchema(Schema):
     def validate_Data(users, **kwargs):

         #validate format for first name
          match = re.search("^[A-Z]{1}[a-z]", users["Fname"])
          if not match:
               raise ValidationError("Incorrect values for first name")

          #TODO eliminate capitals in middle of string

          #validate format for last name
          match = re.search("^[A-Z]{1}[a-z]", users["Lname"])
          if not match:
               raise ValidationError("Incorrect values for last name")

          #TODO eliminate capitals in middle of string

          #validate format for birthdate date 00/00/0000
          match = re.search("^(\d{2})\/(\d{2})\/(\d{4})$", users["Birthdate"])
          if match:
               newDate = ("{}/{}/{}".format(match.group(1),match.group(2),match.group(3)))
               users.update({'Birthdate' : newDate})
          else:
               raise ValidationError("Incorrect birthdate formatting.")

          #validate format for phone number 000-000-0000
          match = re.search("^\(?(\d{3})\)?\-?(\d{3})\-?(\d{4})$", users["Phone"])
          if match:
               newNum = ("({})-{}-{}".format(match.group(1),match.group(2),match.group(3)))
               users.update({'Phone' : newNum})
          else:
               raise ValidationError("Incorrect phone number formatting.")

          #validate username format
          match = re.search("[a-zA-Z0-9]", users["Username"])
          if not match:
               raise ValidationError("Incorrect username formatting.")

          #TODO check to see if username already exists

          #validate password format and hash it
          match = re.search("[a-zA-Z0-9_]", users["Password"])
          if match:
              hashedPassword = EncryptPassword(users["Password"])
              users.update({'Password' : hashedPassword})
          else:
               raise ValidationError("Not a valid password")

          
          return users

     #Define the schema with parameters for new user registry
     Fname = fields.String(validate=validate.Length(min=2, max=12),required=True)
     Lname = fields.String(validate=validate.Length(min=2, max=12),required=True)
     Birthdate = fields.String(required=True)
     Email = fields.Email(required=True)
     Phone = fields.String(required=True)
     League = fields.Boolean(required=True)
     Username = fields.String(validate=validate.Length(min=3, max=12),required=True)
     Password = fields.String(validate=validate.Length(min=6, max=12),required=True)
