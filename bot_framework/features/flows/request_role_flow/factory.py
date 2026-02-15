from bot_framework.features.flows.request_role_flow.actions import (
    RoleAssigner,
    RoleRejectionNotifier,
    RoleRequestSender,
)
from bot_framework.features.flows.request_role_flow.handlers import (
    ApproveRoleHandler,
    RejectRoleHandler,
    RequestRoleCommandHandler,
    RoleSelectionHandler,
    ShowRolesHandler,
)
from bot_framework.features.flows.request_role_flow.presenters import RoleListPresenter
from bot_framework.features.flows.request_role_flow.protocols import (
    IRequestRoleFlowRouter,
    IRequestRoleFlowStateStorage,
)
from bot_framework.features.flows.request_role_flow.request_role_flow_router import (
    RequestRoleFlowRouter,
)
from bot_framework.domain.language_management.repos.protocols.i_phrase_repo import (
    IPhraseRepo,
)
from bot_framework.core.protocols.i_callback_answerer import ICallbackAnswerer
from bot_framework.core.protocols.i_callback_handler_registry import (
    ICallbackHandlerRegistry,
)
from bot_framework.core.protocols.i_message_handler_registry import (
    IMessageHandlerRegistry,
)
from bot_framework.core.protocols.i_message_sender import IMessageSender
from bot_framework.domain.role_management.repos.protocols.i_role_repo import IRoleRepo
from bot_framework.domain.role_management.repos.protocols.i_user_repo import IUserRepo


class RequestRoleFlowFactory:
    def __init__(
        self,
        callback_answerer: ICallbackAnswerer,
        message_sender: IMessageSender,
        phrase_repo: IPhraseRepo,
        role_repo: IRoleRepo,
        user_repo: IUserRepo,
        state_storage: IRequestRoleFlowStateStorage,
    ) -> None:
        self.callback_answerer = callback_answerer
        self.message_sender = message_sender
        self.phrase_repo = phrase_repo
        self.role_repo = role_repo
        self.user_repo = user_repo
        self.state_storage = state_storage

        self._show_roles_handler: ShowRolesHandler | None = None
        self._role_selection_handler: RoleSelectionHandler | None = None
        self._approve_handler: ApproveRoleHandler | None = None
        self._reject_handler: RejectRoleHandler | None = None

    def _get_approve_handler(self) -> ApproveRoleHandler:
        if self._approve_handler is None:
            self._approve_handler = ApproveRoleHandler(
                callback_answerer=self.callback_answerer,
                user_repo=self.user_repo,
                role_assigner=RoleAssigner(
                    message_sender=self.message_sender,
                    phrase_repo=self.phrase_repo,
                    role_repo=self.role_repo,
                ),
            )
        return self._approve_handler

    def _get_reject_handler(self) -> RejectRoleHandler:
        if self._reject_handler is None:
            self._reject_handler = RejectRoleHandler(
                callback_answerer=self.callback_answerer,
                user_repo=self.user_repo,
                role_rejection_notifier=RoleRejectionNotifier(
                    message_sender=self.message_sender,
                    phrase_repo=self.phrase_repo,
                ),
            )
        return self._reject_handler

    def _get_role_selection_handler(self) -> RoleSelectionHandler:
        if self._role_selection_handler is None:
            approve_handler = self._get_approve_handler()
            reject_handler = self._get_reject_handler()

            self._role_selection_handler = RoleSelectionHandler(
                callback_answerer=self.callback_answerer,
                message_sender=self.message_sender,
                phrase_repo=self.phrase_repo,
                role_repo=self.role_repo,
                user_repo=self.user_repo,
                state_storage=self.state_storage,
                role_request_sender=RoleRequestSender(
                    message_sender=self.message_sender,
                    phrase_repo=self.phrase_repo,
                    user_repo=self.user_repo,
                    approve_handler_prefix=approve_handler.prefix,
                    reject_handler_prefix=reject_handler.prefix,
                ),
            )
        return self._role_selection_handler

    def _get_show_roles_handler(self) -> ShowRolesHandler:
        if self._show_roles_handler is None:
            role_selection_handler = self._get_role_selection_handler()

            self._show_roles_handler = ShowRolesHandler(
                callback_answerer=self.callback_answerer,
                role_list_presenter=RoleListPresenter(
                    message_sender=self.message_sender,
                    phrase_repo=self.phrase_repo,
                    role_repo=self.role_repo,
                    role_selection_handler_prefix=role_selection_handler.prefix,
                ),
                user_repo=self.user_repo,
            )
        return self._show_roles_handler

    def create_router(self) -> IRequestRoleFlowRouter:
        role_selection_handler = self._get_role_selection_handler()

        role_list_presenter = RoleListPresenter(
            message_sender=self.message_sender,
            phrase_repo=self.phrase_repo,
            role_repo=self.role_repo,
            role_selection_handler_prefix=role_selection_handler.prefix,
        )

        return RequestRoleFlowRouter(role_list_presenter=role_list_presenter)

    def register_handlers(
        self,
        callback_registry: ICallbackHandlerRegistry,
        message_registry: IMessageHandlerRegistry,
    ) -> None:
        callback_registry.register(self._get_show_roles_handler())
        callback_registry.register(self._get_role_selection_handler())
        callback_registry.register(self._get_approve_handler())
        callback_registry.register(self._get_reject_handler())

        router = self.create_router()
        command_handler = RequestRoleCommandHandler(
            request_role_flow_router=router,
            user_repo=self.user_repo,
        )
        message_registry.register(
            handler=command_handler,
            commands=["request_role"],
            content_types=["text"],
        )
