<p align="center">
  <img src="https://pysimplegui.net/images/logos/Logo_Full_Transparent.png" alt="Description" width="400">
</p>

<p align="center">
  <h2 align="center">psgflash</h2>
  <h2 align="center">A PySimpleGUI Flashcard Application</h2>
</p>



## Features

* Create flash cards
* Manual advance or playback based
* Control playback speed (how long a flashcard remains until answer is shown)
* Control how long answer is shown
* Random or ordered flashcards
* Load multiple sets of cards

## Installation

### Using PIP with PyPI

Not yet on PyPI

### Using PIP with GitHub

You can also pip install the PySimpleGUI Applications that are in the PySimpleGUI GitHub account.  The GitHub versions have bug fixes and new programs/features that have not yet been released to PyPI. To directly pip install from that repo:

#### If you use the command `python` on your computer to invoke Python (Windows):

```bash
python -m pip install --upgrade https://github.com/PySimpleGUI/psgflash/zipball/main
```

#### If you use the command `python3` on your computer to invoke Python (Linux, Mac):

```bash
python3 -m pip install --upgrade https://github.com/PySimpleGUI/psgflash/zipball/main
```
NOTE - the sample flashcard files and images are not currently pip installed.  It's best to clone the repo at this point since you'll want to edit the flashcard files and use your own images

## Usage

Create a flashcard file

The format of a flashcard file is each card is on a single line.  The line contains:
`filename,text_answer`

Here's an example that's included in this repo

```text
Inv003.png,C
Inv006.png,C♯
Inv009.png,D
Inv012.png,E♭
Inv015.png,E
```

## Development status

Still very much in progress.  I coded it up specifically for my own use.  The code is tuned to match the images that I'm using.  Next step would be to look through the images and find the sizes and scale as needed.  Maybe setting for target image size.  Or it could be part of the flashcard file itself.

You may need to edit the code to meet your needs.  It's rather simple code.


## Screen Capture

https://github.com/user-attachments/assets/ae5280fa-1d2b-47fe-ad21-35c9f7fc30d8


## License & Copyright

Copyright 2026 PySimpleGUI.

Licensed under LGPL3.

## Contributing

We are happy to receive issues describing bug reports and feature
requests! If your bug report relates to a security vulnerability,
please do not file a public issue, and please instead reach out to us
at issues@PySimpleGUI.com.

We do not accept (and do not wish to receive) contributions of
user-created or third-party code, including patches, pull requests, or
code snippets incorporated into submitted issues. Please do not send
us any such code! Bug reports and feature requests should not include
any source code.

If you nonetheless submit any user-created or third-party code to us,
(1) you assign to us all rights and title in or relating to the code;
and (2) to the extent any such assignment is not fully effective, you
hereby grant to us a royalty-free, perpetual, irrevocable, worldwide,
unlimited, sublicensable, transferrable license under all intellectual
property rights embodied therein or relating thereto, to exploit the
code in any manner we choose, including to incorporate the code into
PySimpleGUI and to redistribute it under any terms at our discretion.
