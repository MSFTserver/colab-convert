import json
import sys
from os import path

header_comment = '# %%\n'
magic_list = ["cd","env","set_env"]
help_flags = ['--help', '-h', '?']
flags_list = ['--auto-comment', '-ac', '--no-comment', '-nc', '--retain-magic', '-rm', '--convert-magic', '-cm','--no-imports', '-ni', '--outputs', '-o', '--log', '-l']
flags_desc = {
    'Colab-Convert': '\nall flags are optional and have set defaults for best results\nuse flags to enable or disable certain functions on by default\n',
    'Usage:': 'colab-convert <input_file> <output_file> <flags>',
    'Example:': 'colab-convert in.ipynb out.py -nc -rm -o\n',
    '<input_file>:': 'input file to convert',
    '<output_file>:': 'output file to write to',
    '<flags>:': 'extra flags to pass to the converter\n',
    '--help': '(-h)\n  Show this help message\n',
    'Default Flags Set (defaults are determined by input file)': '\n  ipynb input file:\n    [YES] convert magic , [YES] auto comment , [YES] imports , [NO] Outputs\n  py input file:\n    [NO] convert magic , [NO] auto comment , [N/A] imports , [NO] Outputs\n',
    'Available Flags': '\n  toggle certain items on or off\n',
    '  --retain-magic': ' (-rm)  : Keep magic commands in the output\n      .py default    [ON]\n      .ipynb default [OFF]',
    '  --convert-magic': ' (-cm) : Convert magic commands to python code\n      .py default    [OFF]\n      .ipynb default [ON]',
    '  --auto-comment': ' (-ac)  : Convert unsupported magic commands to comments\n      .py default    [OFF]\n      .ipynb default [ON]',
    '  --no-comment': ' (-nc)    : Keep unsupported magic commands\n      .py default    [ON]\n      .ipynb default [OFF]',
    '  --no-imports': ' (-ni)    : Do not add imports from converted magic commands\n      .py default    [OFF]\n      .ipynb default [OFF]',
    '  --outputs': ' (-o)        : Outputs console logs of conversions and commented lines.\n      .py default    [OFF]\n      .ipynb default [OFF]',
    '  --log': ' (-l)            : Same as Outputs\n      .py default    [OFF]\n      .ipynb default [OFF]',
}

