# D118-PS-Enrollment-Translation

Script to translate the PowerSchool ECollect enrollment localization plugin data into different languages.

## Overview

This script is a fairly straightforward translation script. It takes files from an input folder, translates everything to the right of an equal sign on each line, and outputs it to an output folder with the same filename but with the language code changed to the relevant language. It uses the googletrans library, which is a bit of a hacky unoffical Google Translate plugin. For this reason, a lot of waits/delays are necessary in the code, otherwise Google kicks you out for doing too many translations too fast.

## Requirements

The following Python library must be installed on the host machine (links to the installation guide):

- [googletrans](https://github.com/ssut/py-googletrans?tab=readme-ov-file#installation)

However, the library is a bit out of date and seemingly abandoned. The "master" branch seems to have issues working at all, so many suggestions are to use a newer version with `pip install googletrans==4.0.0rc1`. I found that version to have issues with "gendered" language (like German, French, Spanish, etc), so based on [this](https://github.com/ssut/py-googletrans/issues/260#issuecomment-751521801) comment I forked the library and made the changes to fix it. You can find my version [here](https://github.com/Philip-Greyson/py-googletrans/tree/feature/rpc) if you would like to download it and use pip to install it locally in a venv (which I did to run the project).

You must have the the input files in a folder, and the files must contain a language code in the filename which will be replaced for the output name. The lines to be translated inside the file should be in the format `example.key.etc=Text` where the "Text" will be translated while the key and equal sign will be left as-is.

## Customization

Assuming you have similar files for the Ecollect registration translation plugin as we do, this script should mostly just work. However, there are some things you can change defined as constants near the top of the script:

- `LANGUAGES` can be edited to include the languages of your choosing assuming they are supported by the translation library. See [here](https://github.com/ssut/py-googletrans/blob/feature/rpc/googletrans/constants.py) for the language codes in googletrans.
- `INPUT_FOLDER` is the path to the files that need translation. In my case, it is a directory inside the main program directory, simply named "Input". You will want to include an asterisk  after the directory name to include all files, or you can do an asterisk and file type if you have other files in the directory, for example Input/*.properties
- `OUTPUT_FOLDER` is the path to the folder that will get the output files put into it.
- `INPUT_LANGUAGE_CODE` is the country/language code that is in the filename, which will be replaced with the language code for the output filename.
  - If you are starting from a language other than english, you will also want to edit the `translated = translator.translate(textToTranslate, src='en', dest=lang).text` line and edit the src to match whatever source language you begin with.
- `OVERWRITE_EXISTING_OUTPUT` will have the program overwrite any existing matching language files already in the output folder. By default, this is False as every language takes a long time, but if there were changes to the input files you will either want to set this to True, or delete the files from the output so it can process them correctly.
