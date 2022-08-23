import os, re
from colorama import Fore

print(Fore.RESET + '\n')

# STRING MANIPULATION
# ------------------------------------------------------------ #

# Preformat strings to be compliant with data extraction functions
def prep_txt(txt, split=True, removeStr=''):
  t = re.sub("[*]|- ", "", txt)
  t = re.sub("\s+", " ", t)
  t = re.sub(" ", ".", t)
  t = re.sub(removeStr, "", t)
  t = re.sub("^[.]", "", t)
  if split == True: t = t.split(".")
    
  txt = t
  return txt

# Returns an abbreviated version of a string if there are more words than the specified limit; does not change case
def abbreviate_media_titles(title, limit):
  if limit != 0 and len(title.split('.')) > limit:
    abbreviatedTitle = ''
    for x in title.split('.'):
        abbreviatedTitle += x[0]
  else:
    abbreviatedTitle = title

  return abbreviatedTitle

# String formatting ~magic~ to make new pathfiles
def create_new_filename(dest, title, season, episode, part, suffix):
  # Clean up icky user data (i.e., removes trailing slash + prep mediaTitle)
  dest = [i for i in dest.split('/') if i != '']
  dest = '/' + '/'.join(dest)
  aTitle = abbreviate_media_titles(title, 6)

  # Add all values + part and suffix
  newFilename = f'{dest}/{title}/Season.{season}/{aTitle}.s{str(season).zfill(2)}e{str(episode).zfill(2)}'
  if part != None: newFilename = newFilename + '.' + part.lower()
  newFilename = newFilename + '.' + suffix

  return newFilename

# ------------------------------------------------------------ #



# DATA EXTRACTION
# ------------------------------------------------------------ #

# Find where in the string (fname list) the requested data is via a specified regex and return
def search_data_pos(fname, regex):
  i=0

  for word in fname:
    x = re.search(regex, word)
    if x != None:
        return i, x

    else:
      i+=1
      continue

# Find and return the name of a show from filepath
def extract_data_title(filepath, targetDir):
  topDir = ''
  targetDir = [i for i in targetDir.split('/') if i != ''][-1]
  listPath = prep_txt(filepath, split=False, removeStr='').split('/')
  listPath.reverse()

  # Iterate through the path and find the top folder for the show (just under /TV/ or /Movies/ for padme)
  i=0
  for folder in listPath:
    if folder != targetDir:
      i+=1
      continue
    else:
      topDir = listPath[i-1].split('.')
      break

  # Find where the season info is
  try:
    pos = search_data_pos(fname=topDir, regex="^S[0-9]|^s[0-9]|Season|season")[0]
  except TypeError:     # if pos == None:
    data = topDir[0:]
  else:                 # if pos != None:
    data = topDir[0:pos]
  
  # Convert data (mediaTitle) into a clean string
  s = ''
  for word in data: s = s + word + '.'
  data = s.strip()
  data = data[0:-1] # remove additional period

  if data == '':
    raise RuntimeError(Fore.RED + f"Could not find a valid show title for this file. The parent directory of this file might be missing a title.\nFile: {filepath}" + Fore.RESET)

  return data

# Strip strings that contain season data and return just the season number
def extract_data_season(filepath, title):
  parentDir = prep_txt(filepath.split('/')[-2], removeStr=title)
  pos, obj = search_data_pos(fname=parentDir, regex="^S[0-9]|^s[0-9]|Season|season")

  # Reformats "Season X" cases to avoid processing garbage
  if obj.string == 'Season':
    parentDir[pos] = f'S{parentDir[pos+1]}'
    parentDir.pop(pos+1)
  
  data = re.sub("[a-zA-Z]", "", parentDir[pos])

  try: 
    data = int(data)
  except ValueError:
    raise ValueError(Fore.RED + "Could not find a valid season number. There may be invalid characters or multiple seasons contained in a single folder." + Fore.RESET + f"\nFile: {filepath}")
  return data

# Evaluate filenames for the episode number and return just the number
def extract_data_episode(filepath, title, season):
  file = prep_txt(filepath.split('/')[-1], removeStr=title)
  pos, obj = search_data_pos(fname=file, regex="E.?[0-9]$|e.?[0-9]$|^[0-9].+[0-9]$")
  if len(re.findall('E.?[0-9]$|e.+[0-9]$|^[0-9].+[0-9]$', obj.string)) > 1:
    raise RuntimeError(Fore.RED + "There are multiple episodes in a single file, that's stupid and I'm not fixing it." + Fore.RESET + f"\nFile: {filepath}")

  data = re.sub("[a-zA-Z]|-|_", "", obj.string)
  r = re.search(f'{season}', data)

  # Rogue files / folders that span multiple seasons fuck up the data extraction method as it is quite limited (and dumb)
  try:
    ep = int(data[r.span()[1]:])
  except (AttributeError, ValueError) as e: # Thank you mechanical_meat!
    raise ValueError(Fore.RED + "Could not validate season number. Multiple seasons may be placed within a single folder or no season is specified." + Fore.RESET + f"\nFile: {filepath}")
  
  #Check for split episodes
  try:
    obj = search_data_pos(fname=file, regex="cd[0-9]|disc[0-9]|disk[0-9]|dvd[0-9]|part[0-9]|pt[0-9]")[1]
    if obj != None:
      pt = obj.string
  except TypeError:
    pt = None
  finally: 
    return ep, pt
  
# ------------------------------------------------------------ #



# FILE MANIPULATION
# ------------------------------------------------------------ #

