from typing import Tuple

def score_to_color(score: float) -> Tuple[int, int, int]:
    # colormap from red -> orange -> green
    red     = int(255 * (1 - score)) 
    green   = int(255 * score)
    return (0, green, red)
