import argparse

from dynaconf import Dynaconf
from iso2dcat.main import Main


def run_iso():
    parser = argparse.ArgumentParser()
    parser.add_argument('--file')
    args = parser.parse_args()
    config = None
    if args.file:
        config = Dynaconf(
            envvar_prefix='DYNACONF',  # replaced "DYNACONF" by 'DYNACONF'
            settings_files=[args.file],
            environments=True,
            env='Default',
        )
    Main().run(cfg=config)


if __name__ == '__main__':
    run_iso()
