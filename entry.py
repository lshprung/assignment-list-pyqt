
class Entry:
    def __init__(self, desc, due = "", due_alt = "", link = ""):
        self.desc = desc
        self.due = due
        self.due_alt = due_alt
        self.link = link
        self.done = False
