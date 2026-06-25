
"""
Copyright 2026 PySimpleGUI. All rights reserved.

Licensed under LGPL3
"""
#    ___  ___                     __          ____                       __
#  /'___\/\_ \                   /\ \        /\  _`\                    /\ \
# /\ \__/\//\ \      __      ____\ \ \___    \ \ \/\_\     __     _ __  \_\ \    ____
# \ \ ,__\ \ \ \   /'__`\   /',__\\ \  _ `\   \ \ \/_/_  /'__`\  /\`'__\/'_` \  /',__\
#  \ \ \_/  \_\ \_/\ \L\.\_/\__, `\\ \ \ \ \   \ \ \L\ \/\ \L\.\_\ \ \//\ \L\ \/\__, `\
#   \ \_\   /\____\ \__/.\_\/\____/ \ \_\ \_\   \ \____/\ \__/.\_\\ \_\\ \___,_\/\____/
#    \/_/   \/____/\/__/\/_/\/___/   \/_/\/_/    \/___/  \/__/\/_/ \/_/ \/__,_ /\/___/


import PySimpleGUI as sg
from pathlib import Path
from typing import List, Tuple
from random import randint

version = '6.0'
__version__ = version.split()[0]

"""
Changelog since last major release

6.0     24-Jun-2026     Initial release     

"""

class Flashcard:
    def __init__(self, filename, image, answer):
        self.filename = filename
        self.image = image
        self.answer = answer


class G:    # Globals hack
    time_per_card = 0
    answer_delay_time = 0
    show_answer = False
    random_order = False
    number_of_cards = 0
    paused = True

# --------------------------------- LOAD FLASH CARDS---------------------------------


def load_flashcards(flashcards_file):

    inversions_folder = Path(__file__).resolve().parent.parent / "flashcards" / "inversions"
    flashcard_file_path = inversions_folder / flashcards_file
    with open(flashcard_file_path, "r", encoding='utf8') as file:
        lines = file.readlines()

    image_path = inversions_folder
    flashcards: List[Flashcard] = []
    for line in lines:
        file, answer = line.strip().split(',')
        with open(image_path/file, "rb") as image_file:
            image = image_file.read()
        flashcard = Flashcard(file, image, answer)
        flashcards.append(flashcard)

    return flashcards

# --------------------------------- SETTINGS ---------------------------------

def show_settings_window(location:Tuple[int|None, int|None]=(None, None)):
    """
    Shows the settings window

    :param location:        Location of the icon window
    :type location:         Tuple[int, int]
    """

    layout = [#[sg.T('Settings', font='_ 15')],
              [sg.Column([[sg.B(sg.SYMBOL_UP_ARROWHEAD, font='_ 10', p=0, k='-PER CARD UP-')], [sg.B(sg.SYMBOL_DOWN_ARROWHEAD, font='_ 10', p=0,k='-PER CARD DOWN-')]], p=0),
               sg.Input(setting=0, justification='r', s=3, k='-TIME PER CARD-'), sg.T('Seconds to show card')],
              [sg.Checkbox('Show answer before advancing', setting=False, k='-SHOW ANSWER-')],
              [sg.Column([[sg.B(sg.SYMBOL_UP_ARROWHEAD, font='_ 10', p=0, k='-DELAY UP-')], [sg.B(sg.SYMBOL_DOWN_ARROWHEAD, font='_ 10', p=0,k='-DELAY DOWN-')]], p=0),
               sg.Input(setting=0, justification='r', s=3, k='-ANSWER DELAY TIME-'), sg.T('Seconds to show answer before advance')],
              [sg.Checkbox('Order randomly', setting=False, k='-RANDOM-')],
              [sg.Push(), sg.OK(), sg.Cancel()]]

    window = sg.Window('Settings', layout, location=location, keep_on_top=True, font='_ 18', use_custom_titlebar=True)

    while True:
        event, values = window.read()
        # print(event, values)
        if event in (sg.WIN_CLOSED, 'Cancel', 'Exit'):
            break

        try:
            delay = float(values['-ANSWER DELAY TIME-'])
        except:
            delay = 0
        try:
            per_card = float(values['-TIME PER CARD-'])
        except:
            per_card = 0

        if event == 'OK':
            window.settings_save(values)
            # G.show_answer = values['-SHOW ANSWER-']
            # G.random_order = values['-RANDOM-']
            # G.time_per_card = values['-TIME PER CARD-']
            # G.answer_delay_time = values['-ANSWER DELAY TIME-']
            break
        elif event in ('-DELAY UP-','-DELAY DOWN-'):
            inc = +0.5 if event == '-DELAY UP-' else -0.5
            delay += inc
            delay = 0 if delay < 0 else delay
            window['-ANSWER DELAY TIME-'].update(delay)
        elif event in ('-PER CARD UP-','-PER CARD DOWN-'):
            inc = +0.5 if event == '-PER CARD UP-' else -0.5
            per_card += inc
            per_card = 0 if per_card < 0 else per_card
            window['-TIME PER CARD-'].update(per_card)
    window.close()


