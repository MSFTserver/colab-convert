import json
import sys
from os import path

header_comment = '# %%\n'

def nb2py(notebook, args):
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

            if args['c_m']:
                for line in source:
                    spaces_in_line = len(line) - len(line.lstrip(' '))
                    spaces = ""
                    for i in range(spaces_in_line):
                        spaces+=" "
                    strip_line = line.lstrip(' ')
                    
                    # if magic command includes a '!' bang use subprocess to call the command
                    if strip_line.startswith('!'):
                        cmd = strip_line[:-1].replace("!","",1).split(" ")
                        new_cmd = f"    sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8') #<cc-cm>\n    print(sub_p_res) #<cc-cm>\n"
                        new_cmd_spaces = f"{spaces}sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8') #<cc-cm>\n{spaces}print(sub_p_res) #<cc-cm>\n"
                        source[x] = new_cmd_spaces
                        if not sp_added:
                            new_import = True
                            sp_added = True
                            new_imports_cell+=f"import subprocess\n"
                        if not args['n_o']:
                            print(f'  converted:\n    {strip_line}  to:\n  {new_cmd}')

                    # if magic command includes a '%' percent convert to python code
                    elif strip_line.startswith('%'):
                        cmd = strip_line[:-1].replace("%","",1).split(" ")
                        is_cmd = 0

                        # check if command is in the list of commands
                        if cmd[0] in ["cd","env","set_env"]:
                            is_cmd = 1
                            new_import = True
                            if not args['n_o']:
                                print(f'%{cmd[0]} command detected')
                        
                        # if is command, add the new command to the source  
                        if is_cmd:
                            if cmd[0] == "cd":
                                new_cmd = f"os.chdir('{cmd[1]}') #<cc-cm>\n"
                                new_cmd_spaces = f"{spaces}os.chdir('{cmd[1]}') #<cc-cm>\n"
                                if not os_added:
                                    os_added = True
                                    new_imports_cell+="import os\n"

                            if cmd[0] == "env" or cmd[0] == "set_env":
                                if len(cmd) > 1 or cmd[0] == "set_env":
                                    if len(cmd) == 2:
                                        if '=' in cmd[1]:
                                            new_cmd = f"os.environ['{cmd[1].split('=')[0]}'] = '{cmd[1].split('=')[1]}' #<cc-cm>\n"
                                            new_cmd_spaces = f"{spaces}os.environ['{cmd[1].split('=')[0]}'] = '{cmd[1].split('=')[1]}' #<cc-cm>\n"
                                            if not os_added:
                                                os_added = True
                                                new_imports_cell+="import os\n"
                                        else:
                                            new_cmd = f"os.environ['{cmd[1]}'] #<cc-cm>\n"
                                            new_cmd_spaces = f"{spaces}os.environ['{cmd[1]}'] #<cc-cm>\n"
                                            if not os_added:
                                                os_added = True
                                                new_imports_cell+="import os\n"
                                    else:
                                        new_cmd = f"os.environ['{cmd[1]}'] = '{cmd[2]}' #<cc-cm>\n"
                                        new_cmd_spaces = f"{spaces}os.environ['{cmd[1]}'] = '{cmd[2]}' #<cc-cm>\n"
                                        if not os_added:
                                            os_added = True
                                            new_imports_cell+="import os\n"
                                else:
                                    new_cmd = f"for k, v in os.environ.items():\n #<cc-cm>"+"        print(f'{k}={v}') #<cc-cm>\n"
                                    new_cmd_spaces = f"{spaces}for k, v in os.environ.items(): #<cc-cm>\n{spaces}"+"    print(f'{k}={v}') #<cc-cm>\n"
                                    if not os_added:
                                        os_added = True
                                        new_imports_cell+="import os\n"

                            if not args['n_o']:
                                print(f'  converted:\n    {strip_line}  to:\n    {new_cmd}')
                        else:
                            if not args['n_c']:
                                if not args['n_o']:
                                    print(f'unsupported command is detected!')
                                    print(f'  commenting out unsupported command:\n    #<cc-ac> {strip_line}')
                                new_cmd_spaces = f"{spaces}#<cc-ac> {strip_line}"
                            else:
                                if not args['n_o']:
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

