import PySimpleGUI as sg
from pathlib import Path
from typing import List, Tuple
from random import randint
import os


#    .----------------.  .----------------.  .----------------.  .----------------.  .----------------.
#   | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
#   | |  _________   | || |   _____      | || |      __      | || |    _______   | || |  ____  ____  | |
#   | | |_   ___  |  | || |  |_   _|     | || |     /  \     | || |   /  ___  |  | || | |_   ||   _| | |
#   | |   | |_  \_|  | || |    | |       | || |    / /\ \    | || |  |  (__ \_|  | || |   | |__| |   | |
#   | |   |  _|      | || |    | |   _   | || |   / ____ \   | || |   '.___`-.   | || |   |  __  |   | |
#   | |  _| |_       | || |   _| |__/ |  | || | _/ /    \ \_ | || |  |`\____) |  | || |  _| |  | |_  | |
#   | | |_____|      | || |  |________|  | || ||____|  |____|| || |  |_______.'  | || | |____||____| | |
#   | |              | || |              | || |              | || |              | || |              | |
#   | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
#    '----------------'  '----------------'  '----------------'  '----------------'  '----------------'
#    .----------------.  .----------------.  .----------------.  .----------------.  .----------------.
#   | .--------------. || .--------------. || .--------------. || .--------------. || .--------------. |
#   | |     ______   | || |      __      | || |  _______     | || |  ________    | || |    _______   | |
#   | |   .' ___  |  | || |     /  \     | || | |_   __ \    | || | |_   ___ `.  | || |   /  ___  |  | |
#   | |  / .'   \_|  | || |    / /\ \    | || |   | |__) |   | || |   | |   `. \ | || |  |  (__ \_|  | |
#   | |  | |         | || |   / ____ \   | || |   |  __ /    | || |   | |    | | | || |   '.___`-.   | |
#   | |  \ `.___.'\  | || | _/ /    \ \_ | || |  _| |  \ \_  | || |  _| |___.' / | || |  |`\____) |  | |
#   | |   `._____.'  | || ||____|  |____|| || | |____| |___| | || | |________.'  | || |  |_______.'  | |
#   | |              | || |              | || |              | || |              | || |              | |
#   | '--------------' || '--------------' || '--------------' || '--------------' || '--------------' |
#    '----------------'  '----------------'  '----------------'  '----------------'  '----------------'



"""
Copyright 2026 PySimpleGUI. All rights reserved.

Licensed under LGPL3
"""


version = '6.0'
__version__ = version.split()[0]

"""
Changelog since last major release

6.0     24-Jun-2026     Initial release     
"""

INVERSIONS_FOLDER = Path(__file__).resolve().parent.parent / "flashcards" / "inversions"


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
    flashcards = []

#   ██╗      ██████╗  █████╗ ██████╗
#   ██║     ██╔═══██╗██╔══██╗██╔══██╗
#   ██║     ██║   ██║███████║██║  ██║
#   ██║     ██║   ██║██╔══██║██║  ██║
#   ███████╗╚██████╔╝██║  ██║██████╔╝
#   ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚═════╝

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
    G.flashcards = flashcards
    G.number_of_cards = len(flashcards)
    return flashcards

#   ███████╗███████╗████████╗████████╗██╗███╗   ██╗ ██████╗ ███████╗
#   ██╔════╝██╔════╝╚══██╔══╝╚══██╔══╝██║████╗  ██║██╔════╝ ██╔════╝
#   ███████╗█████╗     ██║      ██║   ██║██╔██╗ ██║██║  ███╗███████╗
#   ╚════██║██╔══╝     ██║      ██║   ██║██║╚██╗██║██║   ██║╚════██║
#   ███████║███████╗   ██║      ██║   ██║██║ ╚████║╚██████╔╝███████║
#   ╚══════╝╚══════╝   ╚═╝      ╚═╝   ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚══════╝

