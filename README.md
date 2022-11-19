# Plex File Organizer

This is a script I wrote mainly for educational purposes (teach myself about regexes essentially) but also for personal use to automate the task of renaming loads of downloaded files of TV shows to fit the Plex File Template. Instead of doing all that by hand, this script will figure out the showtitle, season, and episode of each file and organize them accordingly in a neat template, with options to also delete unneccessary files and folders afterwords.

## Installation

Currently I'm only keeping this script as a local zip file that you can easily run and install from the command line. The only reason I'm even setting it up as a python module is to make it so it can be run as a command from anywhere in the command line.

1. Download the [latest release](https://github.com/MilkyIQ/plex-file-organizer/releases "Releases")
2. Navigate to where you downloaded the file `cd (YOUR-PATH-HERE)`
3. Install via pip locally `pip3 install plex-file-organizer-(VERSION).zip`

## Usage

After installing, you should be able to use the `rename` command to rename and/or move a directory of files and folders. The command takes two arguments: *targetDir*, and *outputDir*. *targetDir* is the directory where you have your downloaded shows in (e.g. ~/Downloads); *outputDir* is the directory you want the files to end up in (e.g. ~/Videos).

Command syntax:

```bash
~$ rename {targetDir} {outputDir}
```

Example:

```bash
~$ rename /home/user/Downloads/ /home/user/Videos/
```

If you'd like to try the script out for yourself, you can use [this sample](https://github.com/MilkyIQ/plex-file-organizer/files/9391462/TV.zip) that has a bunch of stinky filenames. (The files are all 0 bytes large as they are just testing files so they dont need to have any actual data.)

## Limitations

Currently the script is very, very basic and simple (I'm not the most advanced on this stuff), so there are a few limitations:

- No support for filepath shortcuts like `$HOME` or `~`. (This is honestly just laziness on my end because I hate string manipulation)
- No support for grabbing files off remote computers (i.e., `user@192.168.2.92:/home/user/Downloads` does not work)
- No support for tab-completing filenames
- The name of the show MUST be labeled in the parent directory of all the files, otherwise it won't work. This is because I am small brain and I don't know any other way of making this script work

## TODO

- [ ] Add flags for manual specification of title/season data
- [ ] Cleanup redundant code
- [ ] Group functions into their own modules (Better for organization maybe?)
