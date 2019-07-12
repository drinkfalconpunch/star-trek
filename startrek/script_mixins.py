from abc import ABCMeta, abstractmethod
from collections import deque
import re
from pathlib import Path
from startrek.exceptions import ScriptException

OMITTED = 'OMITTED'

class ScriptBase(metaclass=ABCMeta):
    def __init__(self, script_text=None, script_path=None, series_name=None,
                 season_number=0, episode_number=0):
        if script_text:
            self.script = script_text
        elif script_path:
            self.script = self._get_script_path_contents(script_path)
        else:
            raise ScriptException('No valid script.')
        self.series_name = series_name
        self.season_number = season_number
        self.episode_number = episode_number
        self.dialogue = None

    @abstractmethod
    def extract_episode_dialogue(self, remove_blank_lines=False):
        pass

    @abstractmethod
    def section_headers(self):
        pass

    @abstractmethod
    def sectioned_script(self):
        pass

    @staticmethod
    def _get_script_path_contents(script_path):
        if isinstance(script_path, str):
            script_path = Path(script_path)
        if not script_path.exists():
            raise ScriptException(f'Invalid script path: {script_path}')
        return open(script_path, 'r').read()



class ScriptBlocks(ScriptBase):
    SECTION_HEADER = ''

    _regex_section_number = r'^\d+[a-zA-Z]?'
    regex_section_number = re.compile(_regex_section_number)
    # regex to get everything between two brackets if it is the only thing in the line.
    _regex_header = r'^\d+[a-zA-Z]?\s*(.+)$'
    regex_header = re.compile(_regex_header)
    # regex to match line starting with capitalized words with a colon, signifying character dialogue.
    _regex_character = r'^\s*([A-Z. ]+)\s*$'
    regex_character = re.compile(_regex_character)
    # # regex to match everything after the character name, colon, and space
    # _regex_dialogue_line = r'^[A-Z]{1,}.+:\s*(.+)'
    # regex_dialogue_line = re.compile(_regex_dialogue_line)

    def _script_to_lines(self):
        return [line for line in self.script]

    def _iterate_lines_words(self, string, remove_blank_lines=False):
        if isinstance(string, list):
            string_list = string
        else:
            string_list = string.splitlines()
        for line in string_list:
            line = line.strip()
            words = line.split()
            if remove_blank_lines:
                if line:
                    yield line, words
            else:
                yield line, words

    def extract_episode_dialogue(self, remove_blank_lines=True):
        script = deque(self.script.splitlines())
        # Iterate through the lines until a number is found as the first character.
        while True:
            line = script.popleft()
            words = line.split()

            # Skip blank lines
            if not words:
                continue
            if any(x in words for x in ('REV', 'REV.', 'FINAL')):
                continue
            if words[0][0].isdigit():
                #  Put it back and break. Runs in O(1) time.
                script.appendleft(line)
                break

        if remove_blank_lines:
            script = list(filter(None, script))

        # Strip out the white space in lines with text
        script = [s.lstrip() for s in script]

        # Remove page header lines and lines with OMITTED in between section numbers
        dialogue = list(filter(lambda line: line[:len(self.SECTION_HEADER)] != self.SECTION_HEADER, script))
        dialogue = list(filter(lambda line: 'OMITTED' not in line or line[0][0].isdigit(), dialogue))

        self.dialogue = dialogue

        # return dialogue

    def get_characters(self):
        a = re.findall(self.regex_character, self.script)
        print(a)

    def section_headers(self):
        '''Returns the section headers from a block of dialogue and their
        respective line numbers in said block.'''

        if not self.dialogue:
            self.extract_episode_dialogue()
            # raise AttributeError('')  # 'Dialogue not found. Script.extract_entire_dialogue()')
        sections = {}
        indices = []

        for index, line in enumerate(self.dialogue):
            words = line.split()
            if not words:
                continue
            try:
                int(words[0][0])
                number = words[0]
                name = " ".join(words[1:])
                if not name:
                    name = 'OMITTED'
                # Check for same section number
                if number in sections.keys():
                    sections[number].append(name)
                else:
                    sections[number] = [name]
                indices.append(index)
            except:
                continue

        return sections, indices

    def sectioned_script(self): #, combine_same_sections=True):
        if not self.dialogue:
            self.extract_episode_dialogue()
        script = deque(self.dialogue)
        sections = {}
        section_number = ''
        section_header = ''
        temp_section = {}

        while len(script) > 0:

            line = script.popleft().split()
            if line[0][0].isdigit():
                # Check for duplicate section number and section header.
                current_number = line[0]
                current_header = ' '.join(line[1:])
                if section_number == current_number:
                    if section_header == current_header:
                        continue
                    else:
                        section_header = current_header
                else:
                    # Dump the temp section to its number and reset the temp section.
                    # TODO: Check for same section number
                    if section_number:
                        if section_header == current_header:
                            continue
                        sections[section_number].append(temp_section)
                        del temp_section
                        temp_section = dict(section_header=section_header, text=[])
                    section_number = current_number
                    section_header = current_header

                # Check if section exists and create new list if not.
                if section_number not in sections:
                    sections[section_number] = []
            else:
                temp_section['text'].append(' '.join(line))

        return sections