def show_settings_window(location:Tuple[int|None, int|None]=(None, None), anchor: str=None):
    """
    Shows the settings window

    :param location:        Location of the icon window
    :type location:         Tuple[int, int]
    """
    sg.theme('dark red')
    flashcard_sets = [f for f in os.listdir(INVERSIONS_FOLDER) if f.endswith('.flash')]

    left_layout = [#[sg.T('Settings', font='_ 15')],
              [sg.Column([[sg.B(sg.SYMBOL_UP_ARROWHEAD, font='_ 10', p=0, k='-PER CARD UP-')], [sg.B(sg.SYMBOL_DOWN_ARROWHEAD, font='_ 10', p=0,k='-PER CARD DOWN-')]], p=0),
               sg.Input(setting=0, justification='r', s=3, k='-TIME PER CARD-'), sg.T('Seconds to show card')],
              [sg.Checkbox('Show answer before advancing', setting=False, k='-SHOW ANSWER-')],
              [sg.Column([[sg.B(sg.SYMBOL_UP_ARROWHEAD, font='_ 10', p=0, k='-DELAY UP-')], [sg.B(sg.SYMBOL_DOWN_ARROWHEAD, font='_ 10', p=0,k='-DELAY DOWN-')]], p=0),
               sg.Input(setting=0, justification='r', s=3, k='-ANSWER DELAY TIME-'), sg.T('Seconds to show answer before advance')],
              [sg.Checkbox('Order randomly', setting=False, k='-RANDOM-')]]

    right_layout = [[sg.T('Flashcards')],
                    [sg.Listbox(flashcard_sets, size=(15,10), k='-FLASH LIST-', no_scrollbar=True)],
                    [sg.P(), sg.B('Load'), sg.P()],
                    ]
    layout = [[sg.Frame("", [[sg.Col(left_layout), sg.Col(right_layout)],
              [sg.OK(), sg.Cancel()]], border_width_no_relief=2, p=0, expand_x=True, expand_y=True)]]

    window = sg.Window('Settings', layout, location=location, keep_on_top=True, font='_ 18',  location_anchor=anchor)

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
        elif event == 'Load':
            try:
                flashset = values['-FLASH LIST-'][0]
            except:     # may not have selected anything.  If so, ignore
                continue
            G.flashcards = load_flashcards(flashset)
            sg.popup(f'Loaded flashcard set {flashset}', keep_on_top=True)
    window.close()


def load_settings():
    G.show_answer = sg.user_settings_get_entry('-SHOW ANSWER-', False)
    G.random_order = sg.user_settings_get_entry('-RANDOM-', False)
    G.time_per_card = float(sg.user_settings_get_entry('-TIME PER CARD-', 0))
    G.answer_delay_time = float(sg.user_settings_get_entry('-ANSWER DELAY TIME-', 0))






#   ███╗   ███╗ █████╗ ██╗███╗   ██╗
#   ████╗ ████║██╔══██╗██║████╗  ██║
#   ██╔████╔██║███████║██║██╔██╗ ██║
#   ██║╚██╔╝██║██╔══██║██║██║╚██╗██║
#   ██║ ╚═╝ ██║██║  ██║██║██║ ╚████║
#   ╚═╝     ╚═╝╚═╝  ╚═╝╚═╝╚═╝  ╚═══╝


def main():

    # --------------------------------- NEXT / PREV CARD ---------------------------------
    def next_card(card_index):
        if G.random_order:
            card_index = randint(0, G.number_of_cards - 1)
        else:
            card_index = (card_index + 1) % G.number_of_cards
        return card_index

    def prev_card(card_index):
        return (card_index + (G.number_of_cards - 1)) % G.number_of_cards
    # ------------------------------------------------------------------------------------

    sg.set_options(icon=music_icon)
    flashcards = load_flashcards('inversions.flash')
    G.number_of_cards = len(flashcards)
    load_settings()

    layout = [[sg.P(), sg.Image(settings_icon, enable_events=True, k='-SETTINGS-')],
              [sg.Image(source=back_icon, enable_events=True, k='-BACK-'), sg.Push(), sg.Image(flashcards[0].image, zoom=3, k='-IMAGE-'), sg.Push(), sg.Image(source=forward_icon,  enable_events=True, k='-FORWARD-')],
              [],
              [sg.P(), sg.Button(size=(3,1), k='-ANSWER-', font='_ 60'), sg.P()],
              [sg.P(),sg.Button(image_source=play_icon, k='-PLAY-', border_width=0, button_color=(sg.theme_button_color_text(), sg.theme_background_color())),
                           sg.Button(image_source=pause_red_icon, k='-PAUSE-', border_width=0, button_color=(sg.theme_button_color_text(), sg.theme_background_color())), sg.P()]]
              # [sg.Push(), sg.Button(sg.SYMBOL_X_SMALL, button_color=(sg.theme_button_color_text(), sg.theme_background_color()), border_width=0, font='_18', k='Exit')]]


    window = sg.Window("Inversions Flashcards", layout, finalize=True, auto_save_location=True, keep_on_top=True, use_custom_titlebar=True, titlebar_icon=music_icon)

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
            window.minimize()
            show_settings_window(location=window.current_location(use_anchor=sg.WIN_ANCHOR_CENTER), anchor=sg.WIN_ANCHOR_CENTER)
            load_settings()
            if flashcards != G.flashcards:
                flashcards = G.flashcards       # New set loaded in settings
            card_index = 0
            window.normal()
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


#   ██╗ ██████╗ ██████╗ ███╗   ██╗███████╗
#   ██║██╔════╝██╔═══██╗████╗  ██║██╔════╝
#   ██║██║     ██║   ██║██╔██╗ ██║███████╗
#   ██║██║     ██║   ██║██║╚██╗██║╚════██║
#   ██║╚██████╗╚██████╔╝██║ ╚████║███████║
#   ╚═╝ ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝╚══════╝

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
