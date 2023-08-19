import mimetypes
import re

class Parser:
    """
    Custom class to parse results whether it is email or not.
    """

    def parse(self, text: str) -> bool:
        """
        Check if given string is an email adress.
        """

        # Regular expression comparison
        regex_template = r'^[\w\.-]+@[\w\.-]+\.\w+$'
        if not re.match(regex_template, text):
            return False
        
        # Comparison with different types of 
        # static elements (videos, photos, so on)
        restr_types = ['video', 'image', 'audio', 'text']
        try:
            if mimetypes.guess_type(text)[0].split("/")[0] in restr_types:
                return False
        except AttributeError:
            pass

        # Manually remove `bootstrap` queries.
        if 'bootstrap' in text:
            return False
        
        # return True if passed every step of validation.
        return True
        