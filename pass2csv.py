import csv
import os
import sys
import gnupg

## Usage
# Run pass2csv /path/to/password-storage

## options
# field names
userfield = "user"
urlfield = "url"

def traverse(path):
    for root, dirs, files in os.walk(path):
        if '.git' in dirs:
            dirs.remove('.git')
        for name in files:
            yield os.path.join(root, name)


def parse(basepath, path, data):
    name = os.path.splitext(os.path.basename(path))[0]
    group = os.path.dirname(os.path.os.path.relpath(path, basepath))
    split_data = data.split('\n')
    password = split_data[0]
    matching_user = [s for s in split_data if userfield+": " in s]
    user = None
    url = None
    if matching_user:
        for x in matching_user:
            user_split = x.split(userfield+": ")
            if len(user_split) == 2:
                user = user_split[1]
            else:
                user = None
    matching_url = [s for s in split_data if urlfield+": " in s]
    if matching_url:
        for x in matching_url:
            url_split = x.split(urlfield+": ")
            if len(url_split) == 2:
                url = url_split[1]
            else:
                url = None
    if url == "None":
        if user == "None":
            return [group, name, password]
        else:
            return [group, name, password, user]
    else:
        if user == "None":
            return [group, name, password, url]
        else:
            return [group, name, password, url, user]
        


def main(path):
    gpg = gnupg.GPG()
    gpg.encoding = 'utf-8'
    csv_data = []
    for file_path in traverse(path):
        if os.path.splitext(file_path)[1] == '.gpg':
            with open(file_path, 'rb') as f:
                data = str(gpg.decrypt_file(f))
                csv_data.append(parse(path, file_path, data))

    with open('pass.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        writer.writerows(csv_data)


if __name__ == '__main__':
    path = os.path.abspath(sys.argv[1])
    main(path)