def py2nb(py_str, args):
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
                if args['c_m']:
                    for line in chunk:
                        spaces_in_line = len(line) - len(line.lstrip(' '))
                        spaces = ""
                        for i in range(spaces_in_line):
                            spaces+=" "
                        strip_line = line.lstrip(' ')

                        # if magic command includes a '!' [bang] use subprocess to call the command
                        if strip_line.startswith('!'):
                            cmd = strip_line[:-1].replace("!","",1).split(" ")
                            new_cmd = f"    sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8') #<cc-cm>\n    print(sub_p_res) #<cc-cm>\n"
                            new_cmd_spaces = f"{spaces}sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8') #<cc-cm>\n{spaces}print(sub_p_res) #<cc-cm>\n"
                            chunk[x] = new_cmd_spaces
                            if not sp_added:
                                new_import = True
                                sp_added = True
                                new_imports_cell+=f"import subprocess\n"
                            if not args['n_o']:
                                print(f'  converted:\n    {strip_line}  to:\n{new_cmd}')

                         # if magic command includes a '%' [percent] convert to python code
                        elif strip_line.startswith('%'):
                            cmd = strip_line[:-1].replace("%","",1).split(" ")
                            is_cmd = 0

                            # check if command is in the list of commands
                            if cmd[0] in ["cd","env",'set_env']:
                                is_cmd = 1
                            if not args['n_o']:
                                print(f'%{cmd[0]} command detected')

                            if is_cmd:
                                if cmd[0] == "cd":
                                    new_cmd = f"os.chdir('{cmd[1]}') #<cc-cm>\n"
                                    new_cmd_spaces = f"{spaces}os.chdir('{cmd[1]}') #<cc-cm>\n"
                                    if not os_added:
                                        os_added = True
                                        new_imports_cell+="import os\n"
                                
                                if cmd[0] == "env" or cmd[0] == "set_env":
                                    if len(cmd) > 1 or cmd[0] == "set_env":
                                        if len(cmd) == 2:
                                            if '=' in cmd[1]:
                                                new_cmd = f"os.environ['{cmd[1].split('=')[0]}'] = '{cmd[1].split('=')[1]}' #<cc-cm>\n"
                                                new_cmd_spaces = f"{spaces}os.environ['{cmd[1].split('=')[0]}'] = '{cmd[1].split('=')[1]}' #<cc-cm>\n"
                                                if not os_added:
                                                    os_added = True
                                                    new_imports_cell+="import os\n"
                                            else:
                                                new_cmd = f"os.environ['{cmd[1]}'] #<cc-cm>\n"
                                                new_cmd_spaces = f"{spaces}os.environ['{cmd[1]}'] #<cc-cm>\n"
                                                if not os_added:
                                                    os_added = True
                                                    new_imports_cell+="import os\n"
                                        else:
                                            new_cmd = f"os.environ['{cmd[1]}'] = '{cmd[2]}' #<cc-cm>\n"
                                            new_cmd_spaces = f"{spaces}os.environ['{cmd[1]}'] = '{cmd[2]}' #<cc-cm>\n"
                                            if not os_added:
                                                os_added = True
                                                new_imports_cell+="import os\n"
                                    else:
                                        new_cmd = f"for k, v in os.environ.items(): #<cc-cm>\n"+"        print(f'{k}={v}') #<cc-cm>\n"
                                        new_cmd_spaces = f"{spaces}for k, v in os.environ.items(): #<cc-cm>\n{spaces}"+"    print(f'{k}={v}') #<cc-cm>\n"
                                        if not os_added:
                                            os_added = True
                                            new_imports_cell+="import os\n"

                                if not args['n_o']:
                                    print(f'  converted:\n    {strip_line}  to:\n    {new_cmd}')
                            else:
                                if args['n_c']:
                                    if not args['n_o']:
                                        print(f'unsupported command is detected!')
                                        print(f'  commenting out unsupported command:\n    #<cc-ac> {strip_line}')
                                    new_cmd_spaces = f"{spaces}#<cc-ac> {strip_line}"
                                else:
                                    if not args['n_o']:
                                        print(f'unsupported command is detected!')
                                        print(f'  not commenting out unsupported command:\n    {strip_line}')
                                    new_cmd_spaces = f"{spaces}{strip_line}"

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


