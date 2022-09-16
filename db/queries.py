from db.models import Message, User, Chat
from django.db.models import Q, Count, F


def get_messages_that_contain_word(word: str) -> list[Message]:
    return list(Message.objects.filter(text__icontains=word))


def get_untitled_chats() -> list[Chat]:
    return list(Chat.objects.filter(title__startswith="Untitled"))


def get_users_who_sent_messages_in_2015() -> list[str]:
    return list(Message.objects.filter(
        sent__year=2015
    ).values_list("user__first_name",
                  "user__last_name"))


def get_actual_chats() -> list[Chat]:
    return list(Chat.objects.filter(message__sent__year__gt=2020))


def get_messages_contain_authors_first_name():
    return list(Message.objects.filter(
        text__icontains=F("user__first_name")
    ))


def get_users_who_sent_messages_starts_with_m_or_a() -> list[User]:
    return list(User.objects.filter(
        Q(message__text__istartswith="a") | Q(message__text__istartswith="m")
    ))


def get_delivered_or_admin_messages() -> list[Message]:
    return list(Message.objects.filter(
        Q(is_delivered=1) | Q(user__username__startswith="admin")
    ))


def get_count_messages_sent_by_first_name(first_name: str) -> int:
    return Message.objects.filter(
        user__first_name=first_name
    ).values_list("user").count()


def get_top_users_by_number_of_the_messages() -> list[User]:
    return list(User.objects.annotate(
        num_messages=Count("message")
    ).order_by("-num_messages")[:3])


def get_last_5_messages_dicts() -> list[dict]:
    users_messages = []
    query_set = Message.objects.select_related("user").order_by("-sent")[:5]
    for query in query_set:
        users_messages.append(
            {"from": query.user.username, "text": query.text}
        )
    return users_messages


def get_chat_dicts() -> list[dict]:
    chat = []
    query_set = Chat.objects.prefetch_related("users").all()
    for query in query_set:
        chat.append(
            {"id": query.id,
             "title": query.title,
             "users": [member.username for member in query.users.all()]}
        )
    return chat
