#: Contains all media content types.
content_type_media = [
    'text', 'audio', 'document', 'animation', 'game', 'photo', 'sticker', 'video', 'video_note', 'voice', 'contact',
    'location', 'venue', 'dice', 'invoice', 'successful_payment', 'connected_website', 'poll', 'passport_data',
    'web_app_data',
]

#: Contains all service content types such as `User joined the group`.
content_type_service = [
    'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo', 'delete_chat_photo', 'group_chat_created',
    'supergroup_chat_created', 'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id', 'pinned_message',
    'proximity_alert_triggered', 'video_chat_scheduled', 'video_chat_started', 'video_chat_ended',
    'video_chat_participants_invited', 'message_auto_delete_timer_changed', 'forum_topic_created', 'forum_topic_closed',
    'forum_topic_reopened',
]

#: All update types, should be used for allowed_updates parameter in polling.
update_types = [
    "message", "edited_message", "channel_post", "edited_channel_post", "inline_query", "chosen_inline_result",
    "callback_query", "shipping_query", "pre_checkout_query", "poll", "poll_answer", "my_chat_member", "chat_member",
    "chat_join_request",
]