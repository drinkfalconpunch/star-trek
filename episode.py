from dataclasses import dataclass

@dataclass
class Episode:
    series_name: str
    season_number: int
    episode_number: int
    episode_name: str
    alt_name: str
    multi_part: bool
    script_file_type: str