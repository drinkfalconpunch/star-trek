from dataclasses import dataclass

@dataclass
class Episode:
    series_name: str = ''
    season_number: int = 0
    episode_number: int = 0
    episode_name: str = ''
    alt_name: str = ''
    multi_part: bool = False
    script_file_type: str = ''
    script: str = ''