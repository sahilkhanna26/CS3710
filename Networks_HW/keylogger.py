from pynput import keyboard


comp_string = ""

def on_press(key):
    global comp_string


    try:
        comp_string = comp_string + key.char
        # print("string", comp_string)
        if("mst3k" in comp_string):
            # print(comp_string)
            # print("success")
            if(len(comp_string) == 15):
                # print("password", comp_string[5:15])
                pword = comp_string[5:15]
                pword = "{"+pword+"}"
                print(pword)
                comp_string =""



        elif(comp_string[len(comp_string)-1] != 'm' and comp_string[len(comp_string)-1]!= 's' and comp_string[len(comp_string)-1]!= 't' and comp_string[len(comp_string)-1]!= '3' and comp_string[len(comp_string)-1]!= 'k'):

            # print(comp_string)
            comp_string = ""

            # print('alphanumeric key {0} pressed'.format(
            #     key.char))
        else:
            pass





    except AttributeError:
        pass

def on_release(key):
    # print('{0} released'.format(
    #     key))
    if key == keyboard.Key.esc:
        # Stop listener
        return False

# Collect events until released
with keyboard.Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()

# ...or, in a non-blocking fashion:
listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()