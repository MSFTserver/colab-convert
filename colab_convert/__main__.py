import json, sys, time, os, logging

# set up logging, adds new logger mode and level
log_file = 'cc-outputs.log'
methodName = 'PRINTOUT'.lower()
if hasattr(logging, 'PRINTOUT'):
    raise AttributeError('{} already defined in logging module'.format('PRINTOUT'))
if hasattr(logging, methodName):
    raise AttributeError('{} already defined in logging module'.format(methodName))
if hasattr(logging.getLoggerClass(), methodName):
    raise AttributeError('{} already defined in logger class'.format(methodName))
def logForLevel(self, message, *args, **kwargs):
    if self.isEnabledFor(25):
        self._log(25, message, args, **kwargs)
def logToRoot(message, *args, **kwargs):
    logging.log(25, message, *args, **kwargs)
logging.addLevelName(25, 'PRINTOUT')
setattr(logging, 'PRINTOUT', 25)
setattr(logging.getLoggerClass(), methodName, logForLevel)
setattr(logging, methodName, logToRoot)
logger= logging.getLogger()
handler = logging.FileHandler(log_file, 'a', 'utf-8')
handler.setFormatter(logging.Formatter('%(asctime)s : %(message)s'))
logger.addHandler(handler)

# default conversion code
header_comment = '# %%\n'
cc_auto_comment = '#<cc-ac>'
cc_trailing_comment = ' #<cc-cm>'
cc_import_comment = '#<cc-imports>\n'
default_env_cmd = [f'for k, v in os.environ.items():{cc_trailing_comment}\n',f"    print(f'{{k}}={{v}}'){cc_trailing_comment}\n"]
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
magic_list = ["cd","env","set_env"]
help_flags = ['--help', '-h', '?']
flags_list = ['--auto-comment', '-ac', '--no-comment', '-nc', '--retain-magic', '-rm', '--convert-magic', '-cm','--no-imports', '-ni', '--outputs', '-o']
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
            reformat_main_metadata+=f'# !! {key}\n'
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
                reformat_metadata+=f'# !! {key}\n'
    
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
                    new_cmd = f"    sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8')\n    print(sub_p_res)\n"
                    new_cmd_spaces = f"{spaces}sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8'){cc_trailing_comment}\n{spaces}print(sub_p_res){cc_trailing_comment}\n"
                    source[x] = new_cmd_spaces
                    check_imports(sp_import,flags,'py')
                    logging.printout(f'[WARN] converted:\n    {strip_line}  to:\n{new_cmd}')

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
                            logging.printout(f'[WARN] %{cmd[0]} command detected')
                        
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
                                    new_cmd = f"{default_env_cmd[0]}    {default_env_cmd[1]}".replace(cc_trailing_comment,"")
                                    new_cmd_spaces = f"{spaces}{default_env_cmd[0]}{spaces}{default_env_cmd[1]}"
                                    check_imports(os_import,flags,'py')

                        if flags['c_m']:
                            logging.printout(f'[WARN] converted:\n    {strip_line}  to:\n    {new_cmd}')
                    else:
                        if not flags['n_c']:
                            logging.printout('[WARN] unsupported command is detected!')
                            logging.printout(f'[WARN] commenting out unsupported command: {strip_line.rstrip()}')
                            is_unsupported = 1
                            new_cmd_spaces = f"{spaces}{cc_auto_comment} {strip_line}"
                        else:
                            logging.printout('[WARN] unsupported command is detected!')
                            logging.printout(f'[WARN] NOT commenting out unsupported command: {strip_line.rstrip()}')
                            new_cmd_spaces = f"{spaces}{strip_line}"
                    if flags['c_m']:   
                        source[x] = new_cmd_spaces
                    if not flags['n_c'] and is_unsupported:
                        source[x] = new_cmd_spaces
                x+=1
            result.append("%s%s" % (header_comment+reformat_metadata, ''.join(source)))
    if new_import:
        format_cell_log = '\n'.join(["  " + split_line for split_line in new_imports_cell_py.split('\n')])
        logging.printout(f'[WARN] adding new imports to the top of the notebook\n{format_cell_log}')
        format_cell = f'\n\n'.join(result)+f'\n\n{header_comment}{reformat_main_metadata}'
        update_cell = f'{new_imports_cell_py}\n{format_cell}'
    else:
        update_cell = '\n\n'.join(result)+f'\n\n{header_comment}{reformat_main_metadata}'

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
                        new_cmd = f"    sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8')\n    print(sub_p_res)\n"
                        new_cmd_spaces = f"{spaces}sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8'){cc_trailing_comment}\n{spaces}print(sub_p_res){cc_trailing_comment}\n"
                        chunk[x] = new_cmd_spaces
                        check_imports(sp_import,flags,'ipy')
                        logging.printout(f'[WARN] converted:\n    {strip_line}  to:\n{new_cmd}')

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
                                logging.printout(f'[WARN] %{cmd[0]} command detected')

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
                                        new_cmd = f"{default_env_cmd[0]}    {default_env_cmd[1]}".replace(cc_trailing_comment,"")
                                        new_cmd_spaces = f"{spaces}{default_env_cmd[0]}{spaces}{default_env_cmd[1]}"
                                        check_imports(os_import,flags,'ipy')

                            if flags['c_m']:
                                logging.printout(f'[WARN] converted:\n    {strip_line}  to:\n    {new_cmd}')
                        else:
                            if not flags['n_c']:
                                logging.printout(f'[WARN] unsupported command is detected!',)
                                logging.printout(f'[WARN] commenting out unsupported command: {strip_line.rstrip()}')
                                is_unsupported = 1
                                new_cmd_spaces = f"{spaces}{cc_auto_comment} {strip_line}"
                            else:
                                logging.printout(f'[WARN] unsupported command is detected!')
                                logging.printout(f'[WARN] not commenting out unsupported command: {strip_line.rstrip()}')
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
        logging.printout('[WARN] adding new imports to the top of the notebook')
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
        raise(Exception('Extensions must be .ipynb and .py or vice versa'))


