import json
import sys
from os import path

header_comment = '# %%\n'

def nb2py(notebook, args):
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
            if args['c_m']:
                for line in source:
                    spaces_in_line = len(line) - len(line.lstrip(' '))
                    spaces = ""
                    for i in range(spaces_in_line):
                        spaces+=" "
                    strip_line = line.lstrip(' ')
                    if strip_line.startswith('!'):
                        cmd = strip_line[:-1].replace("!","",1).split(" ")
                        new_cmd = f"    sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8')\n    print(sub_p_res)\n"
                        new_cmd_spaces = f"{spaces}sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8')\n{spaces}print(sub_p_res)\n"
                        source[x] = new_cmd_spaces
                        if not args['s_o']:
                            print(f'  converted:\n    {strip_line}  to:\n  {new_cmd}')
                    elif strip_line.startswith('%'):
                        cmd = strip_line[:-1].replace("%","",1).split(" ")
                        is_cmd = 0
                        if cmd[0] == "cd":
                            is_cmd = 1
                            if not args['s_o']:
                                print(f'%{cmd[0]} command detected')
                        if is_cmd:
                            if cmd[0] == "cd":
                                new_cmd = f"os.chdir('{cmd[1]}')\n"
                                new_cmd_spaces = f"{spaces}os.chdir('{cmd[1]}')\n"
                            source[x] = new_cmd_spaces
                            if not args['s_o']:
                                print(f'  converted:\n   {strip_line}  to:\n    {new_cmd}')
                        else:
                            if not args['s_o']:
                                print(f'{cmd[0]} magic command is not supported yet!!!')
                    x+=1
            result.append("%s%s" % (header_comment+reformat_metadata, ''.join(source)))

    return '\n\n'.join(result)+f'\n\n{header_comment}{reformat_main_metadata}'


def py2nb(py_str, args):
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
                if args['c_m']:
                    for line in chunk:
                        spaces_in_line = len(line) - len(line.lstrip(' '))
                        spaces = ""
                        for i in range(spaces_in_line):
                            spaces+=" "
                        strip_line = line.lstrip(' ')
                        if strip_line.startswith('!'):
                            cmd = strip_line[:-1].replace("!","",1).split(" ")
                            print(f'!{cmd[0]} command detected')
                            new_cmd = f"    sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8')\n    print(sub_p_res)\n"
                            new_cmd_spaces = f"{spaces}sub_p_res = subprocess.run({cmd}, stdout=subprocess.PIPE).stdout.decode('utf-8')\n{spaces}print(sub_p_res)\n"
                            chunk[x] = new_cmd_spaces
                            if not args['s_o']:
                                print(f'  converted:\n    {strip_line}  to:\n{new_cmd}')
                        elif strip_line.startswith('%'):
                            cmd = strip_line[:-1].replace("%","",1).split(" ")
                            is_cmd = 0
                            if cmd[0] == "cd":
                                is_cmd = 1
                                if not args['s_o']:
                                    print(f'%{cmd[0]} command detected')
                            if is_cmd:
                                if cmd[0] == "cd":
                                    new_cmd = f"os.chdir('{cmd[1]}')\n"
                                    new_cmd_spaces = f"{spaces}os.chdir('{cmd[1]}')\n"
                                chunk[x] = new_cmd_spaces
                                if not args['s_o']:
                                    print(f'  converted:\n   {strip_line}  to:\n    {new_cmd}')
                            else:
                                if not args['s_o']:
                                    print(f'{cmd[0]} magic command is not supported yet!!!')
                        x+=1
                cell['source'] = chunk
            cells.append(cell)

    notebook = {
        'cells': cells,
        'metadata': main_metadata,
          'nbformat': 4,
          'nbformat_minor': 4
    }

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
    extra_args = None if not argv[2:] else argv[2:]
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
        supress_outputs = False
        convert_magic = True
    if in_is_py:
        supress_outputs = False
        convert_magic = False
    if out_file_ext != '.ipynb' and out_file_ext != '.py':
        print('Output file must be .ipynb or .py')
        sys.exit(1)
    if extra_args:
        if '--no-outputs' in extra_args or '-q' in extra_args:
            supress_outputs = True
        if '--convert-magic' in extra_args or '-c' in extra_args:
            convert_magic = True
            print('converting magic commands')
        elif '--retain-magic' in extra_args or '-r' in extra_args:
            convert_magic = False
            if '--convert-magic' in extra_args or '-c' in extra_args:
                print('--retain-magic takes presidence over --convert-magic')
                print('using (-r)\nNOT converting magic commands!')
            else: 
                print('NOT converting magic commands!')
        else:
            if in_is_ipynb:
                print('converting magic commands')
            if in_is_py:
                print('NOT converting magic commands!')
    else:
        if in_is_ipynb:
            print('converting magic commands')
        if in_is_py:
            print('NOT converting magic commands!')
    
    args = {'s_o': supress_outputs, 'c_m': convert_magic}

    convert(in_file=argv[0], out_file=argv[1], extra_args=args)


if __name__ == '__main__':
    main()
