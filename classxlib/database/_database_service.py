"""Database module that contains the DatabaseService Class
used for setting up the database tables and connection"""

# Python Standard Library Imports
import traceback
import os
import json
from datetime import datetime, timezone

# Python Third Party Imports
from sqlalchemy import create_engine
from sqlalchemy.orm import (
    sessionmaker,
    scoped_session,
    Session,
)
from sqlalchemy.orm.session import close_all_sessions
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError, DBAPIError, DatabaseError

# Local Library Imports
from ._generate_tables import generate_tables
from .service import (
    UserService,
    UserLevelService,
    OriginalImageService,
    CropImageService,
    TrainingFileService,
    SegmentImageService,
    LabelImageService,
    ResearchFieldService,
    UserFriendService,
    UserResearchFieldService,
)
from .model import User, UserLevel, ResearchField

__all__ = ["DatabaseService"]


# pylint: disable = too-many-instance-attributes
class DatabaseService:
    """The service class for setting up the database."""

    user_service: UserService
    user_level_service: UserLevelService
    original_image_service: OriginalImageService
    crop_image_service: CropImageService
    segment_image_service: SegmentImageService
    label_image_service: LabelImageService
    research_field_service: ResearchFieldService
    training_file_service: TrainingFileService
    user_friend_service: UserFriendService
    user_research_fields_service: UserResearchFieldService

    def __init__(self, database_url: str, echo: bool = False):
        # Database Connection URL
        self.database_url: str = database_url

        # Whether the database engine is active
        self.active: bool = False

        # Parameter to echo the sql statements or not
        self.echo: bool = echo

        # Creating the database engine
        self.engine: Engine = self._create_db_engine(self.database_url, echo=self.echo)
        self.generate_db_tables()
        if self.active == True:
            # Creating session connection for database
            self.session: Session = self._create_session()
        
            # Creating the table services.
            self._setup_services()

            # Validate rows to make sure all defaults are in the database
            self.start_up_validation()

            # Placeholder for default user ID
            self.DEFAULT_ID: int

    def _create_db_engine(self, database_url: str, echo: bool) -> Engine:
        """Creates the database connection engine

        Args:
            database_url (str): The connection url for the database
            echo (bool): A boolean condition to echo the
            sql statements in the console
        Returns:
            Engine: The SQLAlchemy database connection engine
        """
        try:
            return create_engine(
                database_url, pool_recycle=1800, pool_pre_ping=True, echo=echo
            )
        except (SQLAlchemyError, DatabaseError, DBAPIError, RuntimeError) as error:
            print("Error creating database engine")
            traceback.print_tb(error.__traceback__)
            return False

    def generate_db_tables(self):
        """Generates the database tables. If successful sets active to
        true.

        Args:
            engine (Engine): The SQLAlchemy database connection engine
        """
        # If the engine is None then set active to False
        if self.engine is None:
            self.active = False
        # If generating tables was successful set database to active
        if not self.active and generate_tables(self.engine):
            self.active = True

    def _create_session(self) -> Session:
        """Creates the database shared session object.

        Args:
            engine (Engine): The SQLAlchemy database connection engine

        Returns:
            Session: The shared session object for the
            database services to use.
        """
        # Binding the engine to a session
        self.session_binder = sessionmaker(bind=self.engine)

        # Constructs a scoped session with the session binder
        return scoped_session(self.session_binder)

    def close_session(self):
        """Closes the database connection."""
        self.session: Session
        close_all_sessions()
        self.engine.dispose()

    def _setup_services(self) -> bool:
        try:
            # Setting up the database table services
            self.user_service = UserService(self.session)
            self.user_level_service = UserLevelService(self.session)
            self.original_image_service = OriginalImageService(self.session)
            self.crop_image_service = CropImageService(self.session)
            self.segment_image_service = SegmentImageService(self.session)
            self.label_image_service = LabelImageService(self.session)
            self.research_field_service = ResearchFieldService(self.session)
            self.training_file_service = TrainingFileService(self.session)
            self.user_friend_service = UserFriendService(self.session)
            self.user_research_fields_service = UserResearchFieldService(self.session)
            self.active = True
            default_user_obj = self.user_service.get_by_username("default")
            self.DEFAULT_ID = (
                default_user_obj.id if default_user_obj is not None else None
            )
            return True
        except (SQLAlchemyError, DatabaseError, DBAPIError, RuntimeError) as error:
            print("Error creating database services")
            traceback.print_tb(error.__traceback__)
            return False
        except Exception as error:
            print("Error:", error)
            traceback.print_tb(error.__traceback__)
            return False

    def start_up_validation(self) -> bool:
        """Function that is called on server start up. Verifies
        the Default User Exists and Default Domains Exist.
        """
        # Validating Database Setup and Structure on Startup
        print("BEGINNING SERVER START UP VALIDATION")
        # Validate User Levels
        print("Validating user levels")
        if self._validate_user_levels():
            print("User Level Validation Successful")
        else:
            print("User level validation failed")
            return False
        if self._validate_research_fields():
            print("Research Fields Validation Successful")
        else:
            print("Research Fields validation failed")
            return False
        if self._validate_users():
            print("Users Validation Successful")
        else:
            print("Users validation failed")
            return False
        return True

    def _validate_user_levels(self) -> bool:
        """Checks and validates all User Levels in the
        database to verify their existance before server launch

        Returns:
            bool: Returns True if successful and False if there is an error in validating
        """
        try:
            # Getting the default user level config path
            user_level_config_path = os.path.join(
                os.path.curdir, "classxlib/database/config/user_level.json"
            )
            # Verifying the file existance
            if os.path.isfile(user_level_config_path):
                print("User Level Config found verifying user levels")
                # Opening the config file
                with open(user_level_config_path, "r", encoding="utf-8") as user_level_config_file:
                    # Loading the json data
                    user_level_config = json.load(user_level_config_file)

                    # Looping through each user level
                    for user_level_name in user_level_config.keys():
                        print("Verifying", user_level_name, "user level")
                        # Checking if they already exist
                        user_level_obj = self.user_level_service.get_by_name(user_level_name)
                        user_level_permissions = user_level_config[user_level_name]["permissions"]

                        # If they are None it does not exist
                        if user_level_obj is None:
                            print(user_level_name, "does not exist adding to database")
                            # Creating a new UserLevel database object
                            user_level_obj = UserLevel(
                                name=user_level_name, permissions=user_level_permissions
                            )

                            # Adding it to database
                            user_level_obj = self.user_level_service.add_level(
                                user_level_obj
                            )
                            continue

                        # Verifying the permissions are up to date
                        if dict(user_level_obj.permissions) != dict(
                            user_level_permissions
                        ):
                            print(user_level_name, "permissions invalid, updating")
                            # Updating permissions if not
                            self.user_level_service.update_level_permissions(
                                user_level_id=user_level_obj.id,
                                new_permissions=user_level_permissions,
                            )
            else:
                return False
            return True
        except (TypeError, RuntimeError, ValueError, RuntimeWarning) as error:
            print("Error:", error)
            traceback.print_tb(error.__traceback__)
            return False
        except Exception as error:
            print("Error:", error)
            traceback.print_tb(error.__traceback__)
            return False

    def _validate_research_fields(self) -> bool:
        """Checks and validates all research fields in the
        database to verify their existance before server launch

        Returns:
            bool: Returns True if successful and False if there is an error in validating
        """
        try:
            # Getting the default research field config path
            research_field_config_path = os.path.join(
                os.path.curdir, "classxlib/database/config/research_field.json"
            )
            # Verifying the file existance
            if os.path.isfile(research_field_config_path):
                print("Research field Config found verifying user levels")
                # Opening the config file
                with open(
                    research_field_config_path, "r"
                ) as research_field_config_file:
                    # Loading the json data
                    research_field_config = json.load(research_field_config_file)
                    # Looping through each research field
                    for research_field_name in research_field_config.keys():
                        print("Verifying", research_field_name, "research field")

                        # Checking if they already exist
                        research_field_obj = (
                            self.research_field_service.get_default_field_by_name(
                                research_field_name
                            )
                        )

                        label_map = research_field_config[research_field_name][
                            "label_map"
                        ]
                        metadata_map = research_field_config[research_field_name][
                            "metadata_map"
                        ]
                        protocols = research_field_config[research_field_name][
                            "protocols"
                        ]

                        # If they are None it does not exist
                        if research_field_obj is None:
                            print(
                                research_field_name, "does not exist adding to database"
                            )
                            # Creating a new UserLevel database object
                            research_field_obj = ResearchField(
                                name=research_field_name,
                                user_id=None,
                                visibility=1,
                                last_modified_date=datetime.now(timezone.utc),
                                label_map=label_map,
                                metadata_map=metadata_map,
                                protocols=protocols,
                                field_data={},
                            )

                            # Adding it to database
                            research_field_obj = self.research_field_service.add_field(
                                research_field_obj
                            )
                            continue

                        # Verifying the label map is up to date
                        if (research_field_obj.label_map != \
                            research_field_config[research_field_name]["label_map"]):

                            print(research_field_name, "label map invalid, updating")

                            # Updating label map if not
                            self.research_field_service.update_label_map(
                                research_id=research_field_obj.id,
                                new_label_map=label_map,
                            )
                        # Verifying the metadata map is up to date
                        if (research_field_obj.metadata_map != \
                            research_field_config[research_field_name]["metadata_map"]):

                            print(research_field_name, "metadata map invalid, updating")

                            # Updating metadata map if not
                            self.research_field_service.update_metadata_map(
                                research_id=research_field_obj.id,
                                new_metadata_map=metadata_map,
                            )
                        # Verifying the protocols are up to date
                        if (
                            research_field_obj.protocols != research_field_config[research_field_name]["protocols"]
                        ):

                            print(research_field_name, "protocols invalid, updating")

                            # Updating protocols if not
                            self.research_field_service.update_protocols(
                                research_id=research_field_obj.id,
                                new_protocols=protocols,
                            )
                    return True
            else:
                return False

        except (TypeError, RuntimeError, ValueError, RuntimeWarning) as error:
            print("Error:", error)
            traceback.print_tb(error.__traceback__)
            return False
        except Exception as error:
            print("Error:", error)
            traceback.print_tb(error.__traceback__)
            return False

    def _validate_users(self) -> bool:
        """Validates the default user in the database

        Returns:
            bool: Returns True if successful and False
            if there is errors
        """
        try:
            # Getting default user object
            default_user_obj = self.user_service.get_by_username("default")

            # Getting the list of default research field ids
            default_field_id_list = [research_field_obj.id \
                for research_field_obj in self.research_field_service.get_default_fields()]

            # If the user object is None that means the default user has not been
            # created yet.
            if default_user_obj is None:
                print("Default user does not exist creating now")
                # Creating the default User Object
                default_user_obj = User(
                    username="default",
                    kc_uuid="temp",
                    user_level=self.user_level_service.get_by_name("Admin").id,
                )
                default_user_obj = self.user_service.add_user(default_user_obj)
            else:
                # If it has been created check and verify it's data
                if default_user_obj.kc_uuid == "temp":
                    print(
                        "The default user is not set up in keycloak.",
                        "This is a security risk please set them up.",
                    )

                # Checking it's research field ID list to make sure it has all
                # the defaults added
                # default_user_research_id_list = default_user_obj.user_data['research_fields']

                _id = default_user_obj.id
                added_research_fields = [added.research_id \
                    for added in self.user_research_fields_service.get_user_research_fields(_id)]
                print(added_research_fields)
                
                # Verifying it has them
                for research_field_id in default_field_id_list:
                    if research_field_id not in added_research_fields:
                        print(
                            f"Research Field ID {research_field_id} missing from default user adding now"
                        )
                        self.user_research_fields_service.add_research_field(
                            default_user_obj.id, research_field_id, 999
                        )
            # Setting the default user ID
            self.DEFAULT_ID = default_user_obj.id
            return True
        except Exception as error:
            print("Error:", error)
            traceback.print_tb(error.__traceback__)
            return False
