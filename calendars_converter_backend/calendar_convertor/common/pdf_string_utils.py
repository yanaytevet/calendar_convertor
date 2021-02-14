
class PdfStringUtils:
    @classmethod
    def is_ascii(cls, letter: chr) -> bool:
        return ord(letter) < 128

    @classmethod
    def remove_non_ascii(cls, word: str) -> str:
        return "".join(filter(cls.is_ascii, word))

    @classmethod
    def fix_text(cls, text: str) -> str:
        arr = []
        ascii_arr = []
        for letter in text:
            if not cls.is_ascii(letter):
                if ascii_arr:
                    ascii_arr.reverse()
                    arr.extend(ascii_arr)
                    ascii_arr = []
                arr.append(letter)
            else:
                if letter == "(":
                    letter = ")"
                elif letter == ")":
                    letter = "("
                ascii_arr.append(letter)
        if ascii_arr:
            ascii_arr.reverse()
            arr.extend(ascii_arr)
        res = "".join(arr)[::-1].strip()
        res = res.replace("( ", " (")
        res = res.replace(" )", ") ")
        return res
