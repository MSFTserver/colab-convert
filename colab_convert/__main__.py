import sys, time, os, logging, locale, json, json5

# set up logging, adds new logger mode and level
log_file = 'cc-outputs.log'
logger= logging.getLogger()
handler = logging.FileHandler(log_file, 'a', 'utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler(sys.stdout))

# use of RFC 1766 to get language code
sup_lang = {
    'en_US': ['en_US', 'en', 'english', 'eng'], # English
    #'de_DE':  ['de_DE', 'de', 'german', 'ger', 'deutsch'], # German
    #'fr_FR': ['fr_FR', 'fr', 'french', 'fre', 'français', 'française'],  # French
    #'es_ES': ['es_ES', 'es', 'spanish', 'spa', 'español', 'española'],  # Spanish
    #'ar_AR': ['ar_EG', 'ar', 'eurabaa', 'ara', 'عربى'],  # Arabic
    'nl_NL': ['nl_NL', 'nl', 'dutch', 'dut', 'nlt', 'nederlands']   # Dutch
}
supported_languages = []
translation = None
for i in sup_lang:
    supported_languages.extend(sup_lang[i])

first_run = 1
def get_language(user_language):
    global translation, first_run
    is_lang = False
    if user_language in supported_languages:
        for k,v in sup_lang.items():
            if user_language in v:
                is_lang = True
                lang_file_name = k
                break
    else:
        lang_file_name = 'en_US'

    with open(f"{os.path.dirname(__file__)}/lang/{lang_file_name}.txt", 'r', encoding='utf-8') as f:
        translation = json5.load(f)
    if is_lang:
        if first_run:
            first_run = False
            logging.info(f"\n---------------------------\n----------[{translation['defwrd_start_wrd']}]----------\n---------------------------")
        logging.info(f"[{translation['defwrd_ok_wrd']}]   {user_language} {translation['defmsg_lang_detected_msg']}")
    else:
        logging.warn(f"[WARN]  {user_language} not supported. defaulting to English")

# detect user locale
user_language = locale.getdefaultlocale()[0]
get_language(user_language)

# default conversion code
header_comment = '# %%\n'
cc_auto_comment = '#<cc-ac>'
cc_trailing_comment = ' #<cc-cm>'
cc_import_comment = '#<cc-imports>\n'
os_import = "import os\n"
sp_import = "import subprocess\n"
new_imports_meta_py = '# !! {"metadata":{\n# !!   "id":"cc-imports"\n# !! }'+"}\n"
new_imports_cell_py = f"{header_comment}{new_imports_meta_py}\n{cc_import_comment}\n"
new_imports_meta_ipy = {'id':'cc-imports'}
new_imports_cell_ipy = cc_import_comment
new_import = False
os_added = False
sp_added = False

# default options
flags_desc = {
    'Colab-Convert': f"\n{translation['defmsg_help_main_1_msg']}\n{translation['defmsg_help_main_2_msg']}n",
    f"{translation['defwrd_usage_wrd']}:": f"colab-convert <{translation['defmsg_in_file_msg']}> <{translation['defmsg_out_file_msg']}> <{translation['defwrd_flags_wrd']}>",
    f"{translation['defwrd_example_wrd']}:": f"colab-convert {translation['defwrd_in_wrd']}.ipynb {translation['defwrd_out_wrd']}.py -nc -rm -o\n",
    f"<{translation['defmsg_in_file_msg']}>:": f"{translation['defmsg_in_file_convert_msg']}",
    f"<{translation['defmsg_out_file_msg']}>:": f"{translation['defmsg_out_file_convert_msg']}",
    f"<{translation['defwrd_flags_wrd']}>:": f"{translation['defmsg_flags_help_msg']}\n",
    f"--help": f"(-h)\n  {translation['defmsg_help_flag_msg']}\n",
    f"{translation['defmsg_def_flag_msg']} ({translation['defmsg_def_flag_tip_msg']})": f"\n  ipynb {translation['defmsg_in_file_msg']}:\n    [{translation['defwrd_yes_wrd']}] {translation['defmsg_convert_msg']} , [{translation['defwrd_yes_wrd']}] {translation['defmsg_auto_comment_msg']} , [{translation['defwrd_yes_wrd']}] {translation['defwrd_imports_wrd']} , [{translation['defwrd_no_wrd']}] {translation['defwrd_outputs_wrd']}\n  py {translation['defmsg_in_file_msg']}:\n    [{translation['defwrd_no_wrd']}] {translation['defmsg_convert_msg']} , [{translation['defwrd_no_wrd']}] {translation['defmsg_auto_comment_msg']} , [{translation['defwrd_no_wrd']}] {translation['defwrd_imports_wrd']} , [{translation['defwrd_no_wrd']}] {translation['defwrd_outputs_wrd']}\n",
    f"{translation['defmsg_avl_flags_msg']}": f"\n  {translation['defmsg_avl_flags_tip_msg']}\n",
    f"  --retain-magic": f" (-rm)  : {translation['defmsg_rm_info_msg']}\n      .py {translation['defwrd_default_wrd']}    [{translation['defwrd_on_wrd']}]\n      .ipynb {translation['defwrd_default_wrd']} [{translation['defwrd_off_wrd']}]",
    f"  --convert-magic": f" (-cm) : {translation['defmsg_cm_info_msg']}\n      .py {translation['defwrd_default_wrd']}    [{translation['defwrd_off_wrd']}]\n      .ipynb {translation['defwrd_default_wrd']} [{translation['defwrd_on_wrd']}]",
    f"  --auto-comment": f" (-ac)  : {translation['defmsg_ac_info_msg']}\n      .py {translation['defwrd_default_wrd']}    [{translation['defwrd_off_wrd']}]\n      .ipynb {translation['defwrd_default_wrd']} [{translation['defwrd_on_wrd']}]",
    f"  --no-comment": f" (-nc)    : {translation['defmsg_nc_info_msg']}\n      .py {translation['defwrd_default_wrd']}    [{translation['defwrd_on_wrd']}]\n      .ipynb {translation['defwrd_default_wrd']} [{translation['defwrd_off_wrd']}]",
    f"  --no-imports": f" (-ni)    : {translation['defmsg_ni_info_msg']}\n      .py {translation['defwrd_default_wrd']}    [{translation['defwrd_off_wrd']}]\n      .ipynb {translation['defwrd_default_wrd']} [{translation['defwrd_off_wrd']}]",
    f"  --outputsv": f" (-o)       : {translation['defmsg_out_info_msg']}\n      .py {translation['defwrd_default_wrd']}    [{translation['defwrd_off_wrd']}]\n      .ipynb {translation['defwrd_default_wrd']} [{translation['defwrd_off_wrd']}]",
    f"  --lang=": f" (-l=)         : {translation['defmsg_lang_info_msg']}\n       {translation['defwrd_default_wrd']} [English]\n      --lang=en_US\n      {', '.join(supported_languages)}"
}
magic_list = ["cd","env","set_env"]
help_flags = ['--help', '-h', '?']
flags_list = ['--auto-comment', '-ac', '--no-comment', '-nc', '--retain-magic', '-rm', '--convert-magic', '-cm','--no-imports', '-ni', '--outputs', '-o', '--lang=' , '-l=']

def check_imports(add_import,flags,f_type):
    strip_import = add_import.replace('import ','').replace('\n','')
    if not flags['n_i']:
        if not os_added or not sp_added:
            if strip_import == 'os':
                globals()['os_added'] = True
            if strip_import == 'subprocess':
                globals()['sp_added'] = True
            if f_type == 'ipy':
                globals()['new_imports_cell_ipy']+=add_import
            if f_type == 'py':
                globals()['new_imports_cell_py']+=add_import
            globals()['new_import'] = True

# convert notebook to python
def nb2py(notebook, flags):
    result = []
    cells = notebook['cells']

    main_metadata = json.dumps(notebook['metadata'],indent=2).split("\n")
    reformat_main_metadata = '# !! {"main_metadata":'

    for key in main_metadata:
        if key == '{':
            reformat_main_metadata+=f"{key}\n"
        elif key == '}':
            reformat_main_metadata+="# !! "+key+"}\n"
        else:
            reformat_main_metadata+=f"# !! {key}\n"
    for cell in cells:
        cell_type = cell['cell_type']
        metadata = cell['metadata']
        format_metadata = json.dumps(metadata,indent=2).split("\n")
        reformat_metadata = '# !! {"metadata":'
        for key in format_metadata:
            if key == '{':
                reformat_metadata+=f"{key}\n"
            elif key == '}':
                reformat_metadata+="# !! "+key+"}\n"
            else:
                reformat_metadata+=f"# !! {key}\n"
    
        if cell_type == 'markdown':
            result.append('%s"""\n%s\n"""'%
                          (header_comment+reformat_metadata, ''.join(cell['source'])))

        if cell_type == 'code':

            source = cell['source']
            x = 0

            for line in source:
                spaces_in_line = len(line) - len(line.lstrip(' '))
                spaces = ""
                for i in range(spaces_in_line):
                    spaces+=" "
                strip_line = line.lstrip(' ')
                    
                # if magic command includes a '!' bang use subprocess to call the command
                if strip_line.startswith('!') and flags['c_m']:
                    cmd = strip_line[:-1].replace("!","",1).split(" ")
                    logging.warn(f"[{translation['defwrd_warn_wrd']}] !{cmd[0]} {translation['defmsg_cmd_det_msg']}")
                    new_cmd = f"    sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8')\n    print(sub_p_res)\n"
                    new_cmd_spaces = f"{spaces}sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8'){cc_trailing_comment}\n{spaces}print(sub_p_res){cc_trailing_comment}\n"
                    source[x] = new_cmd_spaces
                    check_imports(sp_import,flags,'py')
                    logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defwrd_converted_wrd']}:\n    {strip_line}  {translation['defwrd_to_wrd']}:\n{new_cmd}")

                # if magic command includes a '%' percent convert to python code
                elif strip_line.startswith('%'):
                    cmd = strip_line[:-1].replace("%","",1).split(" ")
                    is_cmd = 0
                    is_unsupported = 0

                    # check if command is in the list of commands
                    if cmd[0] in magic_list:
                        is_cmd = 1
                        if not flags['n_i']:
                            new_import = True
                            logging.warn(f"[{translation['defwrd_warn_wrd']}] %{cmd[0]} {translation['defmsg_cmd_det_msg']}")
                        
                    # if is command, add the new command to the source  
                    if is_cmd:
                        if cmd[0] == "cd" and flags['c_m']:
                            new_cmd = f"os.chdir('{cmd[1]}')\n"
                            new_cmd_spaces = f"{spaces}os.chdir('{cmd[1]}'){cc_trailing_comment}\n"
                            check_imports(os_import,flags,'py')

                        if cmd[0] == "env" or cmd[0] == "set_env" and flags['c_m']:
                            if len(cmd) > 1 or cmd[0] == "set_env":
                                if len(cmd) == 2:
                                    if '=' in cmd[1]:
                                        new_cmd = f"os.environ['{cmd[1].split('=')[0]}'] = '{cmd[1].split('=')[1]}'\n"
                                        new_cmd_spaces = f"{spaces}os.environ['{cmd[1].split('=')[0]}'] = '{cmd[1].split('=')[1]}'{cc_trailing_comment}\n"
                                        check_imports(os_import,flags,'py')
                                    else:
                                        new_cmd = f"os.environ['{cmd[1]}']\n"
                                        new_cmd_spaces = f"{spaces}os.environ['{cmd[1]}']{cc_trailing_comment}\n"
                                        check_imports(os_import,flags,'py')
                                else:
                                    new_cmd = f"os.environ['{cmd[1]}'] = '{cmd[2]}'\n"
                                    new_cmd_spaces = f"{spaces}os.environ['{cmd[1]}'] = '{cmd[2]}'{cc_trailing_comment}\n"
                                    check_imports(os_import,flags,'py')
                            else:
                                if flags['c_m']:
                                    new_cmd = f"for k, v in os.environ.items():\n    print(f'{{k}}={{v}}')\n"
                                    new_cmd_spaces = f"{spaces}for k, v in os.environ.items():{cc_trailing_comment}\n{spaces}    print(f'{{k}}={{v}}'){cc_trailing_comment}\n"
                                    check_imports(os_import,flags,'py')

                        if flags['c_m']:
                            logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defwrd_converted_wrd']}:\n    {strip_line}  {translation['defwrd_to_wrd']}:\n    {new_cmd}")
                    else:
                        if not flags['n_c']:
                            logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defmsg_un_command_det_msg']}")
                            logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_comment_un_cmd_msg']}: {strip_line.rstrip()}")
                            is_unsupported = 1
                            new_cmd_spaces = f"{spaces}{cc_auto_comment} {strip_line}"
                        else:
                            logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defmsg_un_command_det_msg']}")
                            logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_comment_un_cmd_msg']}: {strip_line.rstrip()}")
                            new_cmd_spaces = f"{spaces}{strip_line}"
                    if flags['c_m']:   
                        source[x] = new_cmd_spaces
                    if not flags['n_c'] and is_unsupported:
                        source[x] = new_cmd_spaces
                x+=1
            result.append("%s%s" % (header_comment+reformat_metadata, ''.join(source)))
    if new_import:
        format_cell_log = '\n'.join(["  " + split_line for split_line in new_imports_cell_py.split('\n')])
        logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defmsg_add_imports_cell_msg']}\n{format_cell_log}")
        format_cell = '\n\n'.join(result)+f"\n\n{header_comment}{reformat_main_metadata}"
        update_cell = f"{new_imports_cell_py}\n{format_cell}"
    else:
        update_cell = '\n\n'.join(result)+f"\n\n{header_comment}{reformat_main_metadata}"

    return update_cell

# convert python to notebook
def py2nb(py_str, flags):

    # remove leading header comment
    if py_str.startswith(header_comment):
        py_str = py_str[len(header_comment):]

    cells = []
    chunks = py_str.split('\n\n%s' % header_comment)

    for chunk in chunks:
        new_json = {'metadata':{}}
        if chunk.startswith('# !!'):
            new_json = json.loads("\n".join([x.strip() for x in chunk.splitlines() if '# !!' in x]).replace('# !!',''))
            chunk = "\n".join([x for x in chunk.splitlines() if '# !!' not in x])
        if chunk.startswith("'''"):
            chunk = chunk.strip("'\n")
            cell_type = 'markdown'
        elif chunk.startswith('"""'):
            chunk = chunk.strip('"\n')
            cell_type = 'markdown'
        else:
            cell_type = 'code'
        if 'main_metadata' in new_json.keys():
            main_metadata = new_json['main_metadata']
        else:
            cell = {
                'cell_type': cell_type,
                'metadata': {} if 'main_metadata' in new_json else new_json['metadata'],
                'source': chunk,
            }
            if cell_type == 'code':
                cell.update({'outputs': [], 'execution_count': None})
                x = 0
                chunk = chunk.splitlines(True)
                for line in chunk:
                    spaces_in_line = len(line) - len(line.lstrip(' '))
                    spaces = ""
                    for i in range(spaces_in_line):
                        spaces+=" "
                    strip_line = line.lstrip(' ')

                    # if magic command includes a '!' [bang] use subprocess to call the command
                    if strip_line.startswith('!') and flags['c_m']:
                        cmd = strip_line[:-1].replace("!","",1).split(" ")
                        logging.warn(f"[{translation['defwrd_warn_wrd']}] !{cmd[0]} {translation['defmsg_cmd_det_msg']}")
                        new_cmd = f"    sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8')\n    print(sub_p_res)\n"
                        new_cmd_spaces = f"{spaces}sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8'){cc_trailing_comment}\n{spaces}print(sub_p_res){cc_trailing_comment}\n"
                        chunk[x] = new_cmd_spaces
                        check_imports(sp_import,flags,'ipy')
                        logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defwrd_converted_wrd']}:\n    {strip_line}  {translation['defwrd_to_wrd']}:\n{new_cmd}")

                     # if magic command includes a '%' [percent] convert to python code
                    elif strip_line.startswith('%'):
                        cmd = strip_line[:-1].replace("%","",1).split(" ")
                        is_cmd = 0
                        is_unsupported = 0

                        # check if command is in the list of commands
                        if cmd[0] in magic_list:
                            is_cmd = 1
                            if not flags['n_i']:
                                new_import = True
                                logging.warn(f"[{translation['defwrd_warn_wrd']}] %{cmd[0]} {translation['defmsg_cmd_det_msg']}")

                        if is_cmd:
                            if cmd[0] == "cd" and flags['c_m']:
                                new_cmd = f"os.chdir('{cmd[1]}')\n"
                                new_cmd_spaces = f"{spaces}os.chdir('{cmd[1]}'){cc_trailing_comment}\n"
                                check_imports(os_import,flags,'ipy')
                            
                            if cmd[0] == "env" or cmd[0] == "set_env" and flags['c_m']:
                                if len(cmd) > 1 or cmd[0] == "set_env":
                                    if len(cmd) == 2:
                                        if '=' in cmd[1]:
                                            new_cmd = f"os.environ['{cmd[1].split('=')[0]}'] = '{cmd[1].split('=')[1]}'\n"
                                            new_cmd_spaces = f"{spaces}os.environ['{cmd[1].split('=')[0]}'] = '{cmd[1].split('=')[1]}'{cc_trailing_comment}\n"
                                            check_imports(os_import,flags,'ipy')
                                        else:
                                            new_cmd = f"os.environ['{cmd[1]}']\n"
                                            new_cmd_spaces = f"{spaces}os.environ['{cmd[1]}']{cc_trailing_comment}\n"
                                            check_imports(os_import,flags,'ipy')
                                    else:
                                        new_cmd = f"os.environ['{cmd[1]}'] = '{cmd[2]}'\n"
                                        new_cmd_spaces = f"{spaces}os.environ['{cmd[1]}'] = '{cmd[2]}'{cc_trailing_comment}\n"
                                        check_imports(os_import,flags,'ipy')
                                else:
                                    if flags['c_m']:
                                        new_cmd = f"for k, v in os.environ.items():\n    print(f'{{k}}={{v}}')\n"
                                        new_cmd_spaces = f"{spaces}for k, v in os.environ.items():{cc_trailing_comment}\n{spaces}    print(f'{{k}}={{v}}'){cc_trailing_comment}\n"
                                        check_imports(os_import,flags,'ipy')

                            if flags['c_m']:
                                logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defwrd_converted_wrd']}:\n    {strip_line}  {translation['defwrd_to_wrd']}:\n    {new_cmd}")
                        else:
                            if not flags['n_c']:
                                logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defmsg_un_command_det_msg']}")
                                logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_comment_un_cmd_msg']}: {strip_line.rstrip()}")
                                is_unsupported = 1
                                new_cmd_spaces = f"{spaces}{cc_auto_comment} {strip_line}"
                            else:
                                logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defmsg_un_command_det_msg']}")
                                logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_comment_un_cmd_msg']}: {strip_line.rstrip()}")
                                new_cmd_spaces = f"{spaces}{strip_line}"
                        if flags['c_m']:   
                            chunk[x] = new_cmd_spaces
                        if not flags['n_c'] and is_unsupported:
                            chunk[x] = new_cmd_spaces
                    x+=1
                cell['source'] = chunk
            cells.append(cell)

    notebook = {
        'cells': cells,
        'metadata': main_metadata,
          'nbformat': 4,
          'nbformat_minor': 4
    }

    if globals()['new_import']:
        logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defmsg_add_imports_cell_msg']}")
        notebook['cells'].insert(0, {
                'cell_type': 'code',
                'metadata': new_imports_meta_ipy,
                'source': [e+'\n' for e in new_imports_cell_ipy.split('\n') if e]
            })

    return notebook


def convert(in_file, out_file, extra_flags):
    _, in_ext = os.path.splitext(in_file)
    _, out_ext = os.path.splitext(out_file)

    if in_ext == '.ipynb' and out_ext == '.py':
        with open(in_file, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        py_str = nb2py(notebook, extra_flags)
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(py_str)

    elif in_ext == '.py' and out_ext == '.ipynb':
        with open(in_file, 'r', encoding='utf-8') as f:
            py_str = f.read()
        notebook = py2nb(py_str, extra_flags)
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2)

    else:
        logging.critical(translation['defmsg_file_ext_msg'])
        sys.exit(1)


def main():
    global translation
    argv = sys.argv[1:]
    extra_flags = None if not argv[2:] else argv[2:]
    lang_flag_used = None if not extra_flags else any(e for e in extra_flags if e.startswith('--lang=') or e.startswith('-l='))

    if extra_flags and lang_flag_used:
        parse_lang = [e for e in extra_flags if e.startswith('--lang=') or e.startswith('-l=')]
        if parse_lang:
            new_lang = parse_lang[0].split('=')[1]
            get_language(new_lang)
        else:
            logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defmsg_no_lang_msg']} --lang=?? (-l=??)")

    if len(argv) == 0:
        logging.error(translation['defmsg_specify_file_msg'])
        logging.error(translation['defmsg_usage_msg'])
        sys.exit(1)
    if len(argv) == 1:
        argv.append('out')

    _, in_file_ext = os.path.splitext(argv[0])
    _, out_file_ext = os.path.splitext(argv[1])

    in_is_py = False
    in_is_ipynb = False

    if argv[0] in help_flags:
        logging.info(translation['defmsg_help_called_msg'])
        for key, value in flags_desc.items():
            print(key, value)
        sys.exit(1)
    if in_file_ext == '.py':
        in_is_py = True
    elif in_file_ext == '.ipynb':
        in_is_ipynb = True
    else:
        logging.error(f"{translation['defwrd_input_wrd']} {translation['defmsg_file_ext_msg']}")
        sys.exit(1)
    if argv[1] == 'out':
        if in_is_ipynb:
            argv[1] += '.py'
            out_file_ext = '.py'
        if in_is_py:
            argv[1] += '.ipynb'
            out_file_ext = '.ipynb'
        logging.warn(f"{translation['defmsg_set_output_ext_msg']} {argv[1]}")
    #default flags
    if in_is_ipynb:
        convert_magic = True
        no_comment = False
        no_imports = False
    if in_is_py:
        convert_magic = False
        no_comment = True
        no_imports = True
    if out_file_ext != '.ipynb' and out_file_ext != '.py':
        logging.error(f"{translation['defwrd_output_wrd']} {translation['defmsg_file_ext_msg']}")
        sys.exit(1)
    if extra_flags:
        test_flags = [element for element in extra_flags if element not in flags_list]
        if test_flags and not lang_flag_used:
            logging.info(translation['defmsg_help_called_msg'])
            for key, value in flags_desc.items():
                print(key, value)
            sys.exit(1)

        # check for --convert-magic and --retain-magic flags
        if '--convert-magic' in extra_flags or '-cm' in extra_flags or '--retain-magic' in extra_flags or '-rm' in extra_flags:
            # if --retain-magic and --convert-magic flag are present 
            # then --convert-magic is negated for --retain-magic [-cm -rm = -rm]
            if '--retain-magic' in extra_flags or '-rm' in extra_flags:
                if '--convert-magic' in extra_flags or '-cm' in extra_flags:
                    logging.warn(f"[{translation['defwrd_warn_wrd']}] --retain-magic (-rm) {translation['defmsg_rm_over_cm_msg']} --convert-magic (-cm)")
                    logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defmsg_rm_over_cm_fall_msg']} --retain-magic (-rm)")
                logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_convert_magic_msg']}")
                convert_magic = False
            else:
                logging.info(f"[{translation['defwrd_ok_wrd']}]   {translation['defmsg_convert_magic_msg']}")
                convert_magic = True
        #just an extra check to report if --convert-magic flag isnt present
        else:
            if convert_magic:
                logging.info(f"[{translation['defwrd_ok_wrd']}]   {translation['defmsg_convert_magic_msg']}")
            else:
                logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_convert_magic_msg']}")

        # check for --no-comment , --auto-comment
        if '--no-comment' in extra_flags or '-nc' in extra_flags or '--auto-comment' in extra_flags or '-ac' in extra_flags:
            # if --auto-comment and --no-comment flags are present
            # then --no-comment is negated for --auto-comment [-nc -ac = -ac]
            if '--auto-comment' in extra_flags or '-ac' in extra_flags:
                if '--no-comment' in extra_flags or '-nc' in extra_flags:
                    logging.warn(f"[{translation['defwrd_warn_wrd']}] --auto-comment (-ac) {translation['defmsg_ac_over_nc_msg']} --no-comment (-nc)")
                    logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defmsg_ac_over_nc_fall_msg']} --auto-comment (-ac)")
                logging.info(f"[{translation['defwrd_ok_wrd']}]   {translation['defmsg_un_comment_msg']}")
                no_comment = False
            else:
                no_comment = True
                logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_un_comment_msg']}")
        #just an extra check to report if --no-comment flag isnt present
        else:
            if no_comment:
                logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_un_comment_msg']}")
            else:
                logging.info(f"[{translation['defwrd_ok_wrd']}]   {translation['defmsg_un_comment_msg']}")

        # check for --no-imports flag
        if '--no-imports' in extra_flags or '-ni' in extra_flags:
            logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_imports_msg']}")
            no_imports = True
        else:
            if not convert_magic:
                if '--retain-magic' in extra_flags or '-rm' in extra_flags:
                    logging.warn(f"[{translation['defwrd_warn_wrd']}] --retain-magic (-rm) {translation['defmsg_ret_mag_det_msg']}")
                else:
                    logging.warn(f"[{translation['defwrd_warn_wrd']}] {translation['defmsg_def_set_ret_mag_msg']}")
                no_imports = True
                logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_imports_msg']}")
            else:
                no_imports = False
                logging.info(f"[{translation['defwrd_ok_wrd']}]   {translation['defmsg_imports_msg']}")

        # check for --no-outputs flag
        if '--outputs' in extra_flags or '-o' in extra_flags:
            logging.info(f"[{translation['defwrd_ok_wrd']}]   {translation['defmsg_outputs_msg']}")
        else:
            logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_outputs_msg']}")
            logger.removeHandler(logger.handlers[-1])

    # set defaults per files if no flags are set
    else:
        if in_is_ipynb:
            logging.info(f"[{translation['defwrd_ok_wrd']}]   {translation['defmsg_convert_magic_msg']}")
            logging.info(f"[{translation['defwrd_ok_wrd']}]   {translation['defmsg_un_comment_msg']}")
            logging.info(f"[{translation['defwrd_ok_wrd']}]   {translation['defmsg_imports_msg']}")
        else:
            logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_convert_magic_msg']}")
            logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_un_comment_msg']}")
            logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_imports_msg']}")
        logging.info(f"[{translation['defwrd_not_wrd']}]  {translation['defmsg_outputs_msg']}")
        logger.removeHandler(logger.handlers[-1])
    
    flags = {'c_m': convert_magic, 'n_c': no_comment , 'n_i': no_imports}

    print(f"\n{translation['defwrd_convert_wrd']} {argv[0]} {translation['defwrd_to_wrd']} {argv[1]}")

    start_time = time.perf_counter()
    convert(in_file=argv[0], out_file=argv[1], extra_flags=flags)
    end_time = time.perf_counter()

    print(f"{translation['defwrd_finished_wrd']}")
    print(f"{translation['defmsg_convert_time_msg']} {round(end_time - start_time, 6)} {translation['defwrd_seconds_wrd']}")
    print(f"\n{translation['defmsg_log_file_msg']}:\n{os.getcwd()}{os.sep}{log_file}")

if __name__ == '__main__':
    main()
