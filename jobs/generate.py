import argparse
import pathlib
import actusmp

# CLI argument parser.
_ARGS = argparse.ArgumentParser("Writes code generated from ACTUS dictionary to file system.")

# Set CLI argument: target programming language.
_ARGS.add_argument(
    "--lang",
    choices=[i for i in actusmp.TargetLanguage],
    dest="lang",
    help="Target programming language status.",
    type=lambda x: actusmp.TargetLanguage[x]
    )

# Set CLI argument: output directory.
_ARGS.add_argument(
    "--dest",
    dest="dest",
    help="Target file system directory into which code will be written.",
    type=pathlib.Path
    )

# Set CLI argument: path to JAVA reference implementation repo (actus-core).
_ARGS.add_argument(
    "--core",
    dest="path_to_core",
    help="path to JAVA reference implementation repo (actus-core).",
    type=pathlib.Path
    )


def _main(args: argparse.Namespace):
    """Main entry point.

    :param args: Parsed command line arguments.

    """
    actusmp.write(args.lang, args.dest, args.path_to_core)


# Entry point.
if __name__ == "__main__":
    _main(_ARGS.parse_args())
