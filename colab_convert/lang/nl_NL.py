############################
## Multi Language Support ##
############################

# you can use this as template to create new language support for the project!
# plase do not change the varible names or command flag names like --help/-h --retain-magic/-rm ect.
# only edit the message after the equal sign and also do not change the command flag names

#############
##  Dutch  ##
##  nl_NL  ##
#############

# default messages
is_warn = '[WAARSCHUW]'
is_on = '[OK]'
is_off = '[NIET]'
lang_detected_msg = 'gedetecteerd als een ondersteunde taal'
outputs_msg = 'toont uitvoer van cc'
convert_magic_msg = 'converteer magische commandos'
un_comment_msg = 'commenting out niet ondersteunde magische commandos'
imports_msg = 'behoud nieuwe imports gemaakt door cc'
add_imports_cell_msg = 'voeg nieuwe imports toe aan de bovenkant van het bestand'
help_called_msg = 'help bericht opgevraagd'
file_ext_msg = 'bestand moet .ipynb or .py zijn'
set_output_ext_msg = 'uitvoerbestand instellen op'
specify_file_msg = 'specifieer minimaal één bestand om te converteren alstublieft'
usage_msg = 'Gebruik: colab-convert <invoer_bestand> <uitvoer_bestand> <extra_flags>'
un_command_det_msg = 'niet ondersteund commando gedetecteerd!'
comment_un_cmd_msg = 'commenting out niet ondersteunde commandos'
def_set_ret_mag_msg = 'standaard instellingen behoudt magische commandos'
ret_mag_det_msg = '--retain-magic is gedetecteerd, nieuwe imports worden NIET gemaakt'
convert_time_msg = 'conversion took'
log_file_msg = 'log bestand aangemaakt'
ac_over_nc_msg = '--auto-comment (-ac) heeft voorrang op --no-comment (-nc)'
ac_over_nc_fall_msg = 'gebruik --auto-comment (-ac)'
rm_over_cm_msg = '--retain-magic (-rm) heeft voorrang op --convert-magic (-cm)'
rm_over_cm_fall_msg = 'gebruik --retain-magic (-rm)'
cmd_det_msg = 'commando detecteerd'

# default words
convert_wrd = 'converteer'
converted_wrd = f'{convert_wrd}ed'
finished_wrd = 'klaar'
to_wrd = 'naar'
seconds_wrd = 'secondes'
input_wrd = 'invoer'
output_wrd = 'uitvoer'

# default options
flags_desc = {
    'Colab-Convert': '\nalle flags zijn optioneel en hebben standaard instellingen voor het beste resultaat\ngebruik flags om bepaalde functies in of uit te schakelen\n',
    'Gebruik:': 'colab-convert <invoer_bestand> <uitvoer_bestand> <flags>',
    'Voorbeeld:': 'colab-convert in.ipynb out.py -nc -rm -o\n',
    '<invoer_bestand>:': 'invoer bestand om te converteren',
    '<uitvoer_bestand>:': 'uitvoer bestand om naar te schrijven',
    '<flags>:': 'extra flags om door te geven aan de converter\n',
    '--help': '(-h)\n  Laat dit hulp bericht zien\n',
    'Standaard Flags ingesteld (standaardinstellingen zijn bepaald door invoer bestand)': '\n  ipynb invoer bestand:\n    [JA] convert magic , [JA] auto comment , [JA] invoer , [NEE] uitvoer\n  py invoer bestand:\n    [NEE] convert magic , [NEE] auto comment , [NO] invoer , [NEE] Uitvoer\n',
    'Beschikbare Flags': '\n  Zet bepaalde items aan of uit\n',
    '  --retain-magic': ' (-rm)  : Behoud magische commandos in de uitvoer\n      .py default    [AAN]\n      .ipynb default [UIT]',
    '  --convert-magic': ' (-cm) : Converteer magische commandos naar python code\n      .py default    [UIT]\n      .ipynb default [AAN]',
    '  --auto-comment': ' (-ac)  : Converteer niet ondersteunde magische commandos naar comments\n      .py default    [UIT]\n      .ipynb default [AAN]',
    '  --no-comment': ' (-nc)    : Behoud niet ondersteunde magische commandos\n      .py default    [AAN]\n      .ipynb default [UIT]',
    '  --no-imports': ' (-ni)    : Voeg imports van geconverteerde magicsche commandos niet toe\n      .py default    [UIT]\n      .ipynb default [AAN]',
    '  --outputs': ' (-o)        : Uitvoer naar console van conversies en commented lines.\n      .py default    [UIT]\n      .ipynb default [AAN]',
}
