class Commit:

    def __init__(self, author, email, date, sha1, message, addedLines, deletedLines):
        self.author = author
        self.email = email
        self.date = date
        self.sha1 = sha1
        self.message = message
        self.addedLines = addedLines
        self.deletedLines = deletedLines