def nb2py(notebook, flags):
    result = []
    cells = notebook['cells']

    main_metadata = json.dumps(notebook['metadata'],indent=2).split("\n")
    reformat_main_metadata = '# !! {"main_metadata":'

    new_imports_meta = '# !! {"metadata":{\n# !!   "id":"colab-convert"\n# !! }'+"}\n"
    new_imports_cell = f"{header_comment}{new_imports_meta}\n#<cc-imports>\n"
    new_import = False
    os_added = False
    sp_added = False

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
                    new_cmd = f"    sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8') #<cc-cm>\n    print(sub_p_res)\n"
                    new_cmd_spaces = f"{spaces}sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8') #<cc-cm>\n{spaces}print(sub_p_res) #<cc-cm>\n"
                    source[x] = new_cmd_spaces
                    if not flags['n_i']:
                        if not sp_added:
                            new_import = True
                            sp_added = True
                            new_imports_cell+=f"import subprocess\n"
                    if not flags['n_o']:
                        print(f'  converted:\n    {strip_line}  to:\n  {new_cmd}')

                # if magic command includes a '%' percent convert to python code
                elif strip_line.startswith('%'):
                    cmd = strip_line[:-1].replace("%","",1).split(" ")
                    is_cmd = 0

                    # check if command is in the list of commands
                    if cmd[0] in magic_list:
                        is_cmd = 1
                        if not flags['n_i']:
                            new_import = True
                            if not flags['n_o']:
                                print(f'%{cmd[0]} command detected')
                        
                    # if is command, add the new command to the source  
                    if is_cmd:
                        if cmd[0] == "cd" and flags['c_m']:
                            new_cmd = f"os.chdir('{cmd[1]}')\n"
                            new_cmd_spaces = f"{spaces}os.chdir('{cmd[1]}') #<cc-cm>\n"
                            if not flags['n_i']:
                                if not os_added:
                                    os_added = True
                                    new_imports_cell+="import os\n"

                        if cmd[0] == "env" or cmd[0] == "set_env" and flags['c_m']:
                            if len(cmd) > 1 or cmd[0] == "set_env":
                                if len(cmd) == 2:
                                    if '=' in cmd[1]:
                                        new_cmd = f"os.environ['{cmd[1].split('=')[0]}'] = '{cmd[1].split('=')[1]}'\n"
                                        new_cmd_spaces = f"{spaces}os.environ['{cmd[1].split('=')[0]}'] = '{cmd[1].split('=')[1]}' #<cc-cm>\n"
                                        if not flags['n_i']:
                                            if not os_added:
                                                os_added = True
                                                new_imports_cell+="import os\n"
                                    else:
                                        new_cmd = f"os.environ['{cmd[1]}']\n"
                                        new_cmd_spaces = f"{spaces}os.environ['{cmd[1]}'] #<cc-cm>\n"
                                        if not flags['n_i']:
                                            if not os_added:
                                                os_added = True
                                                new_imports_cell+="import os\n"
                                else:
                                    new_cmd = f"os.environ['{cmd[1]}'] = '{cmd[2]}'\n"
                                    new_cmd_spaces = f"{spaces}os.environ['{cmd[1]}'] = '{cmd[2]}' #<cc-cm>\n"
                                    if not flags['n_i']:
                                        if not os_added:
                                            os_added = True
                                            new_imports_cell+="import os\n"
                            else:
                                if flags['c_m']:
                                    new_cmd = f"for k, v in os.environ.items():\n"+"        print(f'{k}={v}')\n"
                                    new_cmd_spaces = f"{spaces}for k, v in os.environ.items(): #<cc-cm>\n{spaces}"+"    print(f'{k}={v}') #<cc-cm>\n"
                                    if not flags['n_i']:
                                        if not os_added:
                                            os_added = True
                                            new_imports_cell+="import os\n"

                        if not flags['n_o']:
                            print(f'  converted:\n    {strip_line}  to:\n    {new_cmd}')
                    else:
                        if not flags['n_c']:
                            if not flags['n_o']:
                                print(f'unsupported command is detected!')
                                print(f'  commenting out unsupported command:\n    {strip_line}')
                            new_cmd_spaces = f"{spaces}#<cc-ac> {strip_line}"
                        else:
                            if not flags['n_o']:
                                print(f'unsupported command is detected!')
                                print(f'  not commenting out unsupported command:\n    {strip_line}')
                            new_cmd_spaces = f"{spaces}{strip_line}"
                    
                    source[x] = new_cmd_spaces
                x+=1
            result.append("%s%s" % (header_comment+reformat_metadata, ''.join(source)))
    if new_import:
        format_cell = f'\n\n'.join(result)+f'\n\n{header_comment}{reformat_main_metadata}'
        update_cell = f'{new_imports_cell}\n{format_cell}'
    else:
        update_cell = '\n\n'.join(result)+f'\n\n{header_comment}{reformat_main_metadata}'

    return update_cell

