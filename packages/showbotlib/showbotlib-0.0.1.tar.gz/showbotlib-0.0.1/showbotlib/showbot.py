from .telegramclient import TelegramClient
from . import tv_program


class ShowTelegramBot(TelegramClient):
    def run(self):
        while True:
            updates = self.get_updates()
            self.updates_processing(updates)

    def updates_processing(self, updates):
        for update in updates:
            answer = self.update_processing(update)
            if answer is not None:
                self.sent_message(answer["id"], answer["text"], "HTML")
        if len(updates):
            self.set_updates_readed(updates[-1].update_id)

    def update_processing(self, update):
        if update.message is None:
            return None
        text = update.message.text
        user_id = update.message.from_field.id
        answer = {"id": user_id, "text": ""}
        if text is not None:
            if text.startswith("/"):
                answer["text"] = self.parse_commands(
                    user_id, *text.split(" ", 1)
                )
            else:
                answer["text"] = self.find_show_answer(text)
        else:
            answer["text"] = "Some error"

        return answer

    def find_show_answer(self, show_name):
        text = ""
        try:
            show_data = tv_program.get_show_data(show_name)
            text = f"Name: {show_data.name}\n"
            text += f"Network Name: {show_data.network.name}\n"
            text += f"Network Country Name: {show_data.network.country.name}\n"
            text += "Summary:"
            text += (
                str(show_data.summary)
                .replace("<p>", "")
                .replace("</p>", "")
            )
        except ValueError:
            text = "Show not found"
        return text

    def parse_commands(self, user_id, command, text=None):
        if command == "/add_to_favorites":
            return self.add_to_favorites(user_id, text)
        elif command == "/get_favorites":
            return self.get_favorites(user_id)
        elif command == "/remove_from_favorites":
            return self.remove_from_favorites(user_id, text)
        else:
            return "Unknown command"

    def add_to_favorites(self, user_id, show_name):
        if show_name is None:
            return "Show not found"
        text = ""
        show_name.replace(' ', '\\ ')
        if not hasattr(self, "favorites"):
            self.favorites = dict()
        if user_id not in self.favorites:
            self.favorites[user_id] = list()
        try:
            show_data = tv_program.get_show_data(show_name)
            self.favorites[user_id].append(show_data.name)
            text = f"{show_data.name} has been added to the favorites list"
        except ValueError:
            text = "Show not found"
        return text

    def get_favorites(self, user_id):
        text = ""
        if not hasattr(self, "favorites"):
            self.favorites = dict()
        if user_id not in self.favorites:
            self.favorites[user_id] = list()
        if len(self.favorites[user_id]) == 0:
            text = "You don't have favorite shows"
        else:
            text = ""
            for show in self.favorites[user_id]:
                text += show + "\n"
        return text

    def remove_from_favorites(self, user_id, show_name):
        if show_name is None:
            return "Show not found"
        text = ""
        show_name.replace(' ', '\\ ')
        if not hasattr(self, "favorites"):
            self.favorites = dict()
        if user_id not in self.favorites:
            self.favorites[user_id] = list()
        if show_name not in self.favorites[user_id]:
            text = "You don't have this show in your favorites"
        else:
            self.favorites[user_id].remove(show_name)
            text = f"Show {show_name} has been removed from the favorites list"
        return text
