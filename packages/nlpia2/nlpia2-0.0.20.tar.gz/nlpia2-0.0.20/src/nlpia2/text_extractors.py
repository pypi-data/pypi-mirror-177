import argparse
import doctest
from doctest import DocTestParser
from parsimonious import Grammar
from pathlib import Path
import re
import tempfile

try:
    DATA_DIR = Path(__file__).parent / 'data'
except NameError:
    DATA_DIR = Path.cwd()

assert DATA_DIR.is_dir()

MANUSCRIPT_DIR = Path.home() / 'code/tangibleai/nlpia-manuscript/manuscript/adoc'
DEFAULT_FILENAME = 'Chapter 03 -- Math with Words (TF-IDF Vectors).adoc'
DEFAULT_FILEPATH = MANUSCRIPT_DIR / DEFAULT_FILENAME
DEFAULT_OPTIONFLAGS = doctest.ELLIPSIS | doctest.NORMALIZE_WHITESPACE


def extract_blocks(filepath=Path('data/tests/test.adoc'), grammarpath=Path('data/grammars/adoc.ppeg')):
    filepath, grammarpath = Path(filepath), Path(grammarpath)
    g = Grammar(grammarpath.open().read())
    ast = g.parse(filepath.open().read())
    return ast


def extract_code_lines(filepath=DEFAULT_FILEPATH, with_metadata=True):
    expressions = extract_expressions(filepath=filepath)
    if with_metadata:
        return [vars(ex) for ex in expressions]
    return [ex.source for ex in expressions]


def extract_expressions(filepath=DEFAULT_FILEPATH):
    text = Path(filepath).open('rt').read()
    dtparser = DocTestParser()
    return dtparser.get_examples(text)


def expressions_to_doctests(expressions, prompt='>>> ', ellipsis='... ', comment=''):
    # expressions = extract_expressions(filepath=filepath)

    prompt = prompt or ''
    if prompt and prompt[-1] != ' ':
        prompt += ' '
    if not isinstance(prompt, str):
        prompt = '>>> '

    ellipsis = ellipsis or ''
    if ellipsis and ellipsis[-1] != ' ':
        ellipsis += ' '
    if not isinstance(ellipsis, str):
        ellipsis = '... '

    comment = comment or ''
    if not isinstance(comment, str):
        comment = '# '
    if comment and comment[-1] != ' ':
        comment += ' '
    blocks = ['']

    for exp in expressions:
        lines = exp.source.splitlines()
        if exp.source.strip() and len(lines) == 1:
            blocks[-1] += prompt + exp.source
        else:
            blocks[-1] += prompt + lines[0] + '\n'
            for line in lines[1:]:
                blocks[-1] += ellipsis + lines[0] + '\n'

        if exp.want:
            blocks[-1] += comment + exp.want
            blocks.append('')


def extract_code_file(filepath=DEFAULT_FILEPATH, destfile=None):
    filepath = Path(filepath)
    destfile = Path(destfile) if destfile else filepath.with_suffix('.adoc.py')
    if destfile.is_dir():
        destfile = destfile / filepath.with_suffix('.adoc.py').name
    lines = extract_code_lines(filepath=filepath, with_metadata=False)
    if destfile:
        with Path(destfile).open('wt') as fout:
            fout.writelines(lines)
    return ''.join(lines)


def test_file(filepath=DEFAULT_FILEPATH, adoc=True,
              optionflags=DEFAULT_OPTIONFLAGS,
              name=None,
              verbose=False,
              package=None, module_relative=False,
              **kwargs):
    if name is None:
        name = filepath.name
    if package:
        module_relative = True
        basedir = '.'
    basedir = Path(basedir)
    if not module_relative:
        assert filepath.is_file()
    if adoc:
        with filepath.open() as fin:
            lines = fin.readlines()
            newlines = []
            for pair in zip(lines[:-1], lines[1:]):
                newlines.append(pair[0])
                if not re.match(r'\s*\[\s*source\s*,\s*python\s*\]\s*', pair[0]):
                    if re.match(r'\s*[-]{4,80}\s*', pair[1]):
                        newlines.append('\n')
            newlines.append(lines[-1])
        fp, filepath = tempfile.mkstemp(text=True)
        filepath = Path(filepath)
        with filepath.open('wt') as fout:
            fout.writelines(newlines)
    results = doctest.testfile(str(filepath),
                               name=name,
                               module_relative=module_relative, package=package,
                               optionflags=optionflags, verbose=verbose,
                               **kwargs)
    filepath.unlink()
    return results


def extract_code_files(adocdir=MANUSCRIPT_DIR, destdir=None, glob='*.adoc'):
    adocdir = Path(adocdir)
    if destdir is None:
        destdir = adocdir.parent / 'py'
    destdir = Path(destdir)
    destdir.mkdir(exist_ok=True)
    destpaths = []
    for p in adocdir.glob(glob):
        destfile = (destdir / p.name).with_suffix('.adoc.py')
        print(f"{p} => {destfile}")
        code = extract_code_file(filepath=p)
        with destfile.open('wt') as fout:
            fout.write(code)
        destpaths.append(destfile)
    return destpaths


def parse_args(
        description='Transcoder for doctest-formatted code blocks in asciidoc/txt files to py, or ipynb code blocks',
        input_help='Path to asciidoc or text file containing doctest-format code blocks',
        output_help='Path to new py file created from code blocks in INPUT',
        format_help='Output file format or type (md, py, ipynb, python, or notebook)'):

    parser = argparse.ArgumentParser(description=description)

    parser.add_argument(
        '--input', type=Path, default=None,
        help=input_help
    )
    parser.add_argument(
        '--output', type=Path, default=None,
        help=output_help,
    )
    parser.add_argument(
        '--format', type=str, default='py', help=format_help
    )
    return vars(parser.parse_args())


if __name__ == '__main__':
    args = parse_args()
    if args['input']:
        if Path(args['input']).is_dir():
            results = extract_code_files(adocdir=args['input'])
        else:
            results = extract_code_file(filepath=args['input'])
    else:
        if input('Extract python from all manuscript/adoc files? ').lower()[0] == 'y':
            results = extract_code_files()