class ScriptLines(ScriptBase):


    # regex to get everything between two brackets if it is the only thing in the line.
    _regex_header = r'^\[([^\]]+?)\]$'
    regex_header = re.compile(_regex_header)
    # regex to match line starting with capitalized words with a colon, signifying character dialogue.
    _regex_character = r'^([A-Z]{1,}.+):'
    regex_character = re.compile(_regex_character)
    # regex to match everything after the character name, colon, and space
    _regex_dialogue_line = r'^[A-Z]{1,}.+:\s*(.+)'
    regex_dialogue_line = re.compile(_regex_dialogue_line)

    def extract_episode_dialogue(self, remove_blank_lines=False):
        script = deque(self.script.split('\n'))
        # Iterate through the lines until a number is found as the first character.
        while True:
            line = script.popleft()
            words = line.split()

            # Skip blank lines
            if not words:
                continue
            if words[0][0].isdigit():
                #  Put it back and break. Runs in O(1) time.
                script.appendleft(line)
                break

        if remove_blank_lines:
            script = list(filter(None, script))

        # Strip out the white space in lines with text
        script = [s.lstrip() for s in script]

        # Remove page header lines and lines with OMITTED in between section numbers
        dialogue = list(filter(lambda line: line[:len(self.SECTION_HEADER)] != self.SECTION_HEADER, script))
        dialogue = list(filter(lambda line: 'OMITTED' not in line or line[0][0].isdigit(), dialogue))

        self.dialogue = dialogue

        return dialogue

    def section_headers(self):
        '''Returns the section headers from a block of dialogue and their
        respective line numbers in said block.'''
        if not self.script:
            raise AttributeError('')  # 'Dialogue not found. Script.extract_entire_dialogue()')
        sections = {}
        indices = []

        for index, line in enumerate(self.script):
            words = line.split()
            if not words:
                continue
            try:
                int(words[0][0])
                number = words[0]
                name = " ".join(words[1:])
                if not name:
                    name = 'OMITTED'
                # Check for same section number
                if number in sections.keys():
                    sections[number].append(name)
                else:
                    sections[number] = [name]
                indices.append(index)
            except:
                continue

        return sections, indices

    def sectioned_script(self):
        script = deque(self.script)
        sections = {}
        section_number = 0

        while len(script) > 0:
            line = script.popleft().split()
            if line[0][0].isdigit():
                # Check for duplicate section number
                if line[0] == section_number:
                    continue
                else:
                    section_number = line[0]
                    sections[section_number] = {}
                    sections[section_number]['section_header'] = ' '.join(line[1:])
                    sections[section_number]['text'] = []
            else:
                sections[section_number]['text'].append(' '.join(line))

        return sections

    def _check_header(self, line: str, starts_with='(', ends_with=')'):
        if line.strip().startswith(starts_with) and line.strip().endswith(ends_with):
            return True
        return False

class ScriptTNG(ScriptBlocks):
    """Script class for The Next Generation."""
    SECTION_HEADER = 'STAR TREK'
    pass

class ScriptDeepSpaceNine(ScriptBlocks):
    """Script class for Deep Space Nine."""
    SECTION_HEADER = 'DEEP SPACE'
    pass

class ScriptEnterprise(ScriptLines):
    """Script class for Enterprise."""
    pass

class ScriptTOS(ScriptLines):
    """Script class for The Original Series."""
    pass

class ScriptVoyager(ScriptLines):
    """Script class for Voyager."""
    pass