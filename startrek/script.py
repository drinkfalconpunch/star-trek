from collections import deque
from startrek.exceptions import ScriptException
from startrek.script_mixins import ScriptTNG, ScriptEnterprise, ScriptTOS, ScriptVoyager, ScriptDeepSpaceNine

class Script:
    def __new__(cls, show_name=None, script_text=None, script_path=None):
        if not show_name:
            # Try to infer show from scripts.
            pass
        else:
            if show_name == 'tng':
                return ScriptTNG(script_text, script_path)
            elif show_name == 'voyager':
                return ScriptVoyager(script_text, script_path)
            elif show_name == 'tos':
                return ScriptTOS(script_text, script_path)
            elif show_name == 'ds9':
                return ScriptDeepSpaceNine(script_text, script_path)
            elif show_name == 'enterprise':
                return ScriptEnterprise(script_text, script_path)
            else:
                raise ScriptException('Invalid series.')