def load_settings():
    G.show_answer = sg.user_settings_get_entry('-SHOW ANSWER-', False)
    G.random_order = sg.user_settings_get_entry('-RANDOM-', False)
    G.time_per_card = float(sg.user_settings_get_entry('-TIME PER CARD-', 0))
    G.answer_delay_time = float(sg.user_settings_get_entry('-ANSWER DELAY TIME-', 0))


# --------------------------------- NEXT / PREV CARD ---------------------------------


def next_card(card_index):
    if G.random_order:
        card_index = randint(0, G.number_of_cards-1)
    else:
        card_index = (card_index + 1) % G.number_of_cards
    return card_index

def prev_card(card_index):
    return (card_index + (G.number_of_cards - 1)) % G.number_of_cards


'''
M"""""`'"""`YM          oo          
M  mm.  mm.  M                      
M  MMM  MMM  M .d8888b. dP 88d888b. 
M  MMM  MMM  M 88'  `88 88 88'  `88 
M  MMM  MMM  M 88.  .88 88 88    88 
M  MMM  MMM  M `88888P8 dP dP    dP 
MMMMMMMMMMMMMM
'''

# --------------------------------- MAIN ---------------------------------


def main():
    sg.set_options(icon=music_icon)
    # sg.theme_previewer()
    # sg.theme('Dark gray 10')
    flashcards = load_flashcards('inversions.flash')
    G.number_of_cards = len(flashcards)
    # sg.popup_scrolled('\n'.join([f'{c.filename} - {c.answer}'for c in flashcards]), title='Flashcards')
    load_settings()
    # row_len = 6
    # num_images = 36
    # image_grid = [[sg.Image(flashcards[c + j * row_len].image) for c in range(0, row_len)] for j in range(0, num_images // row_len)]

    layout = [[sg.P(), sg.Image(settings_icon, enable_events=True, k='-SETTINGS-')],
              [sg.Image(source=back_icon, enable_events=True, k='-BACK-'), sg.Push(), sg.Image(flashcards[0].image, zoom=3, k='-IMAGE-'), sg.Push(), sg.Image(source=forward_icon,  enable_events=True, k='-FORWARD-')],
              [],
              [sg.P(), sg.Button(size=(10,1), k='-ANSWER-', font='_ 18'), sg.P()],
              [sg.P(),sg.Button(image_source=play_icon, k='-PLAY-', border_width=0, button_color=(sg.theme_button_color_text(), sg.theme_background_color())),
                           sg.Button(image_source=pause_red_icon, k='-PAUSE-', border_width=0, button_color=(sg.theme_button_color_text(), sg.theme_background_color())), sg.P()]]
              # [sg.Push(), sg.Button(sg.SYMBOL_X_SMALL, button_color=(sg.theme_button_color_text(), sg.theme_background_color()), border_width=0, font='_18', k='Exit')]]


    window = sg.Window("Inversions Flashcards", layout, finalize=True, auto_save_location=True, keep_on_top=True, use_custom_titlebar=True)

    card_index = 0

    while True:
        event, values = window.read()
        # print(event, values)
        if event in (sg.WIN_CLOSED, "Exit"):
            break
        elif event == '-FORWARD-':
            if G.show_answer:
                window['-ANSWER-'].update(flashcards[card_index].answer)
                window.timer_start(frequency_ms=G.answer_delay_time*1000, repeating=False, key='-timer forward-')
            else:
                card_index = next_card(card_index)
                window['-ANSWER-'].update('')
                if not G.paused:
                    window.timer_start(G.time_per_card*1000, repeating=False, key='-FORWARD-')
        elif event == '-timer forward-':
            card_index = next_card(card_index)
            if not G.paused:
                window.timer_start(G.time_per_card*1000, repeating=False, key='-FORWARD-')
            window['-ANSWER-'].update('')
        elif event == '-BACK-':
            card_index = prev_card(card_index)
            window['-ANSWER-'].update('')
        elif event == '-ANSWER-':
            window['-ANSWER-'].update(flashcards[card_index].answer)
        elif event == '-SETTINGS-':
            show_settings_window(location=window.current_location())
            load_settings()
        elif event == '-PLAY-':
            window['-PLAY-'].update(image_source=play_red_icon)
            window['-PAUSE-'].update(image_source=pause_icon)
            G.paused = False
            window.timer_stop_all()
            window.timer_start(G.time_per_card*1000, repeating=False, key='-FORWARD-')
        elif event == '-PAUSE-':
            window['-PLAY-'].update(image_source=play_icon)
            window['-PAUSE-'].update(image_source=pause_red_icon)
            G.paused = True
            window.timer_stop_all()

        window['-IMAGE-'].update(flashcards[card_index].image, zoom=3)

    window.close()


