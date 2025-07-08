#########################################
# Database, request and response models #
#########################################

# Imports
###################################################################################################
from sqlmodel import SQLModel, Relationship, Field
###################################################################################################


###################################################################################################
# Models
class CharacterPower(SQLModel, table=True):

    character_id: int = Field(
        default=None, primary_key=True, foreign_key="character.character_id"
    )
    power_id: int = Field(
        default=None, primary_key=True, foreign_key="powers.power_id"
    )












###################################################################################################