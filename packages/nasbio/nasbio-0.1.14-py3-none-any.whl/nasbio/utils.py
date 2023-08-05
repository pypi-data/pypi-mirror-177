from typing import Optional
from enum import Enum
import operator

import strawberry

operator_keys = {
    '': operator.eq,
    '>': operator.ge,
    '<': operator.le,
}


@strawberry.enum(description='Selection of organisms.')
class OrganismSelect(Enum):
    NONE = ''
    HUMAN = 'human'
    MOUSE = 'mouse'
    RAT = 'rat'


@strawberry.input
class InputWithOrganism:
    organism: Optional[OrganismSelect] = OrganismSelect.NONE