#   ______
#  /\__  _\
#  \/_/\ \/     ___    ___     ___     ____
#     \ \ \    /'___\ / __`\ /' _ `\  /',__\
#      \_\ \__/\ \__//\ \L\ \/\ \/\ \/\__, `\
#      /\_____\ \____\ \____/\ \_\ \_\/\____/
#      \/_____/\/____/\/___/  \/_/\/_/\/___/


play_red_icon = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAAEIUlEQVR4nO3bO6hcVRQG4G8evrDSBEEQH52NokYsLCQSwcIiiIIWYikipvAJPsFCiQ9EsBAR0wmCImJhIAraiA+SThREsFHxgYKCBK4zcyzWbGfP5EbvZM4+58zl/jDcufswc/Za+1/rX2vvM72KSmCCMXpmY9sVPQyhV21/Y/8TQ7HqA3w8ffUFG7YjErt34QDx30ZFVfFwmzNrEhXnTW2uhtn42VUwYohRS3MrjcTu3Wkgd8Ckx6hCb5s6oKLfY1Jl9vXbnFAXsOOAtifQNnYc0PYE2kZdDhiIImPtUJcDxqLCGtT0fY1hVQekVd+P883K6rUJrVUnmj5/AMdws3DCxHyR1VnUtVK/CQa8gzdxkai2+jXeowjqmtxQ5IAN3IajuFswIbGhk0myztXpifgfi2bjFXyIywUbOpkkS9BzIIwdYx8+x5M4YzrWKTaUis+cDWfiKXyKvTrGhtIJKrFhhCvxEV7GOToimSVvnsKAoP1kOnavkMxbdEAySzoghUFPGNmfvh/hErwtJPNCLUpmiRumVX8fB7P7pNhPbBgLyTymRcks4YC0zf4rHsH1wshk2Hh630XJ/EALklmScqeZbbdfi8dx3MzwZGTKFTc4UTKLd5lNJMHTRYX4NK7BETPD0knUySSzeJfZRNJJRg7xJW7EXfhFGJZi/2SSea6CktlU1k2GpUz/GvbgjWxsZOaoXDKP4laFJLNp2ckz/fe4Q7TQ35o1VJtJ5lsKdZltVWFptQd4F1fjpelY30xJFiVzsctcOUG2WYamJDnAH7gPVwkjmR3QbiaZn+Gy7Popo2ubFWfZWoz/pabjuzYdsLiyr+ITXJFdZ14lfsCdos3+Ort+ymirCclPoG/Hs6InyGmfQiTN8RAexc/Z9ZUf7mjaAWlVR7gYzwuJS2NpPik3DPEVHsTh6bXEmlonVBq5vk9wj+gPFvU91QuD6d+Dono8bL56rA1NMCCt2Eg0Oy+KGGa20vn7ocgF9+OLhe+oHU3sB2yIfuAJIV/7bN4MDfAnHsB1wvi8gyyCkgz4W0x8L14QpS/zq57ifoD38BC+MSuIij+pUoIBqTrbjWdEU7PHfJ+fl8Q/CmnbL4zPS+LiKMGAtLo3TV+cmOTSfV8X+wQ/mVeIxlAyBPLGpq9BaVsGTSRBGpa2ZVBaBluRtmVQigGtStsyKMGA1qVtGdTJgFzaUtfWirQtg7oYkG9THcJjWpS2ZVCXA3bhO7FddWQ61okk939Y1QGJ0s+JrazfzSq9zhvP6g5IGxJrteo56n5Qcq2Mp74csHaGJ3RtV7hx7Dig7Qm0jR0HtD2BtpGrQL8KORts41+T9qv5fYo5BxzvhZytraRtAWOo4jAW809kXVrFA01rV80tgfTT2Qv+HdjGdN8S8hCo5bBxjdCHfwCC4TXJeYu0gAAAAABJRU5ErkJggg=='

