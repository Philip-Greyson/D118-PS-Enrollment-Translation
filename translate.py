"""Script to translate the PS Ecollect forms to various languages.

https://github.com/Philip-Greyson/D118-PS-Enrollment-Translation

needs googletrans - I needed to build my own version to fix gendered language issues: https://github.com/Philip-Greyson/py-googletrans

Opens the input files, translates the bit of text after the equal sign, outputs it to a file named with the language code.
Is very slow, waits 3 seconds between lines to prevent rate-limiting translation failure. Also pauses for a minute every 100 lines, and 5 minutes between files
"""


import glob
import time

import googletrans
from googletrans import Translator

# for language codes, see https://github.com/ssut/py-googletrans/blob/master/googletrans/constants.py
LANGUAGES = ['ru', 'tl', 'fr', 'de', 'gu', 'hi', 'hu', 'ko', 'pl', 'pa', 'uk', 'ur']  # define the languages to translate to
INPUT_FOLDER = 'Input/*'
OUTPUT_FOLDER = 'Output/'
INPUT_LANGUAGE_CODE = 'US_en'
OVERWRITE_EXISTING_OUTPUT = False

if __name__ == '__main__':
    translator = Translator()
    inputFiles = glob.glob(INPUT_FOLDER)  # get all files in input folder
    for lang in LANGUAGES:  # go through each language one at a time
        for inputFile in inputFiles:
            print(inputFile)  # debug
            outputFileName = inputFile.split('/')[1]  # get rid of the leading input folder and only get the filename
            outputFile = OUTPUT_FOLDER + outputFileName.split(INPUT_LANGUAGE_CODE)[0] + lang + outputFileName.split(INPUT_LANGUAGE_CODE)[1]  # construct the output file name, replace the US_en language code with the new one
            if OVERWRITE_EXISTING_OUTPUT or not (glob.glob(outputFile)):  # if the output doesnt already exist, or we want to overwrite it
                with open(outputFile, 'w') as output:  # open the output file
                    with open(inputFile) as f:  # open the file for reading
                        lines = f.readlines()
                        for count, line in enumerate(lines):
                            # print(line.strip())  # debug
                            if count % 100 == 0 and count != 0:  # if the line count is divisible by 100
                                time.sleep(60)  # sleep 60 seconds to not get failing translation
                            if "=" in line:
                                try:
                                    lineParts = line.split("=")  # split the line into two parts, the variable definition in the first element, the text that it relates to in the second
                                    variable = lineParts[0]
                                    textToTranslate = lineParts[1]
                                    translated = translator.translate(textToTranslate, src='en', dest=lang).text  # do the actual translation of the text
                                    print(f'{variable}={translated}')
                                    print(f'{variable}={translated}', file=output)
                                except Exception as er:
                                    print(f'Encountered an error on line {count}: {er}')
                                    print(f'{variable}=ERROR, please translate manually!')
                            else:  # if the current line doesnt have an = sign, it doesnt need anything translated, and can be just output as is
                                print(line.strip())
                                print(line.strip(), file=output)
                            time.sleep(3)  # sleep 3 seconds between each line
                time.sleep(300)  # wait 5 minutes between each file so it does not fail