def convert(in_file, out_file, extra_args):
    _, in_ext = path.splitext(in_file)
    _, out_ext = path.splitext(out_file)

    if in_ext == '.ipynb' and out_ext == '.py':
        with open(in_file, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        py_str = nb2py(notebook, extra_args)
        with open(out_file, 'w', encoding='utf-8') as f:
            f.write(py_str)

    elif in_ext == '.py' and out_ext == '.ipynb':
        with open(in_file, 'r', encoding='utf-8') as f:
            py_str = f.read()
        notebook = py2nb(py_str, extra_args)
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(notebook, f, indent=2)

    else:
        raise(Exception('Extensions must be .ipynb and .py or vice versa'))


def main():
    argv = sys.argv[1:]

    if len(argv) == 0:
        print('Usage: colab-convert <input_file> <output_file> <extra_args>')
        sys.exit(1)
    if len(argv) == 1:
        argv.append('out')

    _, in_file_ext = path.splitext(argv[0])
    _, out_file_ext = path.splitext(argv[1])

    in_is_py = False
    in_is_ipynb = False
    args_list = ['--auto-comment', '-ac', '--no-comment', '-nc', '--retain-magic', '-rm', '--convert-magic', '-cm', '--outputs', '-o', '--log', '-l']
    args_desc = {
        '--help': '(-h)\n  Show this help message',
        '--retain-magic': ' (-rm)\n  Retain magic commands in the output\n    default [ON] for .py input files\n    default [OFF] for .ipynb input files\n',
        '--convert-magic': ' (-cm)\n  Convert unsupported magic commands to python code\n    default [OFF] for .py input files\n    default [ON] for .ipynb input files\n',
        '--auto-comment': ' (-ac)\n  Automatically convert unsupported magic commands to comments\n    default [OFF] for .py input files\n    default [ON] for .ipynb input files\n',
        '--no-comment': ' (-nc)\n  Do not convert unsupported magic commands to comments\n    default [ON] for .py input files\n    default [OFF] for .ipynb input files\n',
        '--outputs': ' (-o)\n  Outputs logs of conversions and commented lines.\n    default [OFF]\n',
        '--log': ' (-l)\n  Same as Outputs\n   default [OFF]',
    }
    extra_args = None if not argv[2:] else argv[2:]

    if argv[0] in ['--help', '-h', '?']:
        print(f"list of supported arguments:")
        for key, value in args_desc.items():
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
    #default args
    if in_is_ipynb:
        no_outputs = True
        convert_magic = True
        no_comment = False
    if in_is_py:
        no_outputs = True
        convert_magic = False
        no_comment = True
    if out_file_ext != '.ipynb' and out_file_ext != '.py':
        print('Output file must be .ipynb or .py')
        sys.exit(1)
    if extra_args:
        test_args = [element for element in extra_args if element not in args_list]
        if test_args:
            print(f"list of supported arguments:")
            for key, value in args_desc.items():
                print(key, value)
            sys.exit(1)
        if '--outputs' in extra_args or '--log' in extra_args or '-l' in extra_args or '-o' in extra_args:
            no_outputs = False
            print('showing outputs from converter')
        else:
            print('[NOT] showing outputs from converter')

        if '--no-comment' in extra_args or '-nc' in extra_args or '--auto-comment' in extra_args or '-ac' in extra_args:
            if '--auto-comment' in extra_args or '-ac' in extra_args:
                if '--no-comment' in extra_args or '-nc' in extra_args:
                    print('--auto-comment (-ac) takes presidence over --no-comment (-nc)\n'+'using (-ac)')
                print('[NOT] commenting out unsupported magic commands')
                no_comment = False
            else:
                no_comment = True
                print('[NOT] commenting out unsupported magic commands')
        else:
            print('commenting out unsupported magic commands')

        if '--convert-magic' in extra_args or '-cm' in extra_args or '--retain-magic' in extra_args or '-rm' in extra_args:
            if '--retain-magic' in extra_args or '-rm' in extra_args:
                if '--convert-magic' in extra_args or '-cm' in extra_args:
                    print('--retain-magic (-rm) takes presidence over --convert-magic (-cm)\n'+'using (-rm)')
                print('[NOT] converting magic commands!')
                convert_magic = False
            else:
                print('converting magic commands')
                convert_magic = True
        else:
            if in_is_ipynb:
                print('converting magic commands')
            if in_is_py:
                print('[NOT] converting magic commands!')

    else:
        if in_is_ipynb:
            print('[NOT] showing outputs from converter')
            print('converting magic commands')
            print('commenting out unsupported magic commands')
        if in_is_py:
            print('[NOT] showing outputs from converter')
            print('[NOT] converting magic commands!')
            print('[NOT] commenting out unsupported magic commands!')
    
    args = {'n_o': no_outputs, 'c_m': convert_magic, 'n_c': no_comment}

    convert(in_file=argv[0], out_file=argv[1], extra_args=args)


if __name__ == '__main__':
    main()