def py2nb(py_str, flags):
    # remove leading header comment
    if py_str.startswith(header_comment):
        py_str = py_str[len(header_comment):]

    cells = []
    chunks = py_str.split('\n\n%s' % header_comment)

    new_imports_meta = {'id':'colab-convert'}
    new_imports_cell = f"#<cc-imports>\n"
    new_import = False
    os_added = False
    sp_added = False

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
                        new_cmd_spaces = f"{spaces}sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8') #<cc-cm>\n{spaces}print(sub_p_res) #<cc-cm>\n"
                        chunk[x] = new_cmd_spaces
                        if not flags['n_i']:
                            if not sp_added:
                                new_import = True
                                sp_added = True
                                new_imports_cell+=f"import subprocess\n"
                        if not flags['n_o']:
                            print(f'  converted:\n    {strip_line}  to:\n{new_cmd}')

                     # if magic command includes a '%' [percent] convert to python code
                    elif strip_line.startswith('%'):
                        cmd = strip_line[:-1].replace("%","",1).split(" ")
                        is_cmd = 0

                        # check if command is in the list of commands
                        if cmd[0] in magic_list:
                            is_cmd = 1
                        if not flags['n_o']:
                            print(f'%{cmd[0]} command detected')

                        if is_cmd:
                            if cmd[0] == "cd" and flags['c_m']:
                                new_cmd = f"os.chdir('{cmd[1]}')\n"
                                new_cmd_spaces = f"{spaces}os.chdir('{cmd[1]}') #<cc-cm>\n"
                                if not flags['n_i']:
                                    if not os_added:
                                        os_added = True
                                        new_imports_cell+="import os\n"
                            
                            if cmd[0] == "env" or cmd[0] == "set_env" and flags['c_m']:
                                if len(cmd) > 1 or cmd[0] == "set_env":
                                    if len(cmd) == 2:
                                        if '=' in cmd[1]:
                                            new_cmd = f"os.environ['{cmd[1].split('=')[0]}'] = '{cmd[1].split('=')[1]}'\n"
                                            new_cmd_spaces = f"{spaces}os.environ['{cmd[1].split('=')[0]}'] = '{cmd[1].split('=')[1]}' #<cc-cm>\n"
                                            if not flags['n_i']:
                                                if not os_added:
                                                    os_added = True
                                                    new_imports_cell+="import os\n"
                                        else:
                                            new_cmd = f"os.environ['{cmd[1]}']\n"
                                            new_cmd_spaces = f"{spaces}os.environ['{cmd[1]}'] #<cc-cm>\n"
                                            if not flags['n_i']:
                                                if not os_added:
                                                    os_added = True
                                                    new_imports_cell+="import os\n"
                                    else:
                                        new_cmd = f"os.environ['{cmd[1]}'] = '{cmd[2]}'\n"
                                        new_cmd_spaces = f"{spaces}os.environ['{cmd[1]}'] = '{cmd[2]}' #<cc-cm>\n"
                                        if not flags['n_i']:
                                            if not os_added:
                                                os_added = True
                                                new_imports_cell+="import os\n"
                                else:
                                    if flags['c_m']:
                                        new_cmd = f"for k, v in os.environ.items():\n"+"        print(f'{k}={v}')\n"
                                        new_cmd_spaces = f"{spaces}for k, v in os.environ.items(): #<cc-cm>\n{spaces}"+"    print(f'{k}={v}') #<cc-cm>\n"
                                        if not flags['n_i']:
                                            if not os_added:
                                                os_added = True
                                                new_imports_cell+="import os\n"

                            if not flags['n_o'] and flags['c_m']:
                                print(f'  converted:\n    {strip_line}  to:\n    {new_cmd}')
                        else:
                            if not flags['n_c']:
                                if not flags['n_o']:
                                    print(f'unsupported command is detected!')
                                    print(f'  commenting out unsupported command:\n    {strip_line}')
                                new_cmd_spaces = f"{spaces}#<cc-ac> {strip_line}"
                            else:
                                if not flags['n_o']:
                                    print(f'unsupported command is detected!')
                                    print(f'  not commenting out unsupported command:\n    {strip_line}')
                                new_cmd_spaces = f"{spaces}{strip_line}"
                        if flags['c_m']:   
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

    if new_import:
        notebook['cells'].insert(0, {
                'cell_type': 'code',
                'metadata': new_imports_meta,
                'source': [e+'\n' for e in new_imports_cell.split('\n') if e]
            })

    return notebook