def main():
    logger.setLevel(logging.INFO)
    logging.info('---------------------------')
    logging.info('----------[START]----------')
    logging.info('---------------------------')
    logger.addHandler(logging.StreamHandler(sys.stdout))
    argv = sys.argv[1:]

    if len(argv) == 0:
        logging.error("please specify atleast one file to convert")
        logging.error('Usage: colab-convert <input_file> <output_file> <extra_flags>')
        sys.exit(1)
    if len(argv) == 1:
        argv.append('out')

    _, in_file_ext = os.path.splitext(argv[0])
    _, out_file_ext = os.path.splitext(argv[1])

    in_is_py = False
    in_is_ipynb = False
    extra_flags = None if not argv[2:] else argv[2:]

    if argv[0] in help_flags:
        for key, value in flags_desc.items():
            print(key, value)
        sys.exit(1)
    if in_file_ext == '.py':
        in_is_py = True
    elif in_file_ext == '.ipynb':
        in_is_ipynb = True
    else:
        logging.error('Input file must be .ipynb or .py')
        sys.exit(1)
    if argv[1] == 'out':
        if in_is_ipynb:
            argv[1] += '.py'
            out_file_ext = '.py'
        if in_is_py:
            argv[1] += '.ipynb'
            out_file_ext = '.ipynb'
        logging.warn(f'setting output file to {argv[1]}')
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
        logging.error('Output file must be .ipynb or .py')
        sys.exit(1)
    if extra_flags:
        test_flags = [element for element in extra_flags if element not in flags_list]
        if test_flags:
            for key, value in flags_desc.items():
                print(key, value)
            sys.exit(1)

        # check for --convert-magic and --retain-magic flags
        if '--convert-magic' in extra_flags or '-cm' in extra_flags or '--retain-magic' in extra_flags or '-rm' in extra_flags:
            # if --retain-magic and --convert-magic flag are present 
            # then --convert-magic is negated for --retain-magic [-cm -rm = -rm]
            if '--retain-magic' in extra_flags or '-rm' in extra_flags:
                if '--convert-magic' in extra_flags or '-cm' in extra_flags:
                    logging.warn('[WARN] --retain-magic (-rm) takes presidence over --convert-magic (-cm)')
                    logging.warn('[WARN] using --retain-magic (-rm)')
                logging.info('[NOT]  converting magic commands!')
                convert_magic = False
            else:
                logging.info('[OK]   converting magic commands')
                convert_magic = True
        #just an extra check to report if --convert-magic flag isnt present
        else:
            if convert_magic:
                logging.info('[OK]   converting magic commands')
            else:
                logging.info('[NOT]  converting magic commands!')

        # check for --no-comment , --auto-comment
        if '--no-comment' in extra_flags or '-nc' in extra_flags or '--auto-comment' in extra_flags or '-ac' in extra_flags:
            # if --auto-comment and --no-comment flags are present
            # then --no-comment is negated for --auto-comment [-nc -ac = -ac]
            if '--auto-comment' in extra_flags or '-ac' in extra_flags:
                if '--no-comment' in extra_flags or '-nc' in extra_flags:
                    logging.warn('[WARN] --auto-comment (-ac) takes presidence over --no-comment (-nc)')
                    logging.warn('[WARN] using --auto-comment (-ac)')
                logging.info('[OK]   commenting out unsupported magic commands')
                no_comment = False
            else:
                no_comment = True
                logging.info('[NOT]  commenting out unsupported magic commands!')
        #just an extra check to report if --no-comment flag isnt present
        else:
            if no_comment:
                logging.info('[NOT]  commenting out unsupported magic commands!')
            else:
                logging.info('[OK]   commenting out unsupported magic commands')

        # check for --no-imports flag
        if '--no-imports' in extra_flags or '-ni' in extra_flags:
            logging.info('[NOT]  keeping new imports made by cc')
            no_imports = True
        else:
            if not convert_magic:
                if '--retain-magic' in extra_flags or '-rm' in extra_flags:
                    logging.warn('[WARN] --retain-magic is detected, new imports will NOT be made')
                else:
                    logging.warn('[WARN] default settings is retaining magic commands')
                no_imports = True
                logging.info('[NOT]  keeping new imports made by cc')
            else:
                no_imports = False
                logging.info('[OK]   keeping new imports made by cc')

        # check for --no-outputs flag
        if '--outputs' in extra_flags or '-o' in extra_flags:
            logging.info('[OK]   showing outputs from cc')
        else:
            logging.info('[NOT]  showing outputs from cc!')
            logger.removeHandler(logger.handlers[-1])

    # set defaults per files if no flags are set
    else:
        if in_is_ipynb:
            logging.info('[NOT]  showing outputs from cc')
            logging.info('[OK]   converting magic commands')
            logging.info('[OK]   commenting out unsupported magic commands')
            logging.info('[OK]   keeping new imports made by cc')
            logger.removeHandler(logger.handlers[-1])
        if in_is_py:
            logging.info('[NOT]  showing outputs from cc')
            logging.info('[NOT]  converting magic commands!')
            logging.info('[NOT]  commenting out unsupported magic commands!')
            logging.info('[NOT]  keeping new imports made by cc')
            logger.removeHandler(logger.handlers[-1])
    
    flags = {'c_m': convert_magic, 'n_c': no_comment , 'n_i': no_imports}

    print(f'\nconverting {argv[0]} to {argv[1]}')

    start_time = time.perf_counter()
    convert(in_file=argv[0], out_file=argv[1], extra_flags=flags)
    end_time = time.perf_counter()

    print('Finished!')
    print(f'conversion took {round(end_time - start_time, 6)} seconds')
    print(f'\nlog file created:\n{os.getcwd()}{os.sep}{log_file}')

if __name__ == '__main__':
    main()
