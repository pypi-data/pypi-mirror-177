class PalindromeString:
    def __init__(self, string):
        self.string = string

    def check_string_is_palindrome_or_not(self):
        palindrome_string = self.string[::-1]
        if self.string == palindrome_string:
            return True
        else:
            return False
