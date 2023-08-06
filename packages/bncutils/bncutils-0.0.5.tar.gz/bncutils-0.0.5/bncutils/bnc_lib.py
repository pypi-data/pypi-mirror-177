from secrets import choice
from itertools import permutations
import random
import datetime as dt
import base64
import os
import sys
from pathlib import Path

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import yaml
from yaml.loader import SafeLoader


def base64_decode_(encoded_string):
    return base64.b64decode(encoded_string.encode("ascii")).decode("ascii")


def get_my_first_guess(capacity: int, guess='') -> str:
    new_guess = ''
    while len(new_guess) < capacity:
        c = str(random.randint(0, 9))
        if (not (c in guess)) and (not (c in new_guess)):
            new_guess += c
    return new_guess


def think_of_number_for_you(capacity):
    return "".join(choice(list(permutations("0123456789", capacity))))


def make_my_guess(game):
    """
    The method figures out my next guess proposal based on number
    of cows and bulls that were given by you (user) for my current guess proposal.
    :param game
    :return: - True if the original number is guessed my me (by the script), i.e.
                    my_cows == my_bulls == capacity. So I am a winner.
             - False if everything is OK, and so we can proceed the game to the next iteration.
                    I calculate the next guess proposal based on my_cows and my_bulls.
             - FinishedNotOKException raised if you have misled me during previous game iteration
             by providing of wrong cows and/or bulls. In this case game
             has become inconsistent, so I cannot guess your number, and so I have to finish the game.
    """

    def populate_template(a, b):
        """
        The method replace a vacant place (letter 'V') in 'a' agrument (a template) with a digit from
        b argument consequently. So it makes one possible guess number for guess numbers set.
        :param a: a template with 'V's and digits from the guess number
        :param b: digits which will be put instead of 'V'
        :return: one possible guess number for guess numbers set
        """
        list0 = list(a)
        list1 = []
        list1.extend(b)
        while list0.count('V'):
            list0[list0.index('V')] = list1.pop()
        return "".join(list0)

    capacity = game.capacity
    my_cows = game.my_cows
    my_bulls = game.my_bulls
    my_guess = game.my_guess
    game.my_history_list.append((my_guess, str(my_cows), str(my_bulls)))
    if my_cows == capacity and my_bulls == capacity:
        return True
    if my_cows == 0 and my_bulls == 0:
        for a in my_guess:
            game.available_digits_str = game.available_digits_str.replace(a, '')
        if len(game.total_set) > 0:
            for c in list(game.total_set):
                for cc in game.my_guess:
                    if cc in c:
                        game.total_set.remove(c)
                        break
            if len(game.total_set) == 0:
                raise FinishedNotOKException
            game.my_guess = choice(tuple(game.total_set))
        else:
            game.my_guess = get_my_first_guess(capacity, my_guess)
        game.attempts += 1
        return False
    templates_set = get_templates(my_cows, my_bulls, my_guess, capacity)
    if my_cows == capacity:
        lst = ["".join(x) for x in templates_set]
    else:
        items_for_templates = get_items_for_templates(my_cows, my_guess, capacity, game.available_digits_str)
        lst = [populate_template(a, b) for a in templates_set for b in items_for_templates]
    current_set = set(lst)
    if len(game.total_set) > 0:
        game.total_set = game.total_set & current_set
    else:
        game.total_set = current_set.copy()
    if len(game.total_set) == 0:
        raise FinishedNotOKException
    game.my_guess = choice(tuple(game.total_set))
    game.attempts += 1
    return False


def overlap_set_items(a0, a1):
    lst = []
    for x in zip(a0, a1):
        if x[0].isnumeric() and x[1].isnumeric():
            return None
        lst.append(x[0] if x[0].isnumeric() else x[1])
    digits = list(filter(lambda e: e.isnumeric(), lst))
    if len(digits) != len(set(digits)):
        return None
    else:
        return tuple(lst)


def overlap_sets(set0, set1, iteration):
    total = set()
    while iteration > 0:
        total.clear()
        sss = (overlap_set_items(a, b) for a in set0 for b in set1)
        total = set(sss)
        total.discard(None)
        # total = set(filter(lambda s: s is not None, sss))
        set1 = total.copy()
        iteration -= 1
    return total


