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
is_warn = '[تحذير]'
is_on = '[تعم]'
is_off = '[لا]'
lang_detected_msg = 'تم الاكتشاف كلغة مدعومة '
outputs_msg = 'اضهار النتائج من ال سي سي'
convert_magic_msg = 'تحويل الاوامر السحرية '
un_comment_msg = 'التعليق على الأوامر السحرية غير المدعومة'
imports_msg = 'حفظ الواردات الجديدة التي صنعت ب ال سي سي'
add_imports_cell_msg = 'إضافة عمليات استيراد جديدة إلى أعلى الملف'
help_called_msg = 'تم استخدام المساعدات '
file_ext_msg = 'الملف يجب ان يكون بصيغة .ipynb او .py'
set_output_ext_msg = 'حفظ الملف في'
specify_file_msg = 'حدد على الاقل ملف واحد '
usage_msg = 'الاستعمال: colab-convert <اختر الملف> <مكان الحفاظ > <extra_flags>'
un_command_det_msg = 'الامر غير مدعوم!'
comment_un_cmd_msg = 'التعليق خارج أمر غير مدعوم'
def_set_ret_mag_msg = 'الإعدادات الافتراضية هي الاحتفاظ بالأوامر السحرية'
ret_mag_det_msg = 'تم اكتشاف الاحتفاظ بالسحر, لن يتم حفظ التغييرات'
convert_time_msg = 'سيستغذق التحويل'
log_file_msg = 'تم انشاء السجل'
ac_over_nc_msg = '- تعليق تلقائي (-ac) يتولى الرئاسة - بدون تعليق (-NC)'
ac_over_nc_fall_msg = 'باستخدام - تعليق تلقائي (-ac)'
rm_over_cm_msg = '- السحر الإحتياطي (-rm) يتولى الرئاسة - تحويل السحر (-سم)'
rm_over_cm_fall_msg = 'باستخدام - الاحتفاظ بالسحر (-rm)'
cmd_det_msg = 'تم اكتشاف الامر'

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
