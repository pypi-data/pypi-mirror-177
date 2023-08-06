import click
import six
import dbs
import datetime

from pytz import utc
from pyfiglet import figlet_format
from configstore import ConfigStore
from PyInquirer import Token, prompt, style_from_dict
from dbscli.validators import EmailValidator, PasswordValidator, ApiKeyValidator


try:
    import colorama
    colorama.init()
except ImportError:
    colorama = None

try:
    from termcolor import colored
except ImportError:
    colored = None


conf = ConfigStore("dbs-cli")

style = style_from_dict({
    Token.QuestionMark: '#fac731 bold',
    Token.Answer: '#4688f1 bold',
    Token.Instruction: '',
    Token.Separator: '#cc5454',
    Token.Selected: '#0abf5b',
    Token.Pointer: '#673ab7 bold',
    Token.Question: '',
})


def log(string, color, font="slant", figlet=False):
    if colored:
        if not figlet:
            six.print_(colored(string, color))
        else:
            six.print_(colored(figlet_format(string, font=font), color))
    else:
        six.print_(string)


def ask_account():
    questions = [
        {
            'type': 'input',
            'name': 'account',
            'message': 'Enter DeepNatural account (email address)',
            'validate': EmailValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


def ask_password():
    questions = [
        {
            'type': 'password',
            'name': 'password',
            'message': 'Enter DeepNatural password',
            'validate': PasswordValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


def ask_team_id():
    questions = [
        {
            'type': 'input',
            'name': 'team_id',
            'message': 'Enter DeepNatural Team ID (Only needed to provide once)',
            'validate': TeamIdValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


def ask_api_key():
    questions = [
        {
            'type': 'input',
            'name': 'api_key',
            'message': 'Enter DeepNatural API Key (Only needed to provide once)',
            'validate': ApiKeyValidator,
        },
    ]
    answers = prompt(questions, style=style)
    return answers


@click.group()
def cli():
    """
    CLI for DeepNatural Brain Services
    """
    log("DeepNatural Brain Services", color="blue", figlet=True)
    log("Welcome to DBS CLI", "green")


@cli.command()
def init():
    conf.clear()
    try:
        api_key = conf.get("api_key")
    except KeyError:
        api_key = ask_api_key()
        conf.set(api_key)

    log(f" - Team ID: {conf.get('team_id')}", color='white')
    log(f" - Team Name: {conf.get('team_name')}", color='white')
    log(f" - Team API Key: {conf.get('api_key')[:4] + '*' * 20}", color='white')


# @cli.command()
def account():
    try:
        account = conf.get("account")
        expires_at = datetime.datetime.fromisoformat(conf.get('expires_at'))
        if expires_at < utc.localize(datetime.datetime.utcnow()) - datetime.timedelta(seconds=60):
            r = dbs.auth.refresh_token(conf.get("refresh_token"))
            r['expires_at'] = (utc.localize(datetime.datetime.utcnow()) + datetime.timedelta(seconds=r['expires_in'])).isoformat()
            conf.set(r)
        r = dbs.auth.get_user_profile(conf.get("access_token"))
    except KeyError:
        account = ask_account()
        conf.set(account)
        password = ask_password()

    log(f" - Account: {conf.get('account')}", color='white')


@cli.command()
def text_classification():
    pass


if __name__ == '__main__':
    cli()
