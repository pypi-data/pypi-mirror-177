from fileren.functions import parse_args
from fileren.files_renamer import FilesRenamer


def main():
    path, regex, new_string = parse_args()
    files_renamer = FilesRenamer(path, regex, new_string)
    files_renamer.start()


if __name__ == "__main__":
    main()
