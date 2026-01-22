from bot_framework.entities import RoleName, User
from bot_framework.entities.bot_user import BotUser
from bot_framework.protocols import IEnsureUserExists
from bot_framework.role_management.repos.protocols.i_role_repo import IRoleRepo
from bot_framework.role_management.repos.protocols.i_user_repo import IUserRepo


class EnsureUserExists(IEnsureUserExists):
    def __init__(
        self,
        user_repo: IUserRepo,
        role_repo: IRoleRepo,
    ) -> None:
        self.user_repo = user_repo
        self.role_repo = role_repo

    def execute(
        self,
        user: BotUser,
    ) -> None:
        existing_user = self.user_repo.find_by_id(id=user.id)

        if not existing_user:
            new_user = User(
                id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                language_code=user.language_code or "en",
                is_bot=user.is_bot,
                is_premium=user.is_premium,
            )
            self.user_repo.create(entity=new_user)
            self.role_repo.assign_role_by_name(
                user_id=user.id,
                role_name=RoleName.USER,
            )