def get_items_for_templates(cows, guess, capacity, init_rest_str="0123456789"):
    items_for_templates = []
    for a in guess:
        init_rest_str = init_rest_str.replace(a, '')
    if capacity - cows > 0:
        for l in permutations(init_rest_str, capacity - cows):
            items_for_templates.append(''.join(map(str, l)))
    return items_for_templates


def get_templates(cows, bulls, current_guess, capacity):
    only_bulls_set = set()
    one_cow_set = set()
    total = set()
    if cows == bulls:
        bulls_permut = set(map(tuple, map(sorted, permutations(range(len(current_guess)), cows))))
        for i0 in bulls_permut:
            temp = ["V" for _ in range(capacity)]
            for i1 in i0:
                temp[i1] = current_guess[i1]
            only_bulls_set.add(tuple(temp))
        total = only_bulls_set.copy()
    else:
        for i0 in range(capacity):
            temp = ["V" for _ in range(capacity)]
            for i1, c1 in enumerate(current_guess):
                if i1 == i0:
                    continue
                temp[i0] = c1
                one_cow_set.add(tuple(temp))
        if cows - bulls == 1:
            total = one_cow_set.copy()
        else:
            total = overlap_sets(one_cow_set, one_cow_set, cows - bulls - 1)
        if bulls > 0:
            bulls_permut = set(map(tuple, map(sorted, permutations(range(len(current_guess)), bulls))))
            for i0 in bulls_permut:
                temp = ["V" for _ in range(capacity)]
                for i1 in i0:
                    temp[i1] = current_guess[i1]
                only_bulls_set.add(tuple(temp))
            total = overlap_sets(only_bulls_set, total, 1)
    return total


def validate_cows_and_bulls(cows_raw, bulls_raw, capacity):
    errors_dict = {}
    if not cows_raw.isdigit():
        errors_dict["my_cows"] = "Number of cows must be a digit."
    if not bulls_raw.isdigit():
        errors_dict["my_bulls"] = "Number of bulls must be a digit."
    if len(errors_dict) > 0:
        raise BnCException(errors_dict)
    cows = int(cows_raw)
    bulls = int(bulls_raw)
    if cows > capacity:
        errors_dict["my_cows"] = "Number of cows cannot be more than the capacity (" + str(capacity) + ")."
    if bulls > capacity:
        errors_dict["my_bulls"] = "Number of bulls cannot be more than the capacity (" + str(capacity) + ")."
    if len(errors_dict) > 0:
        raise BnCException(errors_dict)
    if bulls > cows:
        errors_dict["my_bulls"] = "Number of bulls cannot be more than the number of cows."
    if cows == capacity and bulls == capacity - 1:
        errors_dict["my_cows"] = "Erroneous combination of cows and bulls! Try again!"
        errors_dict["my_bulls"] = ""
    if len(errors_dict) > 0:
        raise BnCException(errors_dict)


def validate_your_guess(capacity, input_string):
    errors_dict = {"your_guess": ""}
    if not input_string.isdigit():
        errors_dict["your_guess"] = "Only digits allowed. "
        raise BnCException(errors_dict)
    if len(input_string) != capacity:
        errors_dict["your_guess"] += "Length must be " + str(capacity) + " digits. "
    if len(set(list(input_string))) != len(list(input_string)):
        errors_dict["your_guess"] += "Digits must be unique."
    if len(errors_dict["your_guess"]) > 0:
        raise BnCException(errors_dict)
    return True


def make_your_guess(game, your_guess_string):
    if game.attempts < 1:
        return False
    game.your_cows, game.your_bulls = calc_bulls_and_cows(game.my_number, your_guess_string)
    game.your_history_list.append((str(your_guess_string), str(game.your_cows), str(game.your_bulls)))
    if game.your_cows == game.capacity and game.your_bulls == game.capacity:
        return True
    else:
        return False


def calc_bulls_and_cows(true_number: str, guess_number: str):
    """
    The method calculates a number of cows and a number of bulls based on the true number and a guess number
    :param true_number: string
    :param guess_number: string
    :return: tuple (cows, bulls)
    """
    cows = bulls = 0
    for i0, c0 in enumerate(true_number):
        for i1, c1 in enumerate(guess_number):
            if c0 == c1:
                cows += 1
                if i0 == i1:
                    bulls += 1
                break
    return cows, bulls


