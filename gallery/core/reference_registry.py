from .models import (
    Character,
    Domain,
    Region,
    Race,
    Affiliation,
    StoryFragment,
    TriviaEntry,
    Submerge,
    Flora,
    Fauna,
    Landmark
)


REFERENCEABLE_MODELS = {
    "character": Character,
    "domain": Domain,
    "region": Region,
    "race": Race,
    "affiliation": Affiliation,
    "story": StoryFragment,
    "trivia": TriviaEntry,
    "submerge": Submerge,
    "flora": Flora,
    "fauna": Fauna,
    "landmark": Landmark,
}