def convert(in_file, out_file, extra_flags):
    _, in_ext = path.splitext(in_file)
    _, out_ext = path.splitext(out_file)

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
    argv = sys.argv[1:]

    if len(argv) == 0:
        print("please specify atleast one file to convert")
        print('Usage: colab-convert <input_file> <output_file> <extra_flags>')
        sys.exit(1)
    if len(argv) == 1:
        argv.append('out')

    _, in_file_ext = path.splitext(argv[0])
    _, out_file_ext = path.splitext(argv[1])

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
        print('Input file must be .ipynb or .py')
        sys.exit(1)
    if argv[1] == 'out':
        if in_is_ipynb:
            argv[1] += '.py'
            out_file_ext = '.py'
        if in_is_py:
            argv[1] += '.ipynb'
            out_file_ext = '.ipynb'
        print(f'setting output file to {argv[1]}')
    #default flags
    if in_is_ipynb:
        no_outputs = True
        convert_magic = True
        no_comment = False
        no_imports = False
    if in_is_py:
        no_outputs = True
        convert_magic = False
        no_comment = True
        no_imports = False
    if out_file_ext != '.ipynb' and out_file_ext != '.py':
        print('Output file must be .ipynb or .py')
        sys.exit(1)
    if extra_flags:
        test_flags = [element for element in extra_flags if element not in flags_list]
        if test_flags:
            for key, value in flags_desc.items():
                print(key, value)
            sys.exit(1)

        if '--outputs' in extra_flags or '--log' in extra_flags or '-l' in extra_flags or '-o' in extra_flags:
            no_outputs = False
            print('[OK] showing outputs from converter')
        else:
            print('[NOT] showing outputs from converter!a')

        if '--convert-magic' in extra_flags or '-cm' in extra_flags or '--retain-magic' in extra_flags or '-rm' in extra_flags:
            if '--retain-magic' in extra_flags or '-rm' in extra_flags:
                if '--convert-magic' in extra_flags or '-cm' in extra_flags:
                    print('\n    --retain-magic (-rm) takes presidence over --convert-magic (-cm)\n'+'    using --retain-magic (-rm)\n')
                print('[NOT] converting magic commands!')
                convert_magic = False
            else:
                print('[OK] converting magic commands')
                convert_magic = True
        else:
            if convert_magic:
                print('[OK] converting magic commands')
            else:
                print('[NOT] converting magic commands!')

        if '--no-comment' in extra_flags or '-nc' in extra_flags or '--auto-comment' in extra_flags or '-ac' in extra_flags:
            if not '--convert-magic' in extra_flags and not '-cm' in extra_flags and '--retain-magic' in extra_flags and not '-rm' in extra_flags:
                print('\n    --convert-magic (-cm) is required when --no-comment (-nc) or --auto-comment (-ac) are used')
                print('    auto set to flag --convert-magic (-cm)\n')
                convert_magic = True
            if '--auto-comment' in extra_flags or '-ac' in extra_flags:
                if '--no-comment' in extra_flags or '-nc' in extra_flags and not '--retain-magic' in extra_flags and not '-rm' in extra_flags:
                    print('\n    --auto-comment (-ac) takes presidence over --no-comment (-nc)\n'+'    using --auto-comment (-ac)\n')
                if '--retain-magic' in extra_flags or '-rm' in extra_flags:
                    print('\n    --retain-magic (-rm) takes presidence over --auto-comment (-ac)\n'+'    using --no-comment (-nc)\n')
                    print('[NOT] commenting out unsupported magic commands!')
                    no_comment = True
                else:
                    print('[OK] commenting out unsupported magic commands')
                    no_comment = False
            else:
                no_comment = True
                print('[NOT] commenting out unsupported magic commands!')
        else:
            if no_comment:
                print('[NOT] commenting out unsupported magic commands!')
            else:
                print('[OK] commenting out unsupported magic commands')

        if '--no-imports' in extra_flags or '-ni' in extra_flags:
            print('[NOT] making new imports')
            no_imports = True
        else:
            print('[OK] making new imports')

    else:
        if in_is_ipynb:
            print('[NOT] showing outputs from converter')
            print('[OK] converting magic commands')
            print('[OK] commenting out unsupported magic commands')
            print('[OK] keeping imports')
        if in_is_py:
            print('[NOT] showing outputs from converter')
            print('[NOT] converting magic commands!')
            print('[NOT] commenting out unsupported magic commands!')
            print('[OK] keeping imports')
    
    flags = {'n_o': no_outputs, 'c_m': convert_magic, 'n_c': no_comment , 'n_i': no_imports}

    convert(in_file=argv[0], out_file=argv[1], extra_flags=flags)


if __name__ == '__main__':
    main()
