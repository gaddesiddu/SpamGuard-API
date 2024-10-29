from .storage import Storage

class Markspam:
    def mark_as_spam(self, user_id, phone_number):
        storage = Storage()
        spam = storage.get_spam_by_phone_number(phone_number)
        if spam:
            storage.update_spam_count_phone_number(phone_number)

        else:
            storage.create_new_spam_to_phone_number(phone_number)

            