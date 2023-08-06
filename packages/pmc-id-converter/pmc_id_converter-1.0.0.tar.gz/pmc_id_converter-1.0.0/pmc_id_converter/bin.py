import sys
import json
import click

from simple_loggers import SimpleLogger
from pmc_id_converter import API, version_info


CONTEXT_SETTINGS = dict(help_option_names=['-?', '-h', '--help'])

contact = click.style('Contact: {author} <{author_email}>', italic=True, fg='bright_white')
__epilog__ = click.style(f'''

\b
Examples:
    pmc_idconv --help
    pmc_idconv 30003000                     [PMID]
    pmc_idconv PMC6039336                   [PMCID]
    pmc_idconv 10.1007/s13205-018-1330-z    [DOI]
    pmc_idconv 30003000 30003001 30003002   [BATCH]
    pmc_idconv 30003000 30003001 -o out.jl  [FILE]  

{contact}
'''.format(**version_info), fg='green')

@click.command(
    name=version_info['prog'],
    help=click.style(version_info['desc'], italic=True, fg='cyan', bold=True),
    no_args_is_help=True,
    context_settings=CONTEXT_SETTINGS,
    epilog=__epilog__,
)
@click.argument('ids', nargs=-1)
@click.version_option(version=version_info['version'], prog_name=version_info['prog'])
@click.option('-o', '--outfile', help='the output filename [stdout]')
def cli(**kwargs):
    logger = SimpleLogger('Main')
    ids = kwargs['ids']
    outfile = kwargs['outfile']
    out = open(outfile, 'w') if outfile else sys.stdout
    with out:
        for record in API.idconv(*ids):
            out.write(json.dumps(record.data, ensure_ascii=False) + '\n')
    if outfile:
        logger.debug(f'save file to: {outfile}')


def main():
    cli()


if __name__ == '__main__':
    main()
