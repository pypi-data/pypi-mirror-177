class NoChanges(Exception):
    def __init__(self, message="No changes found in latest section"):
        self.message = message
        super().__init__(self.message)


class InvalidChanges(Exception):
    def __init__(self, invalid_changes):
        self.invalid_changes = invalid_changes
        self.message = f"Invalid changes found: {invalid_changes}"
        super().__init__(self.message)