# Get files from specified path (soon to be deprecated)
def get_files(dir, wantedFiles):
  res = []

  # Recursively add all filepaths (inlcuding those in subdirectories) into a list (not including badfiles)
  for dirname, dirnames, filenames in os.walk(dir):
    for filename in filenames:
      if any(ext in filename for ext in wantedFiles) == True: 
        res.append(os.path.join(dirname, filename))
      else:
        continue
  
  res.sort()
  return res

# Move a file from its given path to its desired output (creating new folders as needed)
def move_file(originPath, destPath):
  destDir = [i for i in destPath.split('/') if i != ''][0:-1]
  destDir = '/' + '/'.join(destDir)

  try:
    os.rename(originPath, destPath)
  except FileNotFoundError:
    os.makedirs(destDir)
    os.rename(originPath, destPath)

# Delete all empty folders and files that are not important to the user
def delete_garbage(dir, wantedFiles):
  badFiles, badFolders = [], []
  
  # Recursively remove all files not ending with suffix in wantedFiles
  for dirpath, _, filenames in os.walk(dir):
    for filename in filenames:
      if any(ext in filename for ext in wantedFiles) == False: 
        badFiles.append(os.path.join(dirpath, filename))
      else:
        continue

  # Greenlight to remove badFiles
  if len(badFiles) > 0:
    size = 0
    for path in sorted(badFiles):
      size += os.path.getsize(path)
      print(path)
    if size >= 1000000: size = str(size / 1000000) + 'MB'
    else: size = str(size) + 'B'
    
    greenLight = input(Fore.YELLOW + f'\n{len(badFiles)} unneeded files ({size}) were found. Would you like to delete them? ' + Fore.RESET + '[Y/n]' + Fore.RESET)
    if greenLight.lower() == 'y':
      for path in badFiles: os.remove(path)
      print('Deleting files...\n')
    else: print('Abort.\n')

  # Recursively find all empty folders and add them into a list (this took me so fucking long to figure out please use it)
  for path, subdirs, files in sorted(list(os.walk(dir))[1:],reverse=True):
    if subdirs == [] and files == []: # if NO subdirs and NO files
      badFolders.append(path)
    if subdirs != [] and files == []: # if YES subdirs but NO files
      for i in subdirs:
        if os.listdir(path + '/' + i) != []:
          break
        else:
          badFolders.append(path)
          break

  
  # Greenlight to remove badFolders
  if len(badFolders) > 0:
    for path in sorted(badFolders): print(path)
    greenLight = input(Fore.YELLOW + f'\n{len(badFolders)} empty folder(s) were found. Would you like to delete them? ' + Fore.RESET + '[Y/n]' + Fore.RESET)
    if greenLight.lower() == 'y':
      for path in badFolders: os.rmdir(path)
      print('Deleting files...\n')
    else: print('Abort.\n')


# ------------------------------------------------------------ #



# MAIN FUNCTIONS
# ------------------------------------------------------------ #

# Ask user to confirm if the changes look OK before merging
# ik this function is pretty useless seeing as it's only a one-time use, but I got really sick of having to comment all this out
# plus it makes it easier to test just the results
def prompt_user(changes, shows, targetDir, wantedFiles):
  # Check for existing files
  badFiles = []
  for old, new in changes:
    if os.path.exists(new):
      badFiles.append(new)

  # Print all changes
  i=0
  for old, new in changes:
    print(Fore.LIGHTBLACK_EX + old, Fore.RED + f'\n ({i}) -> ', Fore.GREEN + new + Fore.RESET)
    i+=1
  print('')

  # Print all shows
  i=0
  for title, count in shows.items():
    print(f'{i+1}. {title.translate({46: 32})} - ({count[0]} folders) - ({count[1]} files)')
    i+=1
  
  # Ask for confirmation
  if badFiles: print(Fore.RED + '\nWARNING: Some existing files will be overwritten in the process' + Fore.RESET, end='')
  greenLight = input(Fore.YELLOW + f'\n{len(changes)} files will be moved. Do these names look okay? ' + Fore.RESET + '[Y/n]' + Fore.RESET)

  # Act on confirmation
  if greenLight.lower() == 'y':
    print('')
    for old, new in changes: move_file(old, new)
    delete_garbage(targetDir, wantedFiles)
  else:
    print('Abort.\n')
    return

# main()
def rename(targetDir, destPath):
  wantedFiles = ['.mp4', '.mkv', '.avi', '.flv', '.mov', '.m4v']
  res, shows = [], {}

  # Primary script loop
  for path in get_files(targetDir, wantedFiles):
    mediaTitle = extract_data_title(path, targetDir)
    mediaSeason = extract_data_season(path, mediaTitle)
    mediaEpisode, filePart = extract_data_episode(path, mediaTitle, mediaSeason)
    fileType = path[path.rfind('.')+1:]
    newPath = create_new_filename(destPath, mediaTitle, mediaSeason, mediaEpisode, filePart, fileType)

    res.append((path, newPath))
    if mediaTitle not in shows.keys():
      shows[mediaTitle] = [[], 1]
    elif mediaTitle in shows.keys() and mediaSeason not in shows[mediaTitle][0]:
      shows[mediaTitle][0].append(mediaSeason)
      shows[mediaTitle][1] += 1
    else:
      shows[mediaTitle][1] += 1
  for name in shows: shows[name] = (len(shows[name][0]), shows[name][1])

  # Prompt user and act on it
  if len(res) > 0:
    prompt_user(res, shows, targetDir, wantedFiles)
  else:
    raise FileNotFoundError(Fore.RED + "Could not find files to rename. Directory may be empty or contain no files that fit the plex media format" + Fore.RESET)

# ------------------------------------------------------------ #

rename('/home/thiago/samba', '/home/thiago/samba')