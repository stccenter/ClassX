"""Module for generating all the ClassX Tables"""
# Python Standard Library Imports
import traceback

# Python Third Party Imports
from sqlalchemy.orm import mapper, relationship, clear_mappers
from sqlalchemy.engine import Engine
from sqlalchemy import MetaData
from sqlalchemy.exc import (SQLAlchemyError, DBAPIError,
                            DatabaseError)

# Local Library Imports
from .table import (create_user_level_table,create_crop_image_table,
                    create_label_image_table,create_original_image_table,
                    create_research_field_table,create_segment_image_table,
                    create_training_file_table,create_user_table,
                    create_user_friends_table, create_user_research_fields_table)
from .model import (CropImage, OriginalImage,
                    LabelImage, User,
                    UserLevel, TrainingFile,
                    ResearchField, SegmentImage,
                    UserFriend, UserResearchField)

__all__ = ['generate_tables']

def generate_tables(engine:Engine) -> bool:
    """Maps out and generates all the tables for
    the classX database

    Args:
        engine (Engine): The SQL engine object to use
        for connecting and manipulating the database.

    Returns:
        bool: Returns true if the tables are successfully made.
        Otherwise returns False if there are errors.
    """
    try:
        # Creating a shared metadata object for generating the tables
        metadata = MetaData()

        # Mapping out all the table structures
        _start_mappers(metadata)

        # Creating the tables
        metadata.create_all(engine)

        return True
    except (SQLAlchemyError, DatabaseError,
                DBAPIError, RuntimeError) as error:
            print("Error generating database tables")
            traceback.print_tb(error.__traceback__)
            return False


def _start_mappers(metadata:MetaData):
    """Maps out the relationships, columns, and structures of
    each table

    Args:
        metadata (MetaData): The shared metadata object for storing
        all of the mapped info.
    """
    # Creating the table structures
    user_table = create_user_table(metadata)
    user_level_table = create_user_level_table(metadata)
    user_friend_table = create_user_friends_table(metadata)
    user_research_field_table = create_user_research_fields_table(metadata)
    original_image_table = create_original_image_table(metadata)
    crop_image_table = create_crop_image_table(metadata)
    segment_image_table = create_segment_image_table(metadata)
    label_image_table = create_label_image_table(metadata)
    training_file_table = create_training_file_table(metadata)
    research_field_table = create_research_field_table(metadata)

    # Mapping out relationships for Users table
    mapper(User,
           user_table,
           properties = {
               'original_images' : relationship(OriginalImage,
                                                primaryjoin=user_table.c.id\
                                                    == original_image_table.c.user_id),
               'crop_images' : relationship(CropImage,
                                            primaryjoin=user_table.c.id\
                                                == crop_image_table.c.user_id),
               'segment_images' : relationship(SegmentImage,
                                               primaryjoin=user_table.c.id\
                                                   == segment_image_table.c.user_id),
               'label_images' : relationship(LabelImage,
                                             primaryjoin=user_table.c.id\
                                                 == label_image_table.c.user_id),
               'training_files': relationship(TrainingFile,
                                              primaryjoin=user_table.c.id\
                                                  == training_file_table.c.user_id),
               'user_research_fields': relationship(UserResearchField,
                                              primaryjoin=user_table.c.id\
                                                  == user_research_field_table.c.user_id),
               'user_friends': relationship(UserFriend,
                                              primaryjoin=user_table.c.id\
                                                  == user_friend_table.c.sender_id),
               'user_friends': relationship(UserFriend,
                                              primaryjoin=user_table.c.id\
                                                  == user_friend_table.c.receiver_id)
               })

    # Mapping out relationships for User Levels table
    mapper(UserLevel, user_level_table, properties = {
        'users' : relationship(User,primaryjoin=user_level_table.c.id == user_table.c.user_level)})
    

    # Mapping out relationships for User Friends table
    mapper(UserFriend, user_friend_table)

    # Mapping out relationships for User research field table
    mapper(UserResearchField, user_research_field_table)

    # Mapping out relationships for Original Images table
    mapper(OriginalImage,
           original_image_table,
           properties={
               'crop_images' : relationship(CropImage,
                                            primaryjoin=original_image_table.c.id\
                                                == crop_image_table.c.original_image_id)
           })

    # Mapping out relationships for Crop Images table
    mapper(CropImage,
           crop_image_table,
           properties = {
               'segment_images' : relationship(SegmentImage,
                                               primaryjoin=crop_image_table.c.id\
                                                   == segment_image_table.c.crop_image_id)
    })

    # Mapping out relationships for Segment Images table
    mapper(SegmentImage,
           segment_image_table,
           properties = {
               'label_images' : relationship(LabelImage,
                                             primaryjoin=segment_image_table.c.id\
                                                 == label_image_table.c.segment_image_id)})

    # Mapping out relationships for Label Images table
    mapper(LabelImage, label_image_table)

    # Mapping out relationships for Training Files table
    mapper(TrainingFile,
           training_file_table,
           properties = {'label_images':relationship(LabelImage,
                                                     primaryjoin=training_file_table.c.id\
                                                         == label_image_table.c.training_file_id)})

    # Mapping out relationships for Research Fields table
    mapper(ResearchField, research_field_table,properties = {
        'original_images' : relationship(OriginalImage,
                                         primaryjoin=research_field_table.c.id\
                                             == original_image_table.c.research_id),
        'crop_images' : relationship(CropImage,
                                     primaryjoin=research_field_table.c.id\
                                         == crop_image_table.c.research_id),
        'segment_images' : relationship(SegmentImage,
                                        primaryjoin=research_field_table.c.id\
                                            == segment_image_table.c.research_id),
        'training_files' : relationship(TrainingFile,
                                        primaryjoin=research_field_table.c.id\
                                            == training_file_table.c.research_id),
        'user_research_fields': relationship(UserResearchField,
                                              primaryjoin=research_field_table.c.id\
                                                  == user_research_field_table.c.research_id)
        })