def get_data_for_fixture_table(fl_raw_data, get_user_data_function):
    data_for_table = list()
    for row in fl_raw_data:
        username = str(row.username_id)
        user_data = get_user_data_function(username=username)
        first_name = str(user_data.first_name)
        last_name = str(user_data.last_name)
        if int(row.winner) == 1:
            winner = "Me"
        elif int(row.winner) == 2:
            winner = "You"
        else:
            winner = "Tie"
        attempts = int(row.attempts)
        # date = dt.datetime.strftime(row.time,"%Y.%m.%d %H:%M:%S")
        # time_ = row.time.replace(tzinfo=row.time.tzinfo)
        date = f"{row.time.astimezone():%Y.%m.%d %H:%M:%S}"
        duration = str(row.duration) + "min"
        entry = (first_name, last_name, username, winner, attempts, date, duration)
        data_for_table.append(entry)
    return data_for_table


def create_db_user(settings, login_to_create, password_to_create):
    try:
        session = make_db_session(settings)
        engine = session.bind.engine
        if login_to_create != settings["admin_user"]:
            sql_command = f"create user {login_to_create} with " \
                          f"encrypted password '{password_to_create}' in role {settings['common_db_user']}"
        else:
            sql_command = f"create user {login_to_create} with " \
                          f"encrypted password '{password_to_create}' in role {settings['admin_user']}"
        with engine.connect() as con:
            con.execute(sql_command)
    except Exception:
        raise


def modify_db_user(settings, login_to_modify, password_to_modify):
    try:
        session = make_db_session(settings)
        engine = session.bind.engine
        sql_command = f"alter role {login_to_modify} with encrypted password '{password_to_modify}'"

        with engine.connect() as con:
            con.execute(sql_command)
    except Exception:
        raise
    session = make_db_session(settings, login_to_modify, password_to_modify)
    return session


def make_db_session(settings, user=None, password=None):
    user = user or settings["default_db_user"]
    if user == settings["default_db_user"]:
        # password = base64_decode_(settings["default_db_password"])
        password = settings["default_db_password"]
    db_conn_string = settings["db_conn_string_pre"] + str(user) + ":" + str(password) + "@" \
                     + settings["db_socket"] + "/" + settings["db_name"]
    # m = re.search(r":([^/].+)@", DB_CONN_STRING)
    # db_conn_string = DB_CONN_STRING.replace(m.group(1), Game.base64_decode_(m.group(1)))
    try:
        if user != settings["default_db_user"]:
            validate_db_user(settings, user, "other")
        engine = create_engine(db_conn_string)
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        return session
    except Exception:
        raise


def delete_db_user(settings, login_to_delete):
    try:
        session = make_db_session(settings)
        engine = session.bind.engine
        sql_command = f"drop role {login_to_delete}"
        with engine.connect() as con:
            con.execute(sql_command)
    except Exception:
        raise


def validate_db_user(settings, login, op):
    try:
        session = make_db_session(settings)
        engine = session.bind.engine
        sql_command = f"select * from pg_roles where rolname='{login}'"
        with engine.connect() as con:
            result = con.execute(sql_command)
    except Exception:
        raise
    try:
        next(result)
    except StopIteration:
        if op != "create":
            raise BnCException("No such user in the database!")
        return
    if op == "create":
        raise BnCException("The user already exists in the database! "
                           "Ask database administrator to delete him")


