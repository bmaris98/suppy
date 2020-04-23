class InvalidResourceCategoryException(Exception):

    def __init__(self, required, passed):
        self.message = 'Invalid resource category.'
        self.required = required
        self.passed = passed