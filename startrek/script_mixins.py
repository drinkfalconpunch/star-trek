from abc import ABCMeta, abstractmethod
from collections import deque

OMITTED = 'OMITTED'

class ScriptBase(metaclass=ABCMeta):
    def __init__(self, script=None, series_name=None, season_number=0, episode_number=0):
        self.script = script
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

class ScriptBlocks(ScriptBase):
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
        dialogue = list(filter(lambda line: line[:len(STAR_TREK)] != STAR_TREK, script))
        dialogue = list(filter(lambda line: 'OMITTED' not in line or line[0][0].isdigit(), dialogue))

        self.dialogue = dialogue

        return dialogue

    def section_headers(self):
        '''Returns the section headers from a block of dialogue and their
        respective line numbers in said block.'''
        if not self.script:
            raise AttributeError('') #'Dialogue not found. Script.extract_entire_dialogue()')
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

class ScriptLines(ScriptBase):
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
        dialogue = list(filter(lambda line: line[:len(STAR_TREK)] != STAR_TREK, script))
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
    pass

class ScriptDeepSpaceNine(ScriptBlocks):
    pass

class ScriptEnterprise(ScriptLines):
    pass

class ScriptTOS(ScriptLines):
    pass

class ScriptVoyager(ScriptLines):
    pass