import os
import re
import dbs
import datetime


from pytz import utc
from PyInquirer import Validator, ValidationError
from configstore import ConfigStore


conf = ConfigStore("dbs-cli")


class EmailValidator(Validator):
    pattern = r"\"?([-a-zA-Z0-9.`?{}]+@\w+\.\w+)\"?"

    def validate(self, email):
        if len(email.text):
            if re.match(self.pattern, email.text):
                return True
            else:
                raise ValidationError(
                    message="Invalid email",
                    cursor_position=len(email.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(email.text))


class EmptyValidator(Validator):
    def validate(self, value):
        if len(value.text):
            return True
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))


class FilePathValidator(Validator):
    def validate(self, value):
        if len(value.text):
            if os.path.isfile(value.text):
                return True
            else:
                raise ValidationError(
                    message="File not found",
                    cursor_position=len(value.text))
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))


class PasswordValidator(Validator):
    def validate(self, value):
        if len(value.text):
            username = conf.get("account")
            try:
                r = dbs.auth.get_token(username=username, password=value.text)
                r['expires_at'] = (utc.localize(datetime.datetime.utcnow()) + datetime.timedelta(seconds=r['expires_in'])).isoformat()
                conf.set(r)
            except:
                raise ValidationError(
                    message="Invalid account or password",
                    cursor_position=len(value.text))
            return True
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))


class ApiKeyValidator(Validator):
    def validate(self, value):
        if len(value.text):
            try:
                r = dbs.team.get_team_detail(api_key=value.text)
                conf.set('team_id', r.get('team_uid', ''))
                conf.set('team_name', r.get('name', ''))
                conf.set('team_description', r.get('description', ''))
            except:
                raise ValidationError(
                    message="There is an error with the API Key!",
                    cursor_position=len(value.text))
            return True
        else:
            raise ValidationError(
                message="You can't leave this blank",
                cursor_position=len(value.text))
