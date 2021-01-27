
class PdfStringUtils:
    @classmethod
    def is_ascii(cls, letter):
        return ord(letter) < 128

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
                ascii_arr.append(letter)
        if ascii_arr:
            ascii_arr.reverse()
            arr.extend(ascii_arr)
        return "".join(arr)[::-1].strip()
