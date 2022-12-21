import ast
import datetime
import mimetypes
import os
import smtplib
import sys

from email.message import EmailMessage
from email.utils import formatdate


def parse(message, *items):
    def validate(address):
        if not isinstance(address.op, ast.MatMult) or not isinstance(address.right, ast.Attribute):
            raise AttributeError

        return ''.join(ast.unparse(address).split())

    def vali_date(date):
        if not isinstance(date.op, ast.Div) or not isinstance(date.left.op, ast.Div):
            raise AttributeError

        return ''.join(ast.unparse(date).split())

    email = EmailMessage()

    headers, attachments = {}, []
    for item in items:
        key, value = item.optional_vars.id, item.context_expr

        if key == "attachment":
            attachments.append(value)
        elif key == "recipient":
            headers[key] = headers.get(key, []) + [value]
        else:
            headers[key] = value

    try:
        email['From'] = validate(headers["sender"])
    except KeyError:
        raise ValueError("Sender not specified")
    except AttributeError:
        raise SyntaxError("Please enter a valid email address")

    try:
        email['To'] = [*map(validate, headers["recipient"])]
    except KeyError:
        raise ValueError("Recipient not specified")
    except AttributeError:
        raise SyntaxError("Please enter a valid email address")

    try:
        email['Subject'] = eval(ast.unparse(headers["subject"]))
    except KeyError:
        raise ValueError("Subject not specified")
    except AttributeError:
        raise ValueError("Subject not specified")

    try:
        email['Date'] = formatdate(datetime.datetime.strptime(vali_date(headers["date"]),
                                                              "%m/%d/%Y").timestamp(),
                                   localtime=True)
    except KeyError:
        email['Date'] = formatdate(localtime=True)
    except AttributeError:
        raise SyntaxError("Please enter a date")

    email.set_content(eval(ast.unparse(message)))

    for attachment in attachments:
        filename = ''.join(ast.unparse(attachment))
        path = os.path.join(os.curdir, filename)

        filetype, encoding = mimetypes.guess_type(path)
        if filetype is None or encoding is not None:
            filetype = 'application/octet-stream'

        maintype, subtype = filetype.split('/', 1)
        with open(path, 'rb') as file:
            email.add_attachment(file.read(),
                                 maintype=maintype,
                                 subtype=subtype,
                                 filename=filename)

    return email


class BushelServer(smtplib.SMTP):
    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not NameError and exc_type is not TypeError:
            return False

        with open(sys.argv[0]) as current:
            components = [*filter(lambda node: isinstance(node, ast.With),
                                  ast.iter_child_nodes(ast.parse(current.read())))][-1]

        email = parse(components.body[0], *components.items)
        self.sendmail(email['From'], email['To'], email.as_string())

        print(f"Email sent to {email['To']}.")
        return True


__all__ = ["BushelServer"]
