import argparse
import runpy
import sys
import webbrowser
from urllib.parse import urlencode

parser = argparse.ArgumentParser(description='Utilitário para encontrar soluções para problemas no Python')
parser.add_argument('-m', '--module', dest='module', action='store_true', help='busca módulo em vez de um script')
parser.add_argument('path', help='caminho para o script Python')
parser.add_argument('args', nargs='*', help='argumentos passados para o script')


def main():
    args = parser.parse_args()

    try:
        sys.argv = ['', *args.args]
        if args.module:
            runpy.run_module(args.path, alter_sys=True)
        else:
            runpy.run_path(args.path)
    except Exception as e:
        error_msg = f'{e.__class__.__name__}: {e}'
        url = f'https://duckduckgo.com/?{urlencode({"q": error_msg})}'
        webbrowser.open(url)


if __name__ == '__main__':
    main()
