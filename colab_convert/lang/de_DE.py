############################
## Multi Language Support ##
############################

# Du kannst dies als Vorlage verwenden, um neue Sprachunterstützung für das Projekt zu erstellen!
# Ändere bitte nicht die Namen der Variablen oder die Namen der Befehle wie --help/-h --retain-magic/-rm etc.
# Bearbeite nur die Nachricht nach dem Gleichheitszeichen und ändere auch nicht die "command flag names".

##############
##  German  ##
##   de_DE  ##
##############

# Standardmeldungen
is_warn = '[Warnung]'
is_on = '[An]'
is_off = '[Aus]'
lang_detected_msg = 'Wird als unterstützte Sprache erkannt'
outputs_msg = 'Ausgaben von cc anzeigen'
convert_magic_msg = 'Magische Befehle umwandeln'
un_comment_msg = 'Auskommentieren von nicht unterstützten magischen Befehlen'
imports_msg = 'Neue importierungen von cc beibehalten'
add_imports_cell_msg = 'Hinzufügen neuer Importe an den Anfang der Datei'
help_called_msg = 'Hilfemeldung aufgerufen'
file_ext_msg = 'Datei muss .ipynb oder .py sein'
set_output_ext_msg = 'Einstellung der Ausgabedatei auf'
specify_file_msg = 'Bitte mindestens eine zu konvertierende Datei angeben'
usage_msg = 'Benutzung: colab-convert <input_file> <output_file> <extra_flags>'
un_command_det_msg = 'Nicht unterstützter Befehl entdeckt!'
comment_un_cmd_msg = 'Nicht unterstützter Befehl wird auskommentiert'
def_set_ret_mag_msg = 'Standardeinstellungen behalten magische Befehle bei'
ret_mag_det_msg = '--retain-magic wurde entdeckt, es werden KEINE neuen Importierungen gemacht'
convert_time_msg = 'Umstellung dauerte'
log_file_msg = 'Protokolldatei wurde erstellt'
ac_over_nc_msg = '--auto-comment (-ac) ersetzt --no-comment (-nc)'
ac_over_nc_fall_msg = 'Nutzt --auto-comment (-ac)'
rm_over_cm_msg = '--retain-magic (-rm) ersetzt --convert-magic (-cm)'
rm_over_cm_fall_msg = 'Nutzt --retain-magic (-rm)'
cmd_det_msg = 'Befehl erkannt'

# Standardwörter
convert_wrd = 'Konvertieren'
converted_wrd = f'{convert_wrd}ed'
finished_wrd = 'Fertig'
to_wrd = 'zu'
seconds_wrd = 'Sekunden'
input_wrd = 'Eingabe'
output_wrd = 'Ausgabe'

# Standardoptionen
flags_desc = {
    'Colab-Convert': '\nall Flags sind optional und haben Standardwerte für beste Ergebnisse \n Benutze flags um bestimmte Funktionen standardmäßig ein- oder auszuschalten \n',
    'Usage:': 'colab-convert <input_file> <output_file> <flags>',
    'Example:': 'colab-convert in.ipynb out.py -nc -rm -o\n',
    '<input_file>:': 'Eingabedatei zum Konvertieren',
    '<output_file>:': 'Ausgabedatei zum Schreiben in',
    '<flags>:': '"extra flags" zur Übergabe an den Konverter\n',
    '--help': '(-h)\n  Diese Hilfemeldung anzeigen\n',
    'Default Flags Set (Standardwerte werden durch die Eingabedatei bestimmt)': '\n  ipynb input file:\n    [YES] Magie umwandeln , [YES] Auto-Kommentar , [YES] Importe , [NO] Ausgaben\n  py input file:\n    [NO] Magie umwandeln , [NO] Auto-Kommentar , [NO] Importe , [NO] Ausgaben\n',
    'Available Flags': '\n  toggle certain items on or off\n',
    '  --retain-magic': ' (-rm)  : Magische Befehle in der Ausgabe behalten\n      .py default    [ON]\n      .ipynb default [OFF]',
    '  --convert-magic': ' (-cm) : Magische Befehle in Python Code umwandeln\n      .py default    [OFF]\n      .ipynb default [ON]',
    '  --auto-comment': ' (-ac)  : Nicht unterstützte magische Befehle in Kommentare umwandeln\n      .py default    [OFF]\n      .ipynb default [ON]',
    '  --no-comment': ' (-nc)    : Nicht unterstützte magische Befehle beibehalten\n      .py default    [ON]\n      .ipynb default [OFF]',
    '  --no-imports': ' (-ni)    : Keine Importe aus konvertierten magischen Befehlen hinzufügen\n      .py default    [OFF]\n      .ipynb default [OFF]',
    '  --outputs': ' (-o)        : Ausgaben auf der Konsole von Konvertierungen und kommentierten Zeilen.\n      .py default    [OFF]\n      .ipynb default [OFF]',
}
