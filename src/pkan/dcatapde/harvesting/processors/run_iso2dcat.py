import argparse

from dynaconf import Dynaconf
from iso2dcat.main import Main


def run_iso():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    parser.add_argument('--target')
    args = parser.parse_args()
    config = None
    target = None
    if args.file:
        config = Dynaconf(
            envvar_prefix='DYNACONF',  # replaced "DYNACONF" by 'DYNACONF'
            settings_files=[args.file],
            environments=True,
            env='Default',
        )
    if args.target:
        target = args.target
    Main().run(cfg=config, stat_file=target)


if __name__ == '__main__':
    run_iso()
