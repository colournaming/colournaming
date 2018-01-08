#!/usr/bin/env python3

from collections import defaultdict
import os.path
import sys
import openpyxl


def read_translations(translation_filename):
    translation_workbook = openpyxl.load_workbook(translation_filename)
    ws = translation_workbook.active
    row = 4
    translation_dict = defaultdict(str)
    while True:
        english = ws['B{0}'.format(row)].value
        translated = ws['C{0}'.format(row)].value
        print(english, translated)
        if not english:
            break
        translation_dict[english] = translated
        row += 1
    return translation_dict


def do_translation(messages, translation_dict, output):
    msgid = ""
    state = None
    for l in messages:
        l = l.strip()
        if l.startswith('msgid'):
            msgid = l.split(' ', maxsplit=1)[1][1:-1]
            state = 'MSGID'
        elif l.startswith('"') and state == 'MSGID':
            msgid += l[1:-1]
        elif l == 'msgstr ""':
            l = 'msgstr "' + translation_dict[msgid] + '"'
        output.write(l + '\n') 


def main(translation_filename, messages_filename, output_filename):
    translation_dict = read_translations(translation_filename)
    with open(messages_filename) as messages:
        with open(output_filename, 'w') as output:
            do_translation(messages, translation_dict, output)
        

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], sys.argv[3])