pause_red_icon = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAADJElEQVR4nO2bMYsUMRTHfzM77oGnoig2Xqv4FYQDtRYstLFQv4EgCLb2Nn4GBQvtLexEsfETWNlYWYnooS67E4vk7WZnx7tJJntvmcsPhmUySebNP5lMkve2MGCw1MAMKFikDZUCqAAKM/yH3ZcK2+oj4J07SmxvGCLSu88CD8CeTQwYA481LTtMDJx3z2wqL33b2B5RAVMl29aN9O5zkuALUBcwNUAxUAEMlAXUxnu+UtOgTSALoG2ANlkAbQO0qQ7O0kqJnVTEUrM6Ay3o1yCGiAlcrADrmCka7Kz0UAkVQCYSD4Fd7Pd0FFC+dvmfAp9YtHgNXAEeYUUI6Qkz7HN8BJ4ROJUPFUC6/XXgZmBZn1dYAQp31MBF4HaPOrexAgS9mrGvwC9s68tCqiuSf9Jy7W/POn8GlJnTZxCUsvLb9g4XLD+MnLe1kqzRm2VmrA6YzToqIgfQWAHamG8yJCakNwSTwmC3fuIrdiAauTQDbAE3gGORdU+BN8AflseLXeACCTZzUgggo/B74G7j2hj4BpwmzFgRdQ+4gxXA5zlwnwSfzZQzwTG29cdYQUbAGfpNmApXx8jVKfeI7VErpHxn/UGwJt3EZsbyZm3boBjNkV8LZAG0DdAmC6BtgDZZAG0DtMkCaBugTRZA2wBtsgDaBmiTBdA2QJssgLYB2mQBtA3QJgugbYA26/AMle4wpPHqyJa4xA+IgyQJKQWYsBpe951+W9jG1dGst825GkUKAaSVrwIvWLS+AY4DJ9z1kFaTvNvAS6yHyHeNXfPu3cv3kEIAMXYHuJegPp8KuNXh3r1ukIou7vEYurjHo+kTIzTl4JBa08gjD9M2LkjeLq4vX+hpS1pnYgU4ySKwOuZ+45ZrWz3rPBVYbqlwV6Rl3mJd1jFBUiXwxatP6vwMvPbydEXc8x8aNnbD+7/AE3e+jiiPjcA4YQ1cavu/QAg5UDKy3H6oBEoe+bVAFkDbAG2yANoGaON/BUpjJzWjAf+btDSN9YkvwO9iEZI2VGYABn5Iguy0AFw2Ngy+9xp7g5FYw515woC7eyf8V+B/y9ShUgL8A3OOuVcAxPYaAAAAAElFTkSuQmCC'

