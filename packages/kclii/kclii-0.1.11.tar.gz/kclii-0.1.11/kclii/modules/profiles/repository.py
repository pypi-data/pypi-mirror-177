from typing import Union, List

from sqlalchemy.exc import NoResultFound

from kclii.database.database import session
from kclii.error.database import NotRecordFound
from .models import ProfileModel, EnvironmentVariablesModel, CurrentModel
from .core import ProfileCoreIn, EnvironmentVariablesIn


class Repository:
    def set_profile(self, profile: ProfileModel) -> CurrentModel:
        try:
            current = session.query(CurrentModel).one()
            current.profile_id = profile.id
        except NoResultFound:
            current = CurrentModel(profile_id=profile.id)

        session.add(current)
        session.commit()
        return current

    def get_current_profile(self) -> CurrentModel:
        try:
            current = session.query(CurrentModel).one()
        except NoResultFound as error:
            raise NotRecordFound(filter_by={}) from error

        return current

    def get_all(self) -> List[ProfileModel]:
        return session.query(ProfileModel).all()

    def get_profile_by_name(self, name: str) -> Union[ProfileModel, NoResultFound]:
        try:
            saved_profile = (
                session.query(ProfileModel).filter(ProfileModel.name == name).one()
            )
        except NoResultFound as error:
            raise NotRecordFound(filter_by={ProfileModel.name, name}) from error

        return saved_profile

    def create_profile(self, profile: ProfileCoreIn) -> ProfileModel:
        new_profile = ProfileModel(name=profile.name)

        session.add(new_profile)
        session.commit()

        return new_profile

    def add_environment_variables(
        self, profile_id: int, environment_variables: List[EnvironmentVariablesIn]
    ):
        environment_variables = [
            EnvironmentVariablesModel(
                key=environment_variable.key,
                value=environment_variable.value,
                profile_id=profile_id,
            )
            for environment_variable in environment_variables
        ]

        session.add_all(environment_variables)
        session.commit()

    def delete_environment_variables(
        self,
        delete_ids: List[int],
    ):
        session.query(EnvironmentVariablesModel).filter(
            EnvironmentVariablesModel.id.in_(delete_ids)
        ).delete()
        session.commit()

    def get_environment_variables_by_profile(
        self, profile_id: int
    ) -> Union[EnvironmentVariablesModel, NoResultFound]:
        try:
            saved_environment_variables = (
                session.query(EnvironmentVariablesModel)
                .filter(EnvironmentVariablesModel.profile_id == profile_id)
                .all()
            )
        except NoResultFound as error:
            raise NotRecordFound(
                filter_by={EnvironmentVariablesModel.profile_id, profile_id}
            ) from error

        return saved_environment_variables
