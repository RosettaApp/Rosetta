from .base import BaseProvider

class CaesarProvider(BaseProvider):
    name = "Caesar"
    slug = "caesar"
    
    def ask(self, prompt):
        def encrypt(text,s):
            result = ""
            for char in text:
                if (char.isupper()):
                    result += chr((ord(char) + s-65) % 26 + 65)
                else:
                    result += chr((ord(char) + s - 97) % 26 + 97)
            return result
        r = encrypt(prompt, 4)
        print(r)
        return r

    def load(self, data):
        pass