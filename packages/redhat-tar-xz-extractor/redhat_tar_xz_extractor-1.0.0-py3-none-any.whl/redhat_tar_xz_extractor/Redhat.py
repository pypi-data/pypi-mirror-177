import os
import shutil
import tarfile


class Redhat:
    def __init__(self,fileuri, extract_folder):
        self.fileuri = fileuri
        self.extract_folder = extract_folder

    def extractor(self):

        match = self.fileuri.split('/')[-1].split('.')[0] + '/sos_commands/hardware/dmidecode'
        search_word = "Asset Tag"
        asset_tag = ""

        with open(self.fileuri, 'rb') as tgzFile:
            with tarfile.open(mode="r|xz", fileobj=tgzFile) as tgz:
                for entry in tgz:
                    if entry.name == match:
                        extract_file_path = os.path.join(self.extract_folder, os.path.normpath(entry.name))
                        os.makedirs(os.path.dirname(extract_file_path), exist_ok=True)
                        with open(extract_file_path, 'wb') as entry_out:
                            shutil.copyfileobj(tgz.extractfile(entry), entry_out)
                        file = open(extract_file_path, 'rb')
                        Lines = file.readlines()
                        for line in Lines:
                            if search_word in line.decode():
                                asset_tag = line.decode().split(':')[-1]
                                break

        return asset_tag