play_icon = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAACuUlEQVR4nO2aP2gUQRSHP+9CRCxEEVQQtbLSgI11qoCVihY2loKktBUttbSwEgxYJBARC0ELMWUKQbGzEg4EExCxSKGiMTmLnce9W+d2d7KwO7N5HxzM3vzZ3Tfvvd/M3IFhGIZhGIZhGDXoA3vafogY6Lf9AE0js34ROObKfaDXzuM0j8z4CrAOXFZ1U80/TvOIAZ4CQ/dZBk6673t03BvEAM+BbeA3mRG+ATdVuyk6miS1AYbAX/cRb1gBZjztO4PPAEMyb5DyL+AusNe17ZQ3TDLA0HP9AZj19E2aMgOIN2yq64fAQdU/6SRZZAAJg213vaXKA+CKGidZyaziAfLyUtbesAyccGMkKZlFKvAKuM/4i2tvkHZJS6bPADLDT1zdLPAef2LU5TckKJlFBlhS9dPAbeCnaifeUCSZ0e8yiwyw6OqmVfszwGvKvSEZyaxiAJlFnelvAF8Z5QNJkj7JPKTGiS5JVjWAoDP9cdfGpw55ybyqxohKMkMNIOiXuAR8YuQBRZIZ3S5zpwaALCyk7gDwgPFFlPaGSZLZeoKsY4D8GADngHf87wn5JPkWOEtmgFqeEIUbKfZRLcZ/kBmkdep4QE/VHQYeMTkExBu+ANfVGMmGgJ7la8BnyiVxATji+vSI4OWhngyeAp7hz/g63j8CFzz3jIKdLoTmge+qj2/WN8k2U/tz40RF6FJ4huycsGwpvAqc99wnOkI2Q3co3wxtALcYhUn0W+O622Ed9y+A065PbX1viqIDkZfAPSYfiEjcrzEubVGt9csIPRLLS9tj4KgbI5r1fQghh6LJSFsIocfiSUhbCCE/jCQjbSFU+WksOWkLoUgGk5W2ELQBtoA/+HdtSUlbCL4/SCyQuLSFoP8iMwDmPHWdRpLZHOPH151JcqHsiln3satn3TAMwzAMwzAS5B8FC5bWiX5/VQAAAABJRU5ErkJggg=='

pause_icon = b'iVBORw0KGgoAAAANSUhEUgAAAEAAAABACAYAAACqaXHeAAACVUlEQVR4nO2au4oUQRSGv+5pZ8EbGrsvIixobiYIBuozCL6Fic+gYLKZwSKbKiY+gZGJkZGBCrpMdxtUnZ3amgK7Lsth2fNBM7vTdU799ddlhjkNhmEYhmEYhnEp6Qrj+opYgAmYE1r6ipyzz2vkkDuLPc7l58ABsAFWGfGTb/8S+Mx2xifgLvACGMlbCSMwAJ+AV4HGc0EG+w635EqvR0G+wf/9rDLn+0jjIob/N0nyCzf7Y2aH0v4kce9vZc6fGTGnlBrQB7HyOnsxIR1nByP/p7Ze53PFMSO7B2acY6DwAC01IIUMoDVZSzqXFoJn3OC/4Q6iFdt9uQc8AK4U5t4AR8Af30eHO+AOgDvsroxsWhggp/AH4El0bw18B26RJ1ZM/Q08xhkQ8hp3aMZbLpuaLx4xa9zsr3GGrIDb1H1h6nwO+bSQPkpX1A4t92x4CE6kD8USRn91Qc7qpS+0XAEXEjNAW4A2ZoC2AG3MAG0B2pgB2gK0MQO0BWhjBmgL0MYM0BagjRmgLUAbM0BbgDZmgLYAbc6jMtT7a6ZNVUd+EpfnB6RA0oSWBpzgKjkhP6j7CXv2OeK8qeJqES0MkFm+B7xhO/szcBW47u/nzJq0vQa8xVWIwtLY/aDvqtpDCwNE7D7wtEG+kAF4uKDvqg5asaQ8XsKS8ngxpQZMuH0Z782YOWojg0mdC9J2SekrNHqTeG8xpQbc8LG58dJ+nbi3V5nzZmbcmeClyMwc40rWJQ9J9cDXIJ/k/AIcBm2WIuX5j5FGYwn2oKRhGIZhGIZhXE7+AcKEj3x0sv44AAAAAElFTkSuQmCC'