def read_config():
    config_file = "bnc_config.yml"
    config_path = os.path.join(Path(__file__).resolve().parent, config_file)
    with open(config_path) as f:
        raw_config = yaml.load(f, Loader=SafeLoader)
    settings = dict()
    # email_messages = dict()
    # email_messages["welcome"] = dict()
    # email_messages["pincode"] = dict()
    settings["default_capacity"] = raw_config["default_capacity"]
    settings["email_messages"] = dict()
    settings["email_messages"]["welcome"] = dict()
    settings["email_messages"]["pincode"] = dict()
    settings["email_messages"]["welcome"]["text"] = raw_config["welcome"]["text"]
    settings["email_messages"]["welcome"]["html"] = raw_config["welcome"]["html"]
    settings["email_messages"]["welcome"]["subject"] = raw_config["welcome"]["subject"]
    settings["email_messages"]["pincode"]["text"] = raw_config["pincode"]["text"]
    settings["email_messages"]["pincode"]["html"] = raw_config["pincode"]["html"]
    settings["email_messages"]["pincode"]["subject"] = raw_config["pincode"]["subject"]
    settings["db_conn_string_pre"] = raw_config["db_connection_string_prefix"]
    settings["db_name"] = raw_config["db_name"]
    settings["default_db_user"] = raw_config["default_db_user"] or os.environ["bnc_default_db_user"]
    settings["default_db_password"] = raw_config["default_db_password"] or os.environ["bnc_default_db_password"]
    settings["common_db_user"] = raw_config["common_db_user"]
    settings["db_socket"] = raw_config["db_socket"]
    settings["admin_user"] = raw_config["admin_user"]
    settings["smtp_address"] = raw_config["smtp_address"]
    settings["bnc_email"] = raw_config["bnc_email"]
    settings["ssl_port"] = raw_config["ssl_port"]
    settings["smtp_password"] = raw_config["smtp_password"] or os.environ["bnc_email_password"]
    # settings["phrases_path"] = raw_config["phrases_path"]
    return settings


def send_email(settings, email, message_type, replace_list):
    # password = base64_decode_(settings["smtp_password"])
    password = settings["smtp_password"]
    smtp_address = settings["smtp_address"]
    ssl_port = settings["ssl_port"]
    email_msg = MIMEMultipart("alternative")
    sender_email = settings["bnc_email"]
    receiver_email = email
    subject = settings["email_messages"][message_type]["subject"]
    email_msg["Subject"] = subject
    email_msg["From"] = sender_email
    email_msg["To"] = receiver_email
    text = settings["email_messages"][message_type]['text']
    html = settings["email_messages"][message_type]['html']
    for e in replace_list:
        text = text.replace(e[0], e[1])
        html = html.replace(e[0], e[1])
    p1 = MIMEText(text, "plain")
    p2 = MIMEText(html, "html")
    email_msg.attach(p1)
    email_msg.attach(p2)
    context = ssl.create_default_context()
    try:
        with smtplib.SMTP_SSL(smtp_address, ssl_port, context=context) as srv:
            srv.login(sender_email, password)
            srv.sendmail(sender_email, receiver_email, email_msg.as_string())
    except Exception:
        raise


def read_phrases():
    phrases_file = "good_phrases"
    phrases_path = os.path.join(Path(__file__).resolve().parent, phrases_file)
    default_phrase = ["I wish you an interesting game!"]
    try:
        with open(Game.phrases_path) as f:
            data = f.read()
    except Exception:
        return default_phrase
    lst = data.split("\n")
    good_phrases = lst if len(lst) else default_phrase
    return [e for e in good_phrases if len(e) < 78] # 78 is a tkinter main window max width now

# def assign_params(cls, function, *args, **kwargs):
#     settings = {}
#     settings = function(*args, **kwargs)
#     for key, value in settings.items():
#         setattr(cls, key, value)


class UserNotFoundException(Exception):
    pass


class InvalidLoginException(Exception):
    def __init__(self, a):
        super().__init__()
        self.msg = "User with this login doesn't exist!" if a else "User with this login already exists!"

    def __repr__(self):
        return "{}".format(self.msg)

    def __str__(self):
        return "{}".format(self.msg)


class FinishedOKException(Exception):
    pass


class FinishedNotOKException(Exception):
    pass


class NoAdminException(Exception):
    pass


class IncorrectPasswordException(Exception):
    def __repr__(self):
        return "Incorrect Password!"

    def __str__(self):
        return "Incorrect Password!"


class IncorrectDBPasswordException(Exception):
    def __repr__(self):
        return "Incorrect DB password for your user! Please ask DB administrator for help."

    def __str__(self):
        return "Incorrect DB password for your user! Please ask DB administrator for help."


class NoPrivilegesException(Exception):
    pass


class BnCException(Exception):
    def __init__(self, msg):
        super().__init__()
        self.msg = msg

    def __add__(self, other):
        if isinstance(self.msg, dict) and isinstance(other.msg, dict):
            temp_dict = self.msg.copy()
            temp_dict.update(other.msg)
            exception = BnCException(temp_dict)
            return exception
        else:
            return self.msg + other.msg

    def __repr__(self):
        return "{}".format(self.msg)

    def __str__(self):
        return "{}".format(self.msg)
