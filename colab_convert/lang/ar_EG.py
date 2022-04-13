############################
## Multi Language Support ##
############################

# you can use this as template to create new language support for the project!
# plase do not change the varible names or command flag names like --help/-h --retain-magic/-rm ect.
# only edit the message after the equal sign and also do not change the command flag names

##############
##  Arabic  ##
##  ar_EG   ##
##############

# default messages
is_warn = '[WARN]'
is_on = '[OK]'
is_off = '[NOT]'
lang_detected_msg = 'Detected as a supported Language'
outputs_msg = 'showing outputs from cc'
convert_magic_msg = 'convert magic commands'
un_comment_msg = 'commenting out unsupported magic commands'
imports_msg = 'keeping new imports made by cc'
add_imports_cell_msg = 'adding new imports to the top of the file'
help_called_msg = 'help message called'
file_ext_msg = 'file must be .ipynb or .py'
set_output_ext_msg = 'setting output file to'
specify_file_msg = 'please specify atleast one file to convert'
usage_msg = 'Usage: colab-convert <input_file> <output_file> <extra_flags>'
un_command_det_msg = 'unsupported command is detected!'
comment_un_cmd_msg = 'commenting out unsupported command'
def_set_ret_mag_msg = 'default settings is retaining magic commands'
ret_mag_det_msg = '--retain-magic is detected, new imports will NOT be made'
convert_time_msg = 'conversion took'
log_file_msg = 'log file created'
ac_over_nc_msg = '--auto-comment (-ac) takes presidence over --no-comment (-nc)'
ac_over_nc_fall_msg = 'using --auto-comment (-ac)'
rm_over_cm_msg = '--retain-magic (-rm) takes presidence over --convert-magic (-cm)'
rm_over_cm_fall_msg = 'using --retain-magic (-rm)'
cmd_det_msg = 'command detected'

# default words
convert_wrd = 'convert'
converted_wrd = f'{convert_wrd}ed'
finished_wrd = 'finished'
to_wrd = 'to'
seconds_wrd = 'seconds'
input_wrd = 'input'
output_wrd = 'output'

# default options
flags_desc = {
    'Colab-Convert': '\nall flags are optional and have set defaults for best results\nuse flags to enable or disable certain functions on/off by default\n',
    'Usage:': 'colab-convert <input_file> <output_file> <flags>',
    'Example:': 'colab-convert in.ipynb out.py -nc -rm -o\n',
    '<input_file>:': 'input file to convert',
    '<output_file>:': 'output file to write to',
    '<flags>:': 'extra flags to pass to the converter\n',
    '--help': '(-h)\n  Show this help message\n',
    'Default Flags Set (defaults are determined by input file)': '\n  ipynb input file:\n    [YES] convert magic , [YES] auto comment , [YES] imports , [NO] Outputs\n  py input file:\n    [NO] convert magic , [NO] auto comment , [NO] imports , [NO] Outputs\n',
    'Available Flags': '\n  toggle certain items on or off\n',
    '  --retain-magic': ' (-rm)  : Keep magic commands in the output\n      .py default    [ON]\n      .ipynb default [OFF]',
    '  --convert-magic': ' (-cm) : Convert magic commands to python code\n      .py default    [OFF]\n      .ipynb default [ON]',
    '  --auto-comment': ' (-ac)  : Convert unsupported magic commands to comments\n      .py default    [OFF]\n      .ipynb default [ON]',
    '  --no-comment': ' (-nc)    : Keep unsupported magic commands\n      .py default    [ON]\n      .ipynb default [OFF]',
    '  --no-imports': ' (-ni)    : Do not add imports from converted magic commands\n      .py default    [OFF]\n      .ipynb default [OFF]',
    '  --outputs': ' (-o)        : Outputs to console of conversions and commented lines.\n      .py default    [OFF]\n      .ipynb default [OFF]',
}