back_icon = b'iVBORw0KGgoAAAANSUhEUgAAAFYAAABWCAYAAABVVmH3AAACkklEQVR4nO2c32oTQRSHv6RRQdEXUGvxNbQWoYLgS/oG9qZeeeeNeiHeiLYq+AbS9MZgk3hxZuh2YTNzJp0kG34fDLskO8nul5P5vwtCCCGEEEIIIYQQ/WQI7Kz7JLaNYce+WIJR2L4IqfmaKCQKfAb8BSbAQes94aQp9RyYhXSO5BbTljoHpiHNuSpXZW4mUeoBV6XOW/tnWJk7QHKTdEXqvJUmYfsFuInELiRX6r+wPQUeo4hdiFfqD2Av5JHUDnKlXnAp9VHIo55YB5JaAa/Un0hqEkVqBaLUfRSp14YitQLeSJXUDCS1Avr7V6CkotoLeSS1A0mtgKRWIFdqHFBROzWDptQxvlEqSe2gROrWRurgmj5nhJWXT4G3wF1s4q89Vhpf+w0cAr+AW9gPsInE4FgLN8I2FalTTOxHTPxWs2zE5kYqmNwB8AarsG6zuZE6w4qnz8Br7Hpmq/ry3DK1z+k4XKO7Dihd8DDkMlKPWRypbeLCi03mAnNzVvoBJWJ3MDGHwBFwh3yphOP6MAE4YonWSh8usJeUROwU+0HeAS9JV1pt+lIUwJoqV1VeGXJKiAX8e+AV6UosNreOsF5XX5pbYOe+crwdhE/AvdWf5mpRl3Yxa+3SRjQIU5ESubshj+Qm8A50nyK52XjlKnIdKHIrIrkVKVkC/zDkkdwE3unwEyQ3G8mtiHcd1wnwIOSR3AReud+R3GxSdx+2KzTJdVASufdDHslN4JX7DcnNRnIr4u1ENOVqQjSBV+5XrPurm5Qz8N5W/wErDiQ2g9wHQfwBnqOIddElN0odA0/CMZLqpC03LvQYY5OWzWOEk6bcCfaIqP3We6IQPdCsInoEX0XUrBJCCCGEEEIIIURv+Q+yyFJcPKZIxQAAAABJRU5ErkJggg=='

