from collections import deque

OMITTED = 'OMITTED'
STAR_TREK = 'STAR TREK'

class Script:
    def __init__(self, script):
        self.script = script
        self.dialogue = None
    
    def extract_entire_dialogue(self, remove_blank_lines=False):
        script = deque(self.script.split('\n'))
        # Iterate through the lines until a number is found as the first character.
        while True:
            line = script.popleft()
            words = line.split()

            # Skip blank lines
            if not words:
                continue
            try:
                # Found the first line.
                int(words[0][0])
                #  Put it back and break. Runs in O(1) time.
                script.appendleft(line)
                break
            except ValueError:
                continue

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
        if not self.dialogue:
            raise AttributeError('Dialogue not found. Script.extract_entire_dialogue()')
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
    
    def find_actors(self):
        actors = ''
        for line in self.script.split('\n'):
            words = line.split()
            if not words:
                continue
            if len(words[0]) > 1 and all([i.isupper() for i in words]):
                # check if line starts with number and skip if true
                try:
                    int(words[0][0])
                    continue
                except:
                    pass
                print('caps', words)
                continue
            if len(line) - len(line.lstrip()) > 4:
                spoken_text = spoken_text + line.strip() + ' \n'
    
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