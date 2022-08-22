"""
The command-line interface for the downloader
"""
import argparse
from .renamer import *


def main():
    parser = argparse.ArgumentParser(
        description="Plex File Organizer"
    )
    parser.add_argument(
        "targetDir", type=str,
        help="The directory to target files"
    )
    parser.add_argument(
        "destPath", type=str,
        help="The desired output path for new files"
    )
    args = parser.parse_args()
    rename(args.targetDir, args.destPath)
    print("Renaming successful!")

if __name__ == "__main__":
    main()