forward_icon = b'iVBORw0KGgoAAAANSUhEUgAAAFYAAABWCAYAAABVVmH3AAACYUlEQVR4nO3cT27TQBiH4TcOLIEDAAUJcQG2tCAQK7rhCFwPdc0OVrCBA/BXnAHRIAQibVjMjGK1LpnYM5VdvY80cpRq2uSXz+O4Hg9IkiRJkiRNUxObCmrOeKwBLsXtk9jaz6mnFOAe8Du2Byd+pi2l4HaBQ+A4tgWG21saR+8TQl0BR7GtMNxeGmAGPAa+sw51deLxAngY+xhuhoYQ1DtCgH9Yh9oVrpWbKVXsDvCBEOBfDLeINMZeBz5iuEXN47Yd7hLDLaId7icMt6gU7g3yw92LfQx3g65wHXMLaYf7GSu3qBTuTfLDtXIz9QnXys3UDvcLhltUCneHdbge0ArpE66Vm6krXIeFQtrhfsXKLWrbcA8x3Gwp3Fvkh7sb+xjuBqMIdzag73xg/5rmhCsPd4DXhJCPOT0nIT23AJ4CbwnhLs/tlU7YVeA9IcT2tbP/jbmXh/7RPhXXxBf5HLgXX9hYZ6fMgV/AXeAZIcCu9zyKyk1j2EtOf/pTbkW/LQwZrH8QPtHlwN9zHnIm1KU98QqhaFLlpuerSxX7grOPuFNuqXJ/EuaKzVrvOdtYx8bJG7ILH7EeCsYud25t10GsIbzXrQwJ9lrsP/bxNVc71H0GfjPoE8oqbg+Ab1y8r1v7wBs8UdhoMicIyVROaV8Bt/GUdrBR/BPmojHUCrz+VYGXZiqwUisw1AqcsFGBU4wqcFJcBU7jrMBKrcCp8hV4c0cFhlpB1w107v4DectnBd6kXElDGAa8rb6wVLGPcCGI4ly6pCIX26nI5aEqckGzilyCryIXjZQkSZIkSZP1DwX/Tsi94fGyAAAAAElFTkSuQmCC'

settings_icon = b'iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAADUklEQVR4nM2XS0iVURCAv/vQyDRBiyJatIqiyKio3IhRtHJZ0KJFBYXRC3osQze2CSRoHaG0ubhslYEgCD2kQChNoQcpLRIkF4pXr9cWZ8Yz/v9/vCoXauDw/2fOnJk5c+Z1UqwfMkAqsLYELG6A57+D0ElCtEtAI7Bb/nW//k8AbwxtWSEt30FhnjQGI7QlIRvApwyTovlmgVrcPWciexZlLQsU8NaxfDZslQoRuA2YEkYDwDkZfYKbEpqM7Fk3pGTUAN3AeaDSrB/Cna4IdBh8m+AKQqNQKTy6hafyD4KatR1/ryPAPeAS8BWYE/xNoc8A1wU3B3wDLsueEcOnPSIjBmnRbg8wA+QJO1seaDZ7m9dAPyO8rX8lnj5nNr4Cxs18AegE9uLuOCujQnCdQqP0E0CvmedCVlBEkxAWgSHB1QGtwGvgdJLmETgL9AO3gHrBDeGjoCmqhJqkGviIc6QloCWkLbAVd+9dwAvgLrAjgU5N3SI8CyKjGn/lywKOGi3nhfC4rKm50zhTDxO/53HgpFFaw/CY8JrHW/dI9HCqaSMwZpjOATfw3l5lhOdx910wzH8DO+VkGeAqMGv4jYkMK3MZND7rgB7DdNQQXzQWilpAcQ/N6UbNWo/wtrJioKm5CpjEmStn1p8Kznq6Dk1QLw19TnCTwJaIjGQzlAFSCf/BPsEqkMKdog7n3bWCO4x3lneES+2irL2XeQZoEFwt8Ey+tlDFFIk64SzOkawTfmalEy6wdiccxkXFisOHwvCD4MBXQw3DT8R94Cc+DDU7QjwMF4CDVolSiSjJT2qAa8BzXKW7A2xPoNPD2UT0FmfJ5URkCZNScT0urfbj0mwpOINL2634sNNUXARORGTGtLXFqBdXUGwxegLsw5lYM2QFsF/WbIiO4wqazrtCwmF95XieleX4FMnJyZbjaWAXkXJs77co8x/AY3wn9AW4D1wBvgszPbFGxwHB5fENyQNcJkR4PQJ+Cb32mTEo1ZI14DNem8F3kNySbQIu4Ey/mTW0ZCFIakr78E3pAGVqShU0kegzTLXO4hKVhmq0Fozhc30qgU8MQu+CpNydFiHTJHtxBvgjNGn8Pa/6VgwpEFIK4DarP80s7f8PG/HIsj7P/wIcDjLERsfn3AAAAABJRU5ErkJggg=='


music_icon = b'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'

if __name__ == '__main__':
    main()
