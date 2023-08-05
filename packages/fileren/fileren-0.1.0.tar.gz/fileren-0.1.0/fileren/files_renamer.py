import os
import re

from rich.console import Console
from rich.text import Text

from rich.prompt import Prompt


class FilesRenamer:
    console = Console()

    def __init__(self, path, pattern: str = None, new_string: str = None):
        self.path = path
        self.files = os.listdir(path)
        self.pattern = pattern
        self.new_string = new_string

    def start(self):
        """
        It renames the files
        """
        if self.pattern is None:
            self.pattern = Prompt.ask("Pattern to search", console=self.console)

        matches = [list(set(re.findall(self.pattern, file))) for file in self.files]
        self.display_changes(matches, None, "red")

        if self.new_string is None:
            self.new_string = Prompt.ask("New text", console=self.console)

        self.display_changes(matches, self.new_string, "green")

        # Search for the pattern in the files
        rename_list = self.rename_files(matches)

        # Ask for confirmation
        if Prompt.ask("Do you want to rename the files?", choices=["y", "n"]) == "y":
            for ren in rename_list:
                os.rename(
                    os.path.join(self.path, ren[0]),
                    os.path.join(self.path, ren[1]),
                )
            self.console.print("Files renamed", style="bold green")
        else:
            self.console.print("Files not renamed", style="bold red")

    def rename_files(self, matches: list) -> list:
        """
        It replaces the string in the text

        :param matches: list of matches
        :return: text with the string replaced
        """

        new_filenames = []
        for i, match in enumerate(matches):
            text_to_replace = self.files[i]
            for substring in match:
                text_to_replace = text_to_replace.replace(substring, self.new_string)

            new_filenames.append([self.files[i], text_to_replace])
        return new_filenames

    def display_changes(self, matches: list, new_string: str = None, color="red"):
        """
        It displays the changes in the files

        :param matches: list of matches
        :param new_string: new string to replace
        :param color: color of the text
        """
        display_text = Text()
        temp_substrings = []
        # If the pattern is found, replace it with the new string
        for i, match in enumerate(matches):
            if match:
                split_text = self.files[i]
                for substring in match:
                    new_substring = new_string
                    if new_substring is None:
                        new_substring = substring

                    temp_substrings.append(new_substring)

                    # Replace the substring with the new string
                    split_text = split_text.replace(
                        substring,
                        f";;{new_substring};;",
                    )
                split_text = split_text.split(";;")
                for text in split_text:
                    if text in temp_substrings:
                        display_text.append(text, style=f"bold {color}")
                    else:
                        display_text.append(text)

                display_text.append("\n")

        self.console.print(display_text)
