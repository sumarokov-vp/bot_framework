# Standard Library
from abc import ABC

# Third Party Stuff
from _typeshed import Incomplete
from telebot import service_utils as service_utils
from telebot.formatting import (
    apply_html_entities as apply_html_entities,
)

DISABLE_KEYLEN_ERROR: bool
logger: Incomplete

class JsonSerializable:
    def to_json(self) -> str|None: ...

class Dictionaryable:
    def to_dict(self) -> dict|None: ...

class JsonDeserializable:
    @classmethod
    def de_json(cls, json_string) -> None: ...
    @staticmethod
    def check_json(json_type, dict_copy: bool = True): ...

class Update(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    update_id: Incomplete
    message: Incomplete
    edited_message: Incomplete
    channel_post: Incomplete
    edited_channel_post: Incomplete
    inline_query: Incomplete
    chosen_inline_result: Incomplete
    callback_query: Incomplete
    shipping_query: Incomplete
    pre_checkout_query: Incomplete
    poll: Incomplete
    poll_answer: Incomplete
    my_chat_member: Incomplete
    chat_member: Incomplete
    chat_join_request: Incomplete
    message_reaction: Incomplete
    message_reaction_count: Incomplete
    removed_chat_boost: Incomplete
    chat_boost: Incomplete
    business_connection: Incomplete
    business_message: Incomplete
    edited_business_message: Incomplete
    deleted_business_messages: Incomplete
    def __init__(self, update_id, message, edited_message, channel_post, edited_channel_post, inline_query, chosen_inline_result, callback_query, shipping_query, pre_checkout_query, poll, poll_answer, my_chat_member, chat_member, chat_join_request, message_reaction, message_reaction_count, removed_chat_boost, chat_boost, business_connection, business_message, edited_business_message, deleted_business_messages, **kwargs) -> None: ...

class ChatMemberUpdated(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    chat: Incomplete
    from_user: Incomplete
    date: Incomplete
    old_chat_member: Incomplete
    new_chat_member: Incomplete
    invite_link: Incomplete
    via_join_request: Incomplete
    via_chat_folder_invite_link: Incomplete
    def __init__(self, chat, from_user, date, old_chat_member, new_chat_member, invite_link: Incomplete | None = None, via_join_request: Incomplete | None = None, via_chat_folder_invite_link: Incomplete | None = None, **kwargs) -> None: ...
    @property
    def difference(self) -> dict[str, list]: ...

class ChatJoinRequest(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    chat: Incomplete
    from_user: Incomplete
    date: Incomplete
    bio: Incomplete
    invite_link: Incomplete
    user_chat_id: Incomplete
    def __init__(self, chat, from_user, user_chat_id, date, bio: Incomplete | None = None, invite_link: Incomplete | None = None, **kwargs) -> None: ...

class WebhookInfo(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    url: Incomplete
    has_custom_certificate: Incomplete
    pending_update_count: Incomplete
    ip_address: Incomplete
    last_error_date: Incomplete
    last_error_message: Incomplete
    last_synchronization_error_date: Incomplete
    max_connections: Incomplete
    allowed_updates: Incomplete
    def __init__(self, url, has_custom_certificate, pending_update_count, ip_address: Incomplete | None = None, last_error_date: Incomplete | None = None, last_error_message: Incomplete | None = None, last_synchronization_error_date: Incomplete | None = None, max_connections: Incomplete | None = None, allowed_updates: Incomplete | None = None, **kwargs) -> None: ...

class User(JsonDeserializable, Dictionaryable, JsonSerializable):
    @classmethod
    def de_json(cls, json_string): ...
    id: Incomplete
    is_bot: Incomplete
    first_name: Incomplete
    username: Incomplete
    last_name: Incomplete
    language_code: Incomplete
    can_join_groups: Incomplete
    can_read_all_group_messages: Incomplete
    supports_inline_queries: Incomplete
    is_premium: Incomplete
    added_to_attachment_menu: Incomplete
    can_connect_to_business: Incomplete
    def __init__(self, id, is_bot, first_name, last_name: Incomplete | None = None, username: Incomplete | None = None, language_code: Incomplete | None = None, can_join_groups: Incomplete | None = None, can_read_all_group_messages: Incomplete | None = None, supports_inline_queries: Incomplete | None = None, is_premium: Incomplete | None = None, added_to_attachment_menu: Incomplete | None = None, can_connect_to_business: Incomplete | None = None, **kwargs) -> None: ...
    @property
    def full_name(self): ...
    def to_json(self): ...
    def to_dict(self): ...

class GroupChat(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    id: Incomplete
    title: Incomplete
    def __init__(self, id, title, **kwargs) -> None: ...

class ChatFullInfo(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    id: Incomplete
    type: Incomplete
    title: Incomplete
    username: Incomplete
    first_name: Incomplete
    last_name: Incomplete
    is_forum: Incomplete
    max_reaction_count: Incomplete
    photo: Incomplete
    bio: Incomplete
    join_to_send_messages: Incomplete
    join_by_request: Incomplete
    has_private_forwards: Incomplete
    has_restricted_voice_and_video_messages: Incomplete
    description: Incomplete
    invite_link: Incomplete
    pinned_message: Incomplete
    permissions: Incomplete
    slow_mode_delay: Incomplete
    message_auto_delete_time: Incomplete
    has_protected_content: Incomplete
    sticker_set_name: Incomplete
    can_set_sticker_set: Incomplete
    linked_chat_id: Incomplete
    location: Incomplete
    active_usernames: Incomplete
    emoji_status_custom_emoji_id: Incomplete
    has_hidden_members: Incomplete
    has_aggressive_anti_spam_enabled: Incomplete
    emoji_status_expiration_date: Incomplete
    available_reactions: Incomplete
    accent_color_id: Incomplete
    background_custom_emoji_id: Incomplete
    profile_accent_color_id: Incomplete
    profile_background_custom_emoji_id: Incomplete
    has_visible_history: Incomplete
    unrestrict_boost_count: Incomplete
    custom_emoji_sticker_set_name: Incomplete
    business_intro: Incomplete
    business_location: Incomplete
    business_opening_hours: Incomplete
    personal_chat: Incomplete
    birthdate: Incomplete
    def __init__(self, id, type, title: Incomplete | None = None, username: Incomplete | None = None, first_name: Incomplete | None = None, last_name: Incomplete | None = None, photo: Incomplete | None = None, bio: Incomplete | None = None, has_private_forwards: Incomplete | None = None, description: Incomplete | None = None, invite_link: Incomplete | None = None, pinned_message: Incomplete | None = None, permissions: Incomplete | None = None, slow_mode_delay: Incomplete | None = None, message_auto_delete_time: Incomplete | None = None, has_protected_content: Incomplete | None = None, sticker_set_name: Incomplete | None = None, can_set_sticker_set: Incomplete | None = None, linked_chat_id: Incomplete | None = None, location: Incomplete | None = None, join_to_send_messages: Incomplete | None = None, join_by_request: Incomplete | None = None, has_restricted_voice_and_video_messages: Incomplete | None = None, is_forum: Incomplete | None = None, max_reaction_count: Incomplete | None = None, active_usernames: Incomplete | None = None, emoji_status_custom_emoji_id: Incomplete | None = None, has_hidden_members: Incomplete | None = None, has_aggressive_anti_spam_enabled: Incomplete | None = None, emoji_status_expiration_date: Incomplete | None = None, available_reactions: Incomplete | None = None, accent_color_id: Incomplete | None = None, background_custom_emoji_id: Incomplete | None = None, profile_accent_color_id: Incomplete | None = None, profile_background_custom_emoji_id: Incomplete | None = None, has_visible_history: Incomplete | None = None, unrestrict_boost_count: Incomplete | None = None, custom_emoji_sticker_set_name: Incomplete | None = None, business_intro: Incomplete | None = None, business_location: Incomplete | None = None, business_opening_hours: Incomplete | None = None, personal_chat: Incomplete | None = None, birthdate: Incomplete | None = None, **kwargs) -> None: ...

class Chat(ChatFullInfo): ...

class MessageID(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    message_id: Incomplete
    def __init__(self, message_id, **kwargs) -> None: ...

class WebAppData(JsonDeserializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string): ...
    data: Incomplete
    button_text: Incomplete
    def __init__(self, data, button_text, **kwargs) -> None: ...
    def to_dict(self): ...

class Message(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    @classmethod
    def parse_chat(cls, chat): ...
    @classmethod
    def parse_photo(cls, photo_size_array): ...
    @classmethod
    def parse_entities(cls, message_entity_array): ...
    content_type: Incomplete
    id: Incomplete
    message_id: Incomplete
    from_user: Incomplete
    date: Incomplete
    chat: Incomplete
    sender_chat: Incomplete
    is_automatic_forward: Incomplete
    reply_to_message: Incomplete
    via_bot: Incomplete
    edit_date: Incomplete
    has_protected_content: Incomplete
    media_group_id: Incomplete
    author_signature: Incomplete
    text: Incomplete
    entities: Incomplete
    caption_entities: Incomplete
    audio: Incomplete
    document: Incomplete
    photo: Incomplete
    sticker: Incomplete
    video: Incomplete
    video_note: Incomplete
    voice: Incomplete
    caption: Incomplete
    contact: Incomplete
    location: Incomplete
    venue: Incomplete
    animation: Incomplete
    dice: Incomplete
    new_chat_members: Incomplete
    left_chat_member: Incomplete
    new_chat_title: Incomplete
    new_chat_photo: Incomplete
    delete_chat_photo: Incomplete
    group_chat_created: Incomplete
    supergroup_chat_created: Incomplete
    channel_chat_created: Incomplete
    migrate_to_chat_id: Incomplete
    migrate_from_chat_id: Incomplete
    pinned_message: Incomplete
    invoice: Incomplete
    successful_payment: Incomplete
    connected_website: Incomplete
    reply_markup: Incomplete
    message_thread_id: Incomplete
    is_topic_message: Incomplete
    chat_background_set: Incomplete
    forum_topic_created: Incomplete
    forum_topic_closed: Incomplete
    forum_topic_reopened: Incomplete
    has_media_spoiler: Incomplete
    forum_topic_edited: Incomplete
    general_forum_topic_hidden: Incomplete
    general_forum_topic_unhidden: Incomplete
    write_access_allowed: Incomplete
    users_shared: Incomplete
    chat_shared: Incomplete
    story: Incomplete
    external_reply: Incomplete
    quote: Incomplete
    link_preview_options: Incomplete
    giveaway_created: Incomplete
    giveaway: Incomplete
    giveaway_winners: Incomplete
    giveaway_completed: Incomplete
    forward_origin: Incomplete
    boost_added: Incomplete
    sender_boost_count: Incomplete
    reply_to_story: Incomplete
    sender_business_bot: Incomplete
    business_connection_id: Incomplete
    is_from_offline: Incomplete
    effect_id: Incomplete
    show_caption_above_media: Incomplete
    json: Incomplete
    def __init__(self, message_id, from_user, date, chat, content_type, options, json_string) -> None: ...
    @property
    def html_text(self): ...
    @property
    def html_caption(self): ...
    @property
    def voice_chat_scheduled(self): ...
    @property
    def voice_chat_started(self): ...
    @property
    def voice_chat_ended(self): ...
    @property
    def voice_chat_participants_invited(self): ...
    @property
    def new_chat_member(self) -> None: ...
    @property
    def forward_from(self): ...
    @property
    def forward_from_chat(self): ...
    @property
    def forward_from_message_id(self): ...
    @property
    def forward_signature(self): ...
    @property
    def forward_sender_name(self): ...
    @property
    def forward_date(self): ...
    @property
    def user_shared(self): ...

class MessageEntity(Dictionaryable, JsonSerializable, JsonDeserializable):
    @staticmethod
    def to_list_of_dicts(entity_list) -> list[dict] | None: ...
    @classmethod
    def de_json(cls, json_string): ...
    type: Incomplete
    offset: Incomplete
    length: Incomplete
    url: Incomplete
    user: Incomplete
    language: Incomplete
    custom_emoji_id: Incomplete
    def __init__(self, type, offset, length, url: Incomplete | None = None, user: Incomplete | None = None, language: Incomplete | None = None, custom_emoji_id: Incomplete | None = None, **kwargs) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class Dice(JsonSerializable, Dictionaryable, JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    value: Incomplete
    emoji: Incomplete
    def __init__(self, value, emoji, **kwargs) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class PhotoSize(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    file_id: Incomplete
    file_unique_id: Incomplete
    width: Incomplete
    height: Incomplete
    file_size: Incomplete
    def __init__(self, file_id, file_unique_id, width, height, file_size: Incomplete | None = None, **kwargs) -> None: ...

class Audio(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    file_id: Incomplete
    file_unique_id: Incomplete
    duration: Incomplete
    performer: Incomplete
    title: Incomplete
    file_name: Incomplete
    mime_type: Incomplete
    file_size: Incomplete
    thumbnail: Incomplete
    def __init__(self, file_id, file_unique_id, duration, performer: Incomplete | None = None, title: Incomplete | None = None, file_name: Incomplete | None = None, mime_type: Incomplete | None = None, file_size: Incomplete | None = None, thumbnail: Incomplete | None = None, **kwargs) -> None: ...
    @property
    def thumb(self): ...

class Voice(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    file_id: Incomplete
    file_unique_id: Incomplete
    duration: Incomplete
    mime_type: Incomplete
    file_size: Incomplete
    def __init__(self, file_id, file_unique_id, duration, mime_type: Incomplete | None = None, file_size: Incomplete | None = None, **kwargs) -> None: ...

class Document(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    file_id: Incomplete
    file_unique_id: Incomplete
    thumbnail: Incomplete
    file_name: Incomplete
    mime_type: Incomplete
    file_size: Incomplete
    def __init__(self, file_id, file_unique_id, thumbnail: Incomplete | None = None, file_name: Incomplete | None = None, mime_type: Incomplete | None = None, file_size: Incomplete | None = None, **kwargs) -> None: ...
    @property
    def thumb(self): ...

class Video(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    file_id: Incomplete
    file_unique_id: Incomplete
    width: Incomplete
    height: Incomplete
    duration: Incomplete
    thumbnail: Incomplete
    file_name: Incomplete
    mime_type: Incomplete
    file_size: Incomplete
    def __init__(self, file_id, file_unique_id, width, height, duration, thumbnail: Incomplete | None = None, file_name: Incomplete | None = None, mime_type: Incomplete | None = None, file_size: Incomplete | None = None, **kwargs) -> None: ...
    @property
    def thumb(self): ...

class VideoNote(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    file_id: Incomplete
    file_unique_id: Incomplete
    length: Incomplete
    duration: Incomplete
    thumbnail: Incomplete
    file_size: Incomplete
    def __init__(self, file_id, file_unique_id, length, duration, thumbnail: Incomplete | None = None, file_size: Incomplete | None = None, **kwargs) -> None: ...
    @property
    def thumb(self): ...

class Contact(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    phone_number: Incomplete
    first_name: Incomplete
    last_name: Incomplete
    user_id: Incomplete
    vcard: Incomplete
    def __init__(self, phone_number, first_name, last_name: Incomplete | None = None, user_id: Incomplete | None = None, vcard: Incomplete | None = None, **kwargs) -> None: ...

class Location(JsonDeserializable, JsonSerializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string): ...
    longitude: Incomplete
    latitude: Incomplete
    horizontal_accuracy: Incomplete
    live_period: Incomplete
    heading: Incomplete
    proximity_alert_radius: Incomplete
    def __init__(self, longitude, latitude, horizontal_accuracy: Incomplete | None = None, live_period: Incomplete | None = None, heading: Incomplete | None = None, proximity_alert_radius: Incomplete | None = None, **kwargs) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class Venue(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    location: Incomplete
    title: Incomplete
    address: Incomplete
    foursquare_id: Incomplete
    foursquare_type: Incomplete
    google_place_id: Incomplete
    google_place_type: Incomplete
    def __init__(self, location, title, address, foursquare_id: Incomplete | None = None, foursquare_type: Incomplete | None = None, google_place_id: Incomplete | None = None, google_place_type: Incomplete | None = None, **kwargs) -> None: ...

class UserProfilePhotos(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    total_count: Incomplete
    photos: Incomplete
    def __init__(self, total_count, photos: Incomplete | None = None, **kwargs) -> None: ...

class File(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    file_id: Incomplete
    file_unique_id: Incomplete
    file_size: Incomplete
    file_path: Incomplete
    def __init__(self, file_id, file_unique_id, file_size: Incomplete | None = None, file_path: Incomplete | None = None, **kwargs) -> None: ...

class ForceReply(JsonSerializable):
    selective: Incomplete
    input_field_placeholder: Incomplete
    def __init__(self, selective: bool | None = None, input_field_placeholder: str | None = None) -> None: ...
    def to_json(self): ...

class ReplyKeyboardRemove(JsonSerializable):
    selective: Incomplete
    def __init__(self, selective: Incomplete | None = None) -> None: ...
    def to_json(self): ...

class WebAppInfo(JsonDeserializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string): ...
    url: Incomplete
    def __init__(self, url, **kwargs) -> None: ...
    def to_dict(self): ...

class ReplyKeyboardMarkup(JsonSerializable):
    max_row_keys: int
    resize_keyboard: Incomplete
    one_time_keyboard: Incomplete
    selective: Incomplete
    row_width: Incomplete
    input_field_placeholder: Incomplete
    keyboard: Incomplete
    is_persistent: Incomplete
    def __init__(self, resize_keyboard: bool | None = None, one_time_keyboard: bool | None = None, selective: bool | None = None, row_width: int = 3, input_field_placeholder: str | None = None, is_persistent: bool | None = None) -> None: ...
    def add(self, *args, row_width: Incomplete | None = None): ...
    def row(self, *args): ...
    def to_json(self): ...

class KeyboardButtonPollType(Dictionaryable):
    type: Incomplete
    def __init__(self, type: Incomplete | None = None) -> None: ...
    def to_dict(self): ...

class KeyboardButtonRequestUsers(Dictionaryable):
    request_id: Incomplete
    user_is_bot: Incomplete
    user_is_premium: Incomplete
    max_quantity: Incomplete
    request_name: Incomplete
    request_username: Incomplete
    request_photo: Incomplete
    def __init__(self, request_id: int, user_is_bot: bool | None = None, user_is_premium: bool | None = None, max_quantity: int | None = None, request_name: str | None = None, request_username: bool | None = None, request_photo: bool | None = None) -> None: ...
    def to_dict(self) -> dict|None: ...

class KeyboardButtonRequestUser(KeyboardButtonRequestUsers):
    def __init__(self, request_id: int, user_is_bot: bool | None = None, user_is_premium: bool | None = None, max_quantity: int | None = None) -> None: ...

class KeyboardButtonRequestChat(Dictionaryable):
    request_id: Incomplete
    chat_is_channel: Incomplete
    chat_is_forum: Incomplete
    chat_has_username: Incomplete
    chat_is_created: Incomplete
    user_administrator_rights: Incomplete
    bot_administrator_rights: Incomplete
    bot_is_member: Incomplete
    request_title: Incomplete
    request_photo: Incomplete
    request_username: Incomplete
    def __init__(self, request_id: int, chat_is_channel: bool, chat_is_forum: bool | None = None, chat_has_username: bool | None = None, chat_is_created: bool | None = None, user_administrator_rights: ChatAdministratorRights | None = None, bot_administrator_rights: ChatAdministratorRights | None = None, bot_is_member: bool | None = None, request_title: str | None = None, request_photo: bool | None = None, request_username: bool | None = None) -> None: ...
    def to_dict(self) -> dict: ...

class KeyboardButton(Dictionaryable, JsonSerializable):
    text: Incomplete
    request_contact: Incomplete
    request_location: Incomplete
    request_poll: Incomplete
    web_app: Incomplete
    request_chat: Incomplete
    request_users: Incomplete
    def __init__(self, text: str, request_contact: bool | None = None, request_location: bool | None = None, request_poll: KeyboardButtonPollType | None = None, web_app: WebAppInfo | None = None, request_user: KeyboardButtonRequestUser | None = None, request_chat: KeyboardButtonRequestChat | None = None, request_users: KeyboardButtonRequestUsers | None = None) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class InlineKeyboardMarkup(Dictionaryable, JsonSerializable, JsonDeserializable):
    max_row_keys: int
    @classmethod
    def de_json(cls, json_string): ...
    row_width: Incomplete
    keyboard: Incomplete
    def __init__(self, keyboard: Incomplete | None = None, row_width: int = 3) -> None: ...
    def add(self, *args, row_width: Incomplete | None = None): ...
    def row(self, *args): ...
    def to_json(self): ...
    def to_dict(self): ...

class InlineKeyboardButton(Dictionaryable, JsonSerializable, JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    text: Incomplete
    url: Incomplete
    callback_data: Incomplete
    web_app: Incomplete
    switch_inline_query: Incomplete
    switch_inline_query_current_chat: Incomplete
    switch_inline_query_chosen_chat: Incomplete
    callback_game: Incomplete
    pay: Incomplete
    login_url: Incomplete
    def __init__(self, text, url: Incomplete | None = None, callback_data: Incomplete | None = None, web_app: Incomplete | None = None, switch_inline_query: Incomplete | None = None, switch_inline_query_current_chat: Incomplete | None = None, switch_inline_query_chosen_chat: Incomplete | None = None, callback_game: Incomplete | None = None, pay: Incomplete | None = None, login_url: Incomplete | None = None, **kwargs) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class LoginUrl(Dictionaryable, JsonSerializable, JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    url: Incomplete
    forward_text: Incomplete
    bot_username: Incomplete
    request_write_access: Incomplete
    def __init__(self, url, forward_text: Incomplete | None = None, bot_username: Incomplete | None = None, request_write_access: Incomplete | None = None, **kwargs) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class CallbackQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    id: Incomplete
    from_user: Incomplete
    message: Incomplete
    inline_message_id: Incomplete
    chat_instance: Incomplete
    data: Incomplete
    game_short_name: Incomplete
    json: Incomplete
    def __init__(self, id, from_user, data, chat_instance, json_string, message: Incomplete | None = None, inline_message_id: Incomplete | None = None, game_short_name: Incomplete | None = None, **kwargs) -> None: ...

class ChatPhoto(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    small_file_id: Incomplete
    small_file_unique_id: Incomplete
    big_file_id: Incomplete
    big_file_unique_id: Incomplete
    def __init__(self, small_file_id, small_file_unique_id, big_file_id, big_file_unique_id, **kwargs) -> None: ...

class ChatMember(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    user: Incomplete
    status: Incomplete
    custom_title: Incomplete
    is_anonymous: Incomplete
    can_be_edited: Incomplete
    can_post_messages: Incomplete
    can_edit_messages: Incomplete
    can_delete_messages: Incomplete
    can_restrict_members: Incomplete
    can_promote_members: Incomplete
    can_change_info: Incomplete
    can_invite_users: Incomplete
    can_pin_messages: Incomplete
    is_member: Incomplete
    can_send_messages: Incomplete
    can_send_polls: Incomplete
    can_send_other_messages: Incomplete
    can_add_web_page_previews: Incomplete
    can_manage_chat: Incomplete
    can_manage_video_chats: Incomplete
    until_date: Incomplete
    can_manage_topics: Incomplete
    can_send_audios: Incomplete
    can_send_documents: Incomplete
    can_send_photos: Incomplete
    can_send_videos: Incomplete
    can_send_video_notes: Incomplete
    can_send_voice_notes: Incomplete
    can_post_stories: Incomplete
    can_edit_stories: Incomplete
    can_delete_stories: Incomplete
    def __init__(self, user, status, custom_title: Incomplete | None = None, is_anonymous: Incomplete | None = None, can_be_edited: Incomplete | None = None, can_post_messages: Incomplete | None = None, can_edit_messages: Incomplete | None = None, can_delete_messages: Incomplete | None = None, can_restrict_members: Incomplete | None = None, can_promote_members: Incomplete | None = None, can_change_info: Incomplete | None = None, can_invite_users: Incomplete | None = None, can_pin_messages: Incomplete | None = None, is_member: Incomplete | None = None, can_send_messages: Incomplete | None = None, can_send_audios: Incomplete | None = None, can_send_documents: Incomplete | None = None, can_send_photos: Incomplete | None = None, can_send_videos: Incomplete | None = None, can_send_video_notes: Incomplete | None = None, can_send_voice_notes: Incomplete | None = None, can_send_polls: Incomplete | None = None, can_send_other_messages: Incomplete | None = None, can_add_web_page_previews: Incomplete | None = None, can_manage_chat: Incomplete | None = None, can_manage_video_chats: Incomplete | None = None, until_date: Incomplete | None = None, can_manage_topics: Incomplete | None = None, can_post_stories: Incomplete | None = None, can_edit_stories: Incomplete | None = None, can_delete_stories: Incomplete | None = None, **kwargs) -> None: ...
    @property
    def can_manage_voice_chats(self): ...

class ChatMemberOwner(ChatMember): ...
class ChatMemberAdministrator(ChatMember): ...
class ChatMemberMember(ChatMember): ...
class ChatMemberRestricted(ChatMember): ...
class ChatMemberLeft(ChatMember): ...
class ChatMemberBanned(ChatMember): ...

class ChatPermissions(JsonDeserializable, JsonSerializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string): ...
    can_send_messages: Incomplete
    can_send_polls: Incomplete
    can_send_other_messages: Incomplete
    can_add_web_page_previews: Incomplete
    can_change_info: Incomplete
    can_invite_users: Incomplete
    can_pin_messages: Incomplete
    can_manage_topics: Incomplete
    can_send_audios: Incomplete
    can_send_documents: Incomplete
    can_send_photos: Incomplete
    can_send_videos: Incomplete
    can_send_video_notes: Incomplete
    can_send_voice_notes: Incomplete
    def __init__(self, can_send_messages: Incomplete | None = None, can_send_media_messages: Incomplete | None = None, can_send_audios: Incomplete | None = None, can_send_documents: Incomplete | None = None, can_send_photos: Incomplete | None = None, can_send_videos: Incomplete | None = None, can_send_video_notes: Incomplete | None = None, can_send_voice_notes: Incomplete | None = None, can_send_polls: Incomplete | None = None, can_send_other_messages: Incomplete | None = None, can_add_web_page_previews: Incomplete | None = None, can_change_info: Incomplete | None = None, can_invite_users: Incomplete | None = None, can_pin_messages: Incomplete | None = None, can_manage_topics: Incomplete | None = None, **kwargs) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class BotCommand(JsonSerializable, JsonDeserializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string): ...
    command: Incomplete
    description: Incomplete
    def __init__(self, command, description, **kwargs) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class BotCommandScope(ABC, JsonSerializable):
    type: Incomplete
    chat_id: Incomplete
    user_id: Incomplete
    def __init__(self, type: str = 'default', chat_id: Incomplete | None = None, user_id: Incomplete | None = None) -> None: ...
    def to_json(self): ...

class BotCommandScopeDefault(BotCommandScope):
    def __init__(self) -> None: ...

class BotCommandScopeAllPrivateChats(BotCommandScope):
    def __init__(self) -> None: ...

class BotCommandScopeAllGroupChats(BotCommandScope):
    def __init__(self) -> None: ...

class BotCommandScopeAllChatAdministrators(BotCommandScope):
    def __init__(self) -> None: ...

class BotCommandScopeChat(BotCommandScope):
    def __init__(self, chat_id: Incomplete | None = None) -> None: ...

class BotCommandScopeChatAdministrators(BotCommandScope):
    def __init__(self, chat_id: Incomplete | None = None) -> None: ...

class BotCommandScopeChatMember(BotCommandScope):
    def __init__(self, chat_id: Incomplete | None = None, user_id: Incomplete | None = None) -> None: ...

class InlineQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    id: Incomplete
    from_user: Incomplete
    query: Incomplete
    offset: Incomplete
    chat_type: Incomplete
    location: Incomplete
    def __init__(self, id, from_user, query, offset, chat_type: Incomplete | None = None, location: Incomplete | None = None, **kwargs) -> None: ...

class InputTextMessageContent(Dictionaryable):
    message_text: Incomplete
    parse_mode: Incomplete
    entities: Incomplete
    link_preview_options: Incomplete
    def __init__(self, message_text, parse_mode: Incomplete | None = None, entities: Incomplete | None = None, disable_web_page_preview: Incomplete | None = None, link_preview_options: Incomplete | None = None) -> None: ...
    def to_dict(self): ...

class InputLocationMessageContent(Dictionaryable):
    latitude: Incomplete
    longitude: Incomplete
    horizontal_accuracy: Incomplete
    live_period: Incomplete
    heading: Incomplete
    proximity_alert_radius: Incomplete
    def __init__(self, latitude, longitude, horizontal_accuracy: Incomplete | None = None, live_period: Incomplete | None = None, heading: Incomplete | None = None, proximity_alert_radius: Incomplete | None = None) -> None: ...
    def to_dict(self): ...

class InputVenueMessageContent(Dictionaryable):
    latitude: Incomplete
    longitude: Incomplete
    title: Incomplete
    address: Incomplete
    foursquare_id: Incomplete
    foursquare_type: Incomplete
    google_place_id: Incomplete
    google_place_type: Incomplete
    def __init__(self, latitude, longitude, title, address, foursquare_id: Incomplete | None = None, foursquare_type: Incomplete | None = None, google_place_id: Incomplete | None = None, google_place_type: Incomplete | None = None) -> None: ...
    def to_dict(self): ...

class InputContactMessageContent(Dictionaryable):
    phone_number: Incomplete
    first_name: Incomplete
    last_name: Incomplete
    vcard: Incomplete
    def __init__(self, phone_number, first_name, last_name: Incomplete | None = None, vcard: Incomplete | None = None) -> None: ...
    def to_dict(self): ...

class InputInvoiceMessageContent(Dictionaryable):
    title: Incomplete
    description: Incomplete
    payload: Incomplete
    provider_token: Incomplete
    currency: Incomplete
    prices: Incomplete
    max_tip_amount: Incomplete
    suggested_tip_amounts: Incomplete
    provider_data: Incomplete
    photo_url: Incomplete
    photo_size: Incomplete
    photo_width: Incomplete
    photo_height: Incomplete
    need_name: Incomplete
    need_phone_number: Incomplete
    need_email: Incomplete
    need_shipping_address: Incomplete
    send_phone_number_to_provider: Incomplete
    send_email_to_provider: Incomplete
    is_flexible: Incomplete
    def __init__(self, title, description, payload, provider_token, currency, prices, max_tip_amount: Incomplete | None = None, suggested_tip_amounts: Incomplete | None = None, provider_data: Incomplete | None = None, photo_url: Incomplete | None = None, photo_size: Incomplete | None = None, photo_width: Incomplete | None = None, photo_height: Incomplete | None = None, need_name: Incomplete | None = None, need_phone_number: Incomplete | None = None, need_email: Incomplete | None = None, need_shipping_address: Incomplete | None = None, send_phone_number_to_provider: Incomplete | None = None, send_email_to_provider: Incomplete | None = None, is_flexible: Incomplete | None = None) -> None: ...
    def to_dict(self): ...

class ChosenInlineResult(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    result_id: Incomplete
    from_user: Incomplete
    location: Incomplete
    inline_message_id: Incomplete
    query: Incomplete
    def __init__(self, result_id, from_user, query, location: Incomplete | None = None, inline_message_id: Incomplete | None = None, **kwargs) -> None: ...

class InlineQueryResultBase(ABC, Dictionaryable, JsonSerializable):
    type: Incomplete
    id: Incomplete
    title: Incomplete
    caption: Incomplete
    input_message_content: Incomplete
    reply_markup: Incomplete
    caption_entities: Incomplete
    parse_mode: Incomplete
    def __init__(self, type, id, title: Incomplete | None = None, caption: Incomplete | None = None, input_message_content: Incomplete | None = None, reply_markup: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class SentWebAppMessage(JsonDeserializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string): ...
    inline_message_id: Incomplete
    def __init__(self, inline_message_id: Incomplete | None = None, **kwargs) -> None: ...
    def to_dict(self): ...

class InlineQueryResultArticle(InlineQueryResultBase):
    url: Incomplete
    hide_url: Incomplete
    description: Incomplete
    thumbnail_url: Incomplete
    thumbnail_width: Incomplete
    thumbnail_height: Incomplete
    def __init__(self, id, title, input_message_content, reply_markup: Incomplete | None = None, url: Incomplete | None = None, hide_url: Incomplete | None = None, description: Incomplete | None = None, thumbnail_url: Incomplete | None = None, thumbnail_width: Incomplete | None = None, thumbnail_height: Incomplete | None = None) -> None: ...
    @property
    def thumb_url(self): ...
    @property
    def thumb_width(self): ...
    @property
    def thumb_height(self): ...
    def to_dict(self): ...

class InlineQueryResultPhoto(InlineQueryResultBase):
    photo_url: Incomplete
    thumbnail_url: Incomplete
    photo_width: Incomplete
    photo_height: Incomplete
    description: Incomplete
    show_caption_above_media: Incomplete
    def __init__(self, id, photo_url, thumbnail_url, photo_width: Incomplete | None = None, photo_height: Incomplete | None = None, title: Incomplete | None = None, description: Incomplete | None = None, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None, show_caption_above_media: Incomplete | None = None) -> None: ...
    @property
    def thumb_url(self): ...
    def to_dict(self): ...

class InlineQueryResultGif(InlineQueryResultBase):
    gif_url: Incomplete
    gif_width: Incomplete
    gif_height: Incomplete
    thumbnail_url: Incomplete
    gif_duration: Incomplete
    thumbnail_mime_type: Incomplete
    show_caption_above_media: Incomplete
    def __init__(self, id, gif_url, thumbnail_url, gif_width: Incomplete | None = None, gif_height: Incomplete | None = None, title: Incomplete | None = None, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None, gif_duration: Incomplete | None = None, parse_mode: Incomplete | None = None, thumbnail_mime_type: Incomplete | None = None, show_caption_above_media: Incomplete | None = None) -> None: ...
    @property
    def thumb_url(self): ...
    @property
    def thumb_mime_type(self): ...
    def to_dict(self): ...

class InlineQueryResultMpeg4Gif(InlineQueryResultBase):
    mpeg4_url: Incomplete
    mpeg4_width: Incomplete
    mpeg4_height: Incomplete
    thumbnail_url: Incomplete
    mpeg4_duration: Incomplete
    thumbnail_mime_type: Incomplete
    show_caption_above_media: Incomplete
    def __init__(self, id, mpeg4_url, thumbnail_url, mpeg4_width: Incomplete | None = None, mpeg4_height: Incomplete | None = None, title: Incomplete | None = None, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None, mpeg4_duration: Incomplete | None = None, thumbnail_mime_type: Incomplete | None = None, show_caption_above_media: Incomplete | None = None) -> None: ...
    @property
    def thumb_url(self): ...
    @property
    def thumb_mime_type(self): ...
    def to_dict(self): ...

class InlineQueryResultVideo(InlineQueryResultBase):
    video_url: Incomplete
    mime_type: Incomplete
    thumbnail_url: Incomplete
    video_width: Incomplete
    video_height: Incomplete
    video_duration: Incomplete
    description: Incomplete
    show_caption_above_media: Incomplete
    def __init__(self, id, video_url, mime_type, thumbnail_url, title, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, video_width: Incomplete | None = None, video_height: Incomplete | None = None, video_duration: Incomplete | None = None, description: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None, show_caption_above_media: Incomplete | None = None) -> None: ...
    @property
    def thumb_url(self): ...
    def to_dict(self): ...

class InlineQueryResultAudio(InlineQueryResultBase):
    audio_url: Incomplete
    performer: Incomplete
    audio_duration: Incomplete
    def __init__(self, id, audio_url, title, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, performer: Incomplete | None = None, audio_duration: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None) -> None: ...
    def to_dict(self): ...

class InlineQueryResultVoice(InlineQueryResultBase):
    voice_url: Incomplete
    voice_duration: Incomplete
    def __init__(self, id, voice_url, title, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, voice_duration: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None) -> None: ...
    def to_dict(self): ...

class InlineQueryResultDocument(InlineQueryResultBase):
    document_url: Incomplete
    mime_type: Incomplete
    description: Incomplete
    thumbnail_url: Incomplete
    thumbnail_width: Incomplete
    thumbnail_height: Incomplete
    def __init__(self, id, title, document_url, mime_type, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, description: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None, thumbnail_url: Incomplete | None = None, thumbnail_width: Incomplete | None = None, thumbnail_height: Incomplete | None = None) -> None: ...
    @property
    def thumb_url(self): ...
    @property
    def thumb_width(self): ...
    @property
    def thumb_height(self): ...
    def to_dict(self): ...

class InlineQueryResultLocation(InlineQueryResultBase):
    latitude: Incomplete
    longitude: Incomplete
    horizontal_accuracy: Incomplete
    live_period: Incomplete
    heading: Incomplete
    proximity_alert_radius: Incomplete
    thumbnail_url: Incomplete
    thumbnail_width: Incomplete
    thumbnail_height: Incomplete
    def __init__(self, id, title, latitude, longitude, horizontal_accuracy, live_period: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None, thumbnail_url: Incomplete | None = None, thumbnail_width: Incomplete | None = None, thumbnail_height: Incomplete | None = None, heading: Incomplete | None = None, proximity_alert_radius: Incomplete | None = None) -> None: ...
    @property
    def thumb_url(self): ...
    @property
    def thumb_width(self): ...
    @property
    def thumb_height(self): ...
    def to_dict(self): ...

class InlineQueryResultVenue(InlineQueryResultBase):
    latitude: Incomplete
    longitude: Incomplete
    address: Incomplete
    foursquare_id: Incomplete
    foursquare_type: Incomplete
    google_place_id: Incomplete
    google_place_type: Incomplete
    thumbnail_url: Incomplete
    thumbnail_width: Incomplete
    thumbnail_height: Incomplete
    def __init__(self, id, title, latitude, longitude, address, foursquare_id: Incomplete | None = None, foursquare_type: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None, thumbnail_url: Incomplete | None = None, thumbnail_width: Incomplete | None = None, thumbnail_height: Incomplete | None = None, google_place_id: Incomplete | None = None, google_place_type: Incomplete | None = None) -> None: ...
    @property
    def thumb_url(self): ...
    @property
    def thumb_width(self): ...
    @property
    def thumb_height(self): ...
    def to_dict(self): ...

class InlineQueryResultContact(InlineQueryResultBase):
    phone_number: Incomplete
    first_name: Incomplete
    last_name: Incomplete
    vcard: Incomplete
    thumbnail_url: Incomplete
    thumbnail_width: Incomplete
    thumbnail_height: Incomplete
    def __init__(self, id, phone_number, first_name, last_name: Incomplete | None = None, vcard: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None, thumbnail_url: Incomplete | None = None, thumbnail_width: Incomplete | None = None, thumbnail_height: Incomplete | None = None) -> None: ...
    @property
    def thumb_url(self): ...
    @property
    def thumb_width(self): ...
    @property
    def thumb_height(self): ...
    def to_dict(self): ...

class InlineQueryResultGame(InlineQueryResultBase):
    game_short_name: Incomplete
    def __init__(self, id, game_short_name, reply_markup: Incomplete | None = None) -> None: ...
    def to_dict(self): ...

class InlineQueryResultCachedBase(ABC, JsonSerializable):
    type: Incomplete
    id: Incomplete
    title: Incomplete
    description: Incomplete
    caption: Incomplete
    reply_markup: Incomplete
    input_message_content: Incomplete
    parse_mode: Incomplete
    caption_entities: Incomplete
    payload_dic: Incomplete
    show_caption_above_media: Incomplete
    def __init__(self) -> None: ...
    def to_json(self): ...

class InlineQueryResultCachedPhoto(InlineQueryResultCachedBase):
    type: str
    id: Incomplete
    photo_file_id: Incomplete
    title: Incomplete
    description: Incomplete
    caption: Incomplete
    caption_entities: Incomplete
    reply_markup: Incomplete
    input_message_content: Incomplete
    parse_mode: Incomplete
    show_caption_above_media: Incomplete
    def __init__(self, id, photo_file_id, title: Incomplete | None = None, description: Incomplete | None = None, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None, show_caption_above_media: Incomplete | None = None) -> None: ...

class InlineQueryResultCachedGif(InlineQueryResultCachedBase):
    type: str
    id: Incomplete
    gif_file_id: Incomplete
    title: Incomplete
    description: Incomplete
    caption: Incomplete
    caption_entities: Incomplete
    reply_markup: Incomplete
    input_message_content: Incomplete
    parse_mode: Incomplete
    show_caption_above_media: Incomplete
    def __init__(self, id, gif_file_id, title: Incomplete | None = None, description: Incomplete | None = None, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None, show_caption_above_media: Incomplete | None = None) -> None: ...

class InlineQueryResultCachedMpeg4Gif(InlineQueryResultCachedBase):
    type: str
    id: Incomplete
    mpeg4_file_id: Incomplete
    title: Incomplete
    description: Incomplete
    caption: Incomplete
    caption_entities: Incomplete
    reply_markup: Incomplete
    input_message_content: Incomplete
    parse_mode: Incomplete
    show_caption_above_media: Incomplete
    def __init__(self, id, mpeg4_file_id, title: Incomplete | None = None, description: Incomplete | None = None, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None, show_caption_above_media: Incomplete | None = None) -> None: ...

class InlineQueryResultCachedSticker(InlineQueryResultCachedBase):
    type: str
    id: Incomplete
    sticker_file_id: Incomplete
    reply_markup: Incomplete
    input_message_content: Incomplete
    def __init__(self, id, sticker_file_id, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None) -> None: ...

class InlineQueryResultCachedDocument(InlineQueryResultCachedBase):
    type: str
    id: Incomplete
    document_file_id: Incomplete
    title: Incomplete
    description: Incomplete
    caption: Incomplete
    caption_entities: Incomplete
    reply_markup: Incomplete
    input_message_content: Incomplete
    parse_mode: Incomplete
    def __init__(self, id, document_file_id, title, description: Incomplete | None = None, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None) -> None: ...

class InlineQueryResultCachedVideo(InlineQueryResultCachedBase):
    type: str
    id: Incomplete
    video_file_id: Incomplete
    title: Incomplete
    description: Incomplete
    caption: Incomplete
    caption_entities: Incomplete
    reply_markup: Incomplete
    input_message_content: Incomplete
    parse_mode: Incomplete
    show_caption_above_media: Incomplete
    def __init__(self, id, video_file_id, title, description: Incomplete | None = None, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None, show_caption_above_media: Incomplete | None = None) -> None: ...

class InlineQueryResultCachedVoice(InlineQueryResultCachedBase):
    type: str
    id: Incomplete
    voice_file_id: Incomplete
    title: Incomplete
    caption: Incomplete
    caption_entities: Incomplete
    reply_markup: Incomplete
    input_message_content: Incomplete
    parse_mode: Incomplete
    def __init__(self, id, voice_file_id, title, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None) -> None: ...

class InlineQueryResultCachedAudio(InlineQueryResultCachedBase):
    type: str
    id: Incomplete
    audio_file_id: Incomplete
    caption: Incomplete
    caption_entities: Incomplete
    reply_markup: Incomplete
    input_message_content: Incomplete
    parse_mode: Incomplete
    def __init__(self, id, audio_file_id, caption: Incomplete | None = None, caption_entities: Incomplete | None = None, parse_mode: Incomplete | None = None, reply_markup: Incomplete | None = None, input_message_content: Incomplete | None = None) -> None: ...

class Game(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    @classmethod
    def parse_photo(cls, photo_size_array): ...
    @classmethod
    def parse_entities(cls, message_entity_array): ...
    title: Incomplete
    description: Incomplete
    photo: Incomplete
    text: Incomplete
    text_entities: Incomplete
    animation: Incomplete
    def __init__(self, title, description, photo, text: Incomplete | None = None, text_entities: Incomplete | None = None, animation: Incomplete | None = None, **kwargs) -> None: ...

class Animation(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    file_id: Incomplete
    file_unique_id: Incomplete
    width: Incomplete
    height: Incomplete
    duration: Incomplete
    thumbnail: Incomplete
    file_name: Incomplete
    mime_type: Incomplete
    file_size: Incomplete
    def __init__(self, file_id, file_unique_id, width: Incomplete | None = None, height: Incomplete | None = None, duration: Incomplete | None = None, thumbnail: Incomplete | None = None, file_name: Incomplete | None = None, mime_type: Incomplete | None = None, file_size: Incomplete | None = None, **kwargs) -> None: ...
    @property
    def thumb(self): ...

class GameHighScore(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    position: Incomplete
    user: Incomplete
    score: Incomplete
    def __init__(self, position, user, score, **kwargs) -> None: ...

class LabeledPrice(JsonSerializable, Dictionaryable):
    label: Incomplete
    amount: Incomplete
    def __init__(self, label, amount) -> None: ...
    def to_dict(self): ...
    def to_json(self): ...

class Invoice(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    title: Incomplete
    description: Incomplete
    start_parameter: Incomplete
    currency: Incomplete
    total_amount: Incomplete
    def __init__(self, title, description, start_parameter, currency, total_amount, **kwargs) -> None: ...

class ShippingAddress(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    country_code: Incomplete
    state: Incomplete
    city: Incomplete
    street_line1: Incomplete
    street_line2: Incomplete
    post_code: Incomplete
    def __init__(self, country_code, state, city, street_line1, street_line2, post_code, **kwargs) -> None: ...

class OrderInfo(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    name: Incomplete
    phone_number: Incomplete
    email: Incomplete
    shipping_address: Incomplete
    def __init__(self, name: Incomplete | None = None, phone_number: Incomplete | None = None, email: Incomplete | None = None, shipping_address: Incomplete | None = None, **kwargs) -> None: ...

class ShippingOption(JsonSerializable):
    id: Incomplete
    title: Incomplete
    prices: Incomplete
    def __init__(self, id, title) -> None: ...
    def add_price(self, *args): ...
    def to_json(self): ...

class SuccessfulPayment(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    currency: Incomplete
    total_amount: Incomplete
    invoice_payload: Incomplete
    shipping_option_id: Incomplete
    order_info: Incomplete
    telegram_payment_charge_id: Incomplete
    provider_payment_charge_id: Incomplete
    def __init__(self, currency, total_amount, invoice_payload, shipping_option_id: Incomplete | None = None, order_info: Incomplete | None = None, telegram_payment_charge_id: Incomplete | None = None, provider_payment_charge_id: Incomplete | None = None, **kwargs) -> None: ...

class ShippingQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    id: Incomplete
    from_user: Incomplete
    invoice_payload: Incomplete
    shipping_address: Incomplete
    def __init__(self, id, from_user, invoice_payload, shipping_address, **kwargs) -> None: ...

class PreCheckoutQuery(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    id: Incomplete
    from_user: Incomplete
    currency: Incomplete
    total_amount: Incomplete
    invoice_payload: Incomplete
    shipping_option_id: Incomplete
    order_info: Incomplete
    def __init__(self, id, from_user, currency, total_amount, invoice_payload, shipping_option_id: Incomplete | None = None, order_info: Incomplete | None = None, **kwargs) -> None: ...

class StickerSet(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    name: Incomplete
    title: Incomplete
    sticker_type: Incomplete
    stickers: Incomplete
    thumbnail: Incomplete
    def __init__(self, name, title, sticker_type, stickers, thumbnail: Incomplete | None = None, **kwargs) -> None: ...
    @property
    def thumb(self): ...
    @property
    def contains_masks(self): ...
    @property
    def is_animated(self): ...
    @property
    def is_video(self): ...

class Sticker(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    file_id: Incomplete
    file_unique_id: Incomplete
    type: Incomplete
    width: Incomplete
    height: Incomplete
    is_animated: Incomplete
    is_video: Incomplete
    thumbnail: Incomplete
    emoji: Incomplete
    set_name: Incomplete
    mask_position: Incomplete
    file_size: Incomplete
    premium_animation: Incomplete
    custom_emoji_id: Incomplete
    needs_repainting: Incomplete
    def __init__(self, file_id, file_unique_id, type, width, height, is_animated, is_video, thumbnail: Incomplete | None = None, emoji: Incomplete | None = None, set_name: Incomplete | None = None, mask_position: Incomplete | None = None, file_size: Incomplete | None = None, premium_animation: Incomplete | None = None, custom_emoji_id: Incomplete | None = None, needs_repainting: Incomplete | None = None, **kwargs) -> None: ...
    @property
    def thumb(self): ...

class MaskPosition(Dictionaryable, JsonDeserializable, JsonSerializable):
    @classmethod
    def de_json(cls, json_string): ...
    point: Incomplete
    x_shift: Incomplete
    y_shift: Incomplete
    scale: Incomplete
    def __init__(self, point, x_shift, y_shift, scale, **kwargs) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class InputMedia(Dictionaryable, JsonSerializable):
    type: Incomplete
    media: Incomplete
    caption: Incomplete
    parse_mode: Incomplete
    caption_entities: Incomplete
    def __init__(self, type, media, caption: Incomplete | None = None, parse_mode: Incomplete | None = None, caption_entities: Incomplete | None = None) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...
    def convert_input_media(self): ...

class InputMediaPhoto(InputMedia):
    has_spoiler: Incomplete
    show_caption_above_media: Incomplete
    def __init__(self, media, caption: Incomplete | None = None, parse_mode: Incomplete | None = None, caption_entities: Incomplete | None = None, has_spoiler: Incomplete | None = None, show_caption_above_media: Incomplete | None = None) -> None: ...
    def to_dict(self): ...

class InputMediaVideo(InputMedia):
    thumbnail: Incomplete
    width: Incomplete
    height: Incomplete
    duration: Incomplete
    supports_streaming: Incomplete
    has_spoiler: Incomplete
    show_caption_above_media: Incomplete
    def __init__(self, media, thumbnail: Incomplete | None = None, caption: Incomplete | None = None, parse_mode: Incomplete | None = None, caption_entities: Incomplete | None = None, width: Incomplete | None = None, height: Incomplete | None = None, duration: Incomplete | None = None, supports_streaming: Incomplete | None = None, has_spoiler: Incomplete | None = None, show_caption_above_media: Incomplete | None = None) -> None: ...
    @property
    def thumb(self): ...
    def to_dict(self): ...

class InputMediaAnimation(InputMedia):
    thumbnail: Incomplete
    width: Incomplete
    height: Incomplete
    duration: Incomplete
    has_spoiler: Incomplete
    show_caption_above_media: Incomplete
    def __init__(self, media, thumbnail: Incomplete | None = None, caption: Incomplete | None = None, parse_mode: Incomplete | None = None, caption_entities: Incomplete | None = None, width: Incomplete | None = None, height: Incomplete | None = None, duration: Incomplete | None = None, has_spoiler: Incomplete | None = None, show_caption_above_media: Incomplete | None = None) -> None: ...
    @property
    def thumb(self): ...
    def to_dict(self): ...

class InputMediaAudio(InputMedia):
    thumbnail: Incomplete
    duration: Incomplete
    performer: Incomplete
    title: Incomplete
    def __init__(self, media, thumbnail: Incomplete | None = None, caption: Incomplete | None = None, parse_mode: Incomplete | None = None, caption_entities: Incomplete | None = None, duration: Incomplete | None = None, performer: Incomplete | None = None, title: Incomplete | None = None) -> None: ...
    @property
    def thumb(self): ...
    def to_dict(self): ...

class InputMediaDocument(InputMedia):
    thumbnail: Incomplete
    disable_content_type_detection: Incomplete
    def __init__(self, media, thumbnail: Incomplete | None = None, caption: Incomplete | None = None, parse_mode: Incomplete | None = None, caption_entities: Incomplete | None = None, disable_content_type_detection: Incomplete | None = None) -> None: ...
    @property
    def thumb(self): ...
    def to_dict(self): ...

class PollOption(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    text: Incomplete
    voter_count: Incomplete
    text_entities: Incomplete
    def __init__(self, text, voter_count: int = 0, text_entities: Incomplete | None = None, **kwargs) -> None: ...

class InputPollOption(JsonSerializable):
    text: Incomplete
    text_parse_mode: Incomplete
    text_entities: Incomplete
    def __init__(self, text, text_parse_mode: Incomplete | None = None, text_entities: Incomplete | None = None, **kwargs) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class Poll(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    id: Incomplete
    question: Incomplete
    options: Incomplete
    total_voter_count: Incomplete
    is_closed: Incomplete
    is_anonymous: Incomplete
    type: Incomplete
    allows_multiple_answers: Incomplete
    correct_option_id: Incomplete
    explanation: Incomplete
    explanation_entities: Incomplete
    question_entities: Incomplete
    open_period: Incomplete
    close_date: Incomplete
    def __init__(self, question, options, poll_id: Incomplete | None = None, total_voter_count: Incomplete | None = None, is_closed: Incomplete | None = None, is_anonymous: Incomplete | None = None, type: Incomplete | None = None, allows_multiple_answers: Incomplete | None = None, correct_option_id: Incomplete | None = None, explanation: Incomplete | None = None, explanation_entities: Incomplete | None = None, open_period: Incomplete | None = None, close_date: Incomplete | None = None, poll_type: Incomplete | None = None, question_entities: Incomplete | None = None, **kwargs) -> None: ...
    def add(self, option) -> None: ...

class PollAnswer(JsonSerializable, JsonDeserializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string): ...
    poll_id: Incomplete
    user: Incomplete
    option_ids: Incomplete
    voter_chat: Incomplete
    def __init__(self, poll_id, option_ids, user: Incomplete | None = None, voter_chat: Incomplete | None = None, **kwargs) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class ChatLocation(JsonSerializable, JsonDeserializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string): ...
    location: Incomplete
    address: Incomplete
    def __init__(self, location, address, **kwargs) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class ChatInviteLink(JsonSerializable, JsonDeserializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string): ...
    invite_link: Incomplete
    creator: Incomplete
    creates_join_request: Incomplete
    is_primary: Incomplete
    is_revoked: Incomplete
    name: Incomplete
    expire_date: Incomplete
    member_limit: Incomplete
    pending_join_request_count: Incomplete
    def __init__(self, invite_link, creator, creates_join_request, is_primary, is_revoked, name: Incomplete | None = None, expire_date: Incomplete | None = None, member_limit: Incomplete | None = None, pending_join_request_count: Incomplete | None = None, **kwargs) -> None: ...
    def to_json(self): ...
    def to_dict(self): ...

class ProximityAlertTriggered(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    traveler: Incomplete
    watcher: Incomplete
    distance: Incomplete
    def __init__(self, traveler, watcher, distance, **kwargs) -> None: ...

class VideoChatStarted(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    def __init__(self) -> None: ...

class VoiceChatStarted(VideoChatStarted):
    def __init__(self) -> None: ...

class VideoChatScheduled(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    start_date: Incomplete
    def __init__(self, start_date, **kwargs) -> None: ...

class VoiceChatScheduled(VideoChatScheduled):
    def __init__(self, *args, **kwargs) -> None: ...

class VideoChatEnded(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    duration: Incomplete
    def __init__(self, duration, **kwargs) -> None: ...

class VoiceChatEnded(VideoChatEnded):
    def __init__(self, *args, **kwargs) -> None: ...

class VideoChatParticipantsInvited(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    users: Incomplete
    def __init__(self, users: Incomplete | None = None, **kwargs) -> None: ...

class VoiceChatParticipantsInvited(VideoChatParticipantsInvited):
    def __init__(self, *args, **kwargs) -> None: ...

class MessageAutoDeleteTimerChanged(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    message_auto_delete_time: Incomplete
    def __init__(self, message_auto_delete_time, **kwargs) -> None: ...

class MenuButton(JsonDeserializable, JsonSerializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string): ...
    def to_json(self) -> None: ...
    def to_dict(self) -> None: ...

class MenuButtonCommands(MenuButton):
    type: str
    def __init__(self, type: Incomplete | None = None, **kwargs) -> None: ...
    def to_dict(self): ...
    def to_json(self): ...

class MenuButtonWebApp(MenuButton):
    type: str
    text: Incomplete
    web_app: Incomplete
    def __init__(self, type, text, web_app, **kwargs) -> None: ...
    def to_dict(self): ...
    def to_json(self): ...

class MenuButtonDefault(MenuButton):
    type: str
    def __init__(self, type: Incomplete | None = None, **kwargs) -> None: ...
    def to_dict(self): ...
    def to_json(self): ...

class ChatAdministratorRights(JsonDeserializable, JsonSerializable, Dictionaryable):
    @classmethod
    def de_json(cls, json_string): ...
    is_anonymous: Incomplete
    can_manage_chat: Incomplete
    can_delete_messages: Incomplete
    can_manage_video_chats: Incomplete
    can_restrict_members: Incomplete
    can_promote_members: Incomplete
    can_change_info: Incomplete
    can_invite_users: Incomplete
    can_post_messages: Incomplete
    can_edit_messages: Incomplete
    can_pin_messages: Incomplete
    can_manage_topics: Incomplete
    can_post_stories: Incomplete
    can_edit_stories: Incomplete
    can_delete_stories: Incomplete
    def __init__(self, is_anonymous: bool, can_manage_chat: bool, can_delete_messages: bool, can_manage_video_chats: bool, can_restrict_members: bool, can_promote_members: bool, can_change_info: bool, can_invite_users: bool, can_post_messages: bool|None = None, can_edit_messages: bool|None = None, can_pin_messages: bool|None = None, can_manage_topics: bool|None = None, can_post_stories: bool|None = None, can_edit_stories: bool|None = None, can_delete_stories: bool|None = None, **kwargs,) -> None: ...
    def to_dict(self): ...
    def to_json(self): ...

class InputFile:
    def __init__(self, file) -> None: ...
    @property
    def file(self): ...

class ForumTopicCreated(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    name: Incomplete
    icon_color: Incomplete
    icon_custom_emoji_id: Incomplete
    def __init__(self, name: str, icon_color: int, icon_custom_emoji_id: str | None = None, **kwargs) -> None: ...

class ForumTopicClosed(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    def __init__(self) -> None: ...

class ForumTopicReopened(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    def __init__(self) -> None: ...

class ForumTopicEdited(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    name: Incomplete
    icon_custom_emoji_id: Incomplete
    def __init__(self, name: str | None = None, icon_custom_emoji_id: str | None = None, **kwargs) -> None: ...

class GeneralForumTopicHidden(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    def __init__(self) -> None: ...

class GeneralForumTopicUnhidden(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    def __init__(self) -> None: ...

class ForumTopic(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    message_thread_id: Incomplete
    name: Incomplete
    icon_color: Incomplete
    icon_custom_emoji_id: Incomplete
    def __init__(self, message_thread_id: int, name: str, icon_color: int, icon_custom_emoji_id: str | None = None, **kwargs) -> None: ...

class WriteAccessAllowed(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    web_app_name: Incomplete
    from_request: Incomplete
    from_attachment_menu: Incomplete
    def __init__(self, from_request: bool | None = None, web_app_name: str | None = None, from_attachment_menu: bool | None = None, **kwargs) -> None: ...

class ChatShared(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    request_id: Incomplete
    chat_id: Incomplete
    title: Incomplete
    photo: Incomplete
    username: Incomplete
    def __init__(self, request_id: int, chat_id: int, title: str | None = None, photo: list[PhotoSize] | None = None, username: str | None = None, **kwargs) -> None: ...

class BotDescription(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    description: Incomplete
    def __init__(self, description: str, **kwargs) -> None: ...

class BotShortDescription(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    short_description: Incomplete
    def __init__(self, short_description: str, **kwargs) -> None: ...

class InputSticker(Dictionaryable, JsonSerializable):
    sticker: Incomplete
    emoji_list: Incomplete
    mask_position: Incomplete
    keywords: Incomplete
    format: Incomplete
    def __init__(self, sticker: str | InputFile, emoji_list: list[str], format: str | None = None, mask_position: MaskPosition | None = None, keywords: list[str] | None = None) -> None: ...
    def to_dict(self) -> dict: ...
    def to_json(self) -> str|None: ...
    def convert_input_sticker(self): ...

class SwitchInlineQueryChosenChat(JsonDeserializable, Dictionaryable, JsonSerializable):
    @classmethod
    def de_json(cls, json_string): ...
    query: Incomplete
    allow_user_chats: Incomplete
    allow_bot_chats: Incomplete
    allow_group_chats: Incomplete
    allow_channel_chats: Incomplete
    def __init__(self, query: Incomplete | None = None, allow_user_chats: Incomplete | None = None, allow_bot_chats: Incomplete | None = None, allow_group_chats: Incomplete | None = None, allow_channel_chats: Incomplete | None = None, **kwargs) -> None: ...
    def to_dict(self): ...
    def to_json(self): ...

class BotName(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    name: Incomplete
    def __init__(self, name: str, **kwargs) -> None: ...

class InlineQueryResultsButton(JsonSerializable, Dictionaryable):
    text: Incomplete
    web_app: Incomplete
    start_parameter: Incomplete
    def __init__(self, text: str, web_app: WebAppInfo | None = None, start_parameter: str | None = None) -> None: ...
    def to_dict(self) -> dict: ...
    def to_json(self) -> str: ...

class Story(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    chat: Incomplete
    id: Incomplete
    def __init__(self, chat: Chat, id: int, **kwargs) -> None: ...

class ReactionType(JsonDeserializable, Dictionaryable, JsonSerializable):
    @classmethod
    def de_json(cls, json_string): ...
    type: Incomplete
    def __init__(self, type: str) -> None: ...
    def to_dict(self) -> dict: ...
    def to_json(self) -> str: ...

class ReactionTypeEmoji(ReactionType):
    emoji: Incomplete
    def __init__(self, emoji: str, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...

class ReactionTypeCustomEmoji(ReactionType):
    custom_emoji_id: Incomplete
    def __init__(self, custom_emoji_id: str, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...

class MessageReactionUpdated(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    chat: Incomplete
    message_id: Incomplete
    user: Incomplete
    actor_chat: Incomplete
    date: Incomplete
    old_reaction: Incomplete
    new_reaction: Incomplete
    def __init__(self, chat: Chat, message_id: int, date: int, old_reaction: list[ReactionType], new_reaction: list[ReactionType], user: User | None = None, actor_chat: Chat | None = None, **kwargs) -> None: ...

class MessageReactionCountUpdated(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    chat: Incomplete
    message_id: Incomplete
    date: Incomplete
    reactions: Incomplete
    def __init__(self, chat: Chat, message_id: int, date: int, reactions: list[ReactionCount], **kwargs) -> None: ...

class ReactionCount(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    type: Incomplete
    total_count: Incomplete
    def __init__(self, type: ReactionType, total_count: int, **kwargs) -> None: ...

class ExternalReplyInfo(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    origin: Incomplete
    chat: Incomplete
    message_id: Incomplete
    link_preview_options: Incomplete
    animation: Incomplete
    audio: Incomplete
    document: Incomplete
    photo: Incomplete
    sticker: Incomplete
    story: Incomplete
    video: Incomplete
    video_note: Incomplete
    voice: Incomplete
    has_media_spoiler: Incomplete
    contact: Incomplete
    dice: Incomplete
    game: Incomplete
    giveaway: Incomplete
    giveaway_winners: Incomplete
    invoice: Incomplete
    location: Incomplete
    poll: Incomplete
    venue: Incomplete
    def __init__(self, origin: MessageOrigin, chat: Chat | None = None, message_id: int | None = None, link_preview_options: LinkPreviewOptions | None = None, animation: Animation | None = None, audio: Audio | None = None, document: Document | None = None, photo: list[PhotoSize] | None = None, sticker: Sticker | None = None, story: Story | None = None, video: Video | None = None, video_note: VideoNote | None = None, voice: Voice | None = None, has_media_spoiler: bool | None = None, contact: Contact | None = None, dice: Dice | None = None, game: Game | None = None, giveaway: Giveaway | None = None, giveaway_winners: GiveawayWinners | None = None, invoice: Invoice | None = None, location: Location | None = None, poll: Poll | None = None, venue: Venue | None = None, **kwargs) -> None: ...

class MessageOrigin(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    type: Incomplete
    date: Incomplete
    def __init__(self, type: str, date: int) -> None: ...

class MessageOriginUser(MessageOrigin):
    sender_user: Incomplete
    def __init__(self, date: int, sender_user: User) -> None: ...

class MessageOriginHiddenUser(MessageOrigin):
    sender_user_name: Incomplete
    def __init__(self, date: int, sender_user_name: str) -> None: ...

class MessageOriginChat(MessageOrigin):
    sender_chat: Incomplete
    author_signature: Incomplete
    def __init__(self, date: int, sender_chat: Chat, author_signature: str | None = None) -> None: ...

class MessageOriginChannel(MessageOrigin):
    chat: Incomplete
    message_id: Incomplete
    author_signature: Incomplete
    def __init__(self, date: int, chat: Chat, message_id: int, author_signature: str | None = None) -> None: ...

class LinkPreviewOptions(JsonDeserializable, Dictionaryable, JsonSerializable):
    @classmethod
    def de_json(cls, json_string): ...
    is_disabled: Incomplete
    url: Incomplete
    prefer_small_media: Incomplete
    prefer_large_media: Incomplete
    show_above_text: Incomplete
    def __init__(self, is_disabled: bool | None = None, url: str | None = None, prefer_small_media: bool | None = None, prefer_large_media: bool | None = None, show_above_text: bool | None = None, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    def to_json(self) -> str: ...

class Giveaway(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    chats: Incomplete
    winners_selection_date: Incomplete
    winner_count: Incomplete
    only_new_members: Incomplete
    has_public_winners: Incomplete
    prize_description: Incomplete
    country_codes: Incomplete
    premium_subscription_month_count: Incomplete
    def __init__(self, chats: list[Chat], winners_selection_date: int, winner_count: int, only_new_members: bool | None = None, has_public_winners: bool | None = None, prize_description: str | None = None, country_codes: list[str] | None = None, premium_subscription_month_count: int | None = None, **kwargs) -> None: ...

class GiveawayWinners(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    chat: Incomplete
    giveaway_message_id: Incomplete
    winners_selection_date: Incomplete
    winner_count: Incomplete
    winners: Incomplete
    additional_chat_count: Incomplete
    premium_subscription_month_count: Incomplete
    unclaimed_prize_count: Incomplete
    only_new_members: Incomplete
    was_refunded: Incomplete
    prize_description: Incomplete
    def __init__(self, chat: Chat, giveaway_message_id: int, winners_selection_date: int, winner_count: int, winners: list[User], additional_chat_count: int | None = None, premium_subscription_month_count: int | None = None, unclaimed_prize_count: int | None = None, only_new_members: bool | None = None, was_refunded: bool | None = None, prize_description: str | None = None, **kwargs) -> None: ...

class GiveawayCompleted(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    winner_count: Incomplete
    unclaimed_prize_count: Incomplete
    giveaway_message: Incomplete
    def __init__(self, winner_count: int, unclaimed_prize_count: int | None = None, giveaway_message: Message | None = None, **kwargs) -> None: ...

class GiveawayCreated(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    def __init__(self, **kwargs) -> None: ...

class TextQuote(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    text: Incomplete
    entities: Incomplete
    position: Incomplete
    is_manual: Incomplete
    def __init__(self, text: str, position: int, entities: list[MessageEntity] | None = None, is_manual: bool | None = None, **kwargs) -> None: ...
    @property
    def html_text(self): ...

class ReplyParameters(JsonDeserializable, Dictionaryable, JsonSerializable):
    @classmethod
    def de_json(cls, json_string): ...
    message_id: Incomplete
    chat_id: Incomplete
    allow_sending_without_reply: Incomplete
    quote: Incomplete
    quote_parse_mode: Incomplete
    quote_entities: Incomplete
    quote_position: Incomplete
    def __init__(self, message_id: int, chat_id: int | str | None = None, allow_sending_without_reply: bool | None = None, quote: str | None = None, quote_parse_mode: str | None = None, quote_entities: list[MessageEntity] | None = None, quote_position: int | None = None, **kwargs) -> None: ...
    def to_dict(self) -> dict: ...
    def to_json(self) -> str: ...

class UsersShared(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    request_id: Incomplete
    users: Incomplete
    def __init__(self, request_id, users: list[SharedUser], **kwargs) -> None: ...
    @property
    def user_id(self) -> None: ...
    @property
    def user_ids(self): ...

class ChatBoostUpdated(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    chat: Incomplete
    boost: Incomplete
    def __init__(self, chat, boost, **kwargs) -> None: ...

class ChatBoostRemoved(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    chat: Incomplete
    boost_id: Incomplete
    remove_date: Incomplete
    source: Incomplete
    def __init__(self, chat, boost_id, remove_date, source, **kwargs) -> None: ...

class ChatBoostSource(ABC, JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...

class ChatBoostSourcePremium(ChatBoostSource):
    @classmethod
    def de_json(cls, json_string): ...
    source: Incomplete
    user: Incomplete
    def __init__(self, source, user, **kwargs) -> None: ...

class ChatBoostSourceGiftCode(ChatBoostSource):
    @classmethod
    def de_json(cls, json_string): ...
    source: Incomplete
    user: Incomplete
    def __init__(self, source, user, **kwargs) -> None: ...

class ChatBoostSourceGiveaway(ChatBoostSource):
    @classmethod
    def de_json(cls, json_string): ...
    source: Incomplete
    giveaway_message_id: Incomplete
    user: Incomplete
    is_unclaimed: Incomplete
    def __init__(self, source, giveaway_message_id, user: Incomplete | None = None, is_unclaimed: Incomplete | None = None, **kwargs) -> None: ...

class ChatBoost(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    boost_id: Incomplete
    add_date: Incomplete
    expiration_date: Incomplete
    source: Incomplete
    def __init__(self, boost_id, add_date, expiration_date, source, **kwargs) -> None: ...

class UserChatBoosts(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    boosts: Incomplete
    def __init__(self, boosts, **kwargs) -> None: ...

class InaccessibleMessage(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    chat: Incomplete
    message_id: Incomplete
    date: Incomplete
    def __init__(self, chat, message_id, date, **kwargs) -> None: ...
    def __getattr__(self, item): ...

class ChatBoostAdded(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    boost_count: Incomplete
    def __init__(self, boost_count, **kwargs) -> None: ...

class BusinessConnection(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    id: Incomplete
    user: Incomplete
    user_chat_id: Incomplete
    date: Incomplete
    can_reply: Incomplete
    is_enabled: Incomplete
    def __init__(self, id, user, user_chat_id, date, can_reply, is_enabled, **kwargs) -> None: ...

class BusinessMessagesDeleted(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    business_connection_id: Incomplete
    chat: Incomplete
    message_ids: Incomplete
    def __init__(self, business_connection_id, chat, message_ids, **kwargs) -> None: ...

class BusinessIntro(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    title: Incomplete
    message: Incomplete
    sticker: Incomplete
    def __init__(self, title: Incomplete | None = None, message: Incomplete | None = None, sticker: Incomplete | None = None, **kwargs) -> None: ...

class BusinessLocation(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    address: Incomplete
    location: Incomplete
    def __init__(self, address, location: Incomplete | None = None, **kwargs) -> None: ...

class BusinessOpeningHoursInterval(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    opening_minute: Incomplete
    closing_minute: Incomplete
    def __init__(self, opening_minute, closing_minute, **kwargs) -> None: ...

class BusinessOpeningHours(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    time_zone_name: Incomplete
    opening_hours: Incomplete
    def __init__(self, time_zone_name, opening_hours, **kwargs) -> None: ...

class SharedUser(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    user_id: Incomplete
    first_name: Incomplete
    last_name: Incomplete
    username: Incomplete
    photo: Incomplete
    def __init__(self, user_id, first_name: Incomplete | None = None, last_name: Incomplete | None = None, username: Incomplete | None = None, photo: Incomplete | None = None, **kwargs) -> None: ...

class Birthdate(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    day: Incomplete
    month: Incomplete
    year: Incomplete
    def __init__(self, day, month, year: Incomplete | None = None, **kwargs) -> None: ...

class BackgroundFill(ABC, JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...

class BackgroundFillSolid(BackgroundFill):
    @classmethod
    def de_json(cls, json_string): ...
    type: Incomplete
    color: Incomplete
    def __init__(self, type, color, **kwargs) -> None: ...

class BackgroundFillGradient(BackgroundFill):
    @classmethod
    def de_json(cls, json_string): ...
    type: Incomplete
    top_color: Incomplete
    bottom_color: Incomplete
    rotation_angle: Incomplete
    def __init__(self, type, top_color, bottom_color, rotation_angle, **kwargs) -> None: ...

class BackgroundFillFreeformGradient(BackgroundFill):
    @classmethod
    def de_json(cls, json_string): ...
    type: Incomplete
    colors: Incomplete
    def __init__(self, type, colors, **kwargs) -> None: ...

class BackgroundType(ABC, JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...

class BackgroundTypeFill(BackgroundFill):
    @classmethod
    def de_json(cls, json_string): ...
    type: Incomplete
    fill: Incomplete
    dark_theme_dimming: Incomplete
    def __init__(self, type, fill, dark_theme_dimming, **kwargs) -> None: ...

class BackgroundTypeWallpaper(BackgroundFill):
    @classmethod
    def de_json(cls, json_string): ...
    type: Incomplete
    document: Incomplete
    dark_theme_dimming: Incomplete
    is_blurred: Incomplete
    is_moving: Incomplete
    def __init__(self, type, document, dark_theme_dimming, is_blurred: Incomplete | None = None, is_moving: Incomplete | None = None, **kwargs) -> None: ...

class BackgroundTypePattern(BackgroundFill):
    @classmethod
    def de_json(cls, json_string): ...
    type: Incomplete
    document: Incomplete
    fill: Incomplete
    intensity: Incomplete
    is_inverted: Incomplete
    is_moving: Incomplete
    def __init__(self, type, document, fill, intensity, is_inverted: Incomplete | None = None, is_moving: Incomplete | None = None, **kwargs) -> None: ...

class BackgroundTypeChatTheme(BackgroundFill):
    @classmethod
    def de_json(cls, json_string): ...
    type: Incomplete
    theme_name: Incomplete
    def __init__(self, type, theme_name, **kwargs) -> None: ...

class ChatBackground(JsonDeserializable):
    @classmethod
    def de_json(cls, json_string): ...
    type: Incomplete
    def __init__(self, type, **kwargs) -> None: ...
