from arrai import Arrai


class UIManager(object):

    def __init__(self, text_string: str):

        self.set_arrais(text_string)

    def set_arrais(self, text_string: str):
        self.arrai_list = []

        text_string_list = text_string.splitlines()

        currentPos = 1
        for x in range(int(text_string_list[0])):
            VectorOrMatrix = text_string_list[currentPos]
            currentPos += 1

            if VectorOrMatrix == 'V':
                total = int(text_string_list[currentPos])
                currentPos += 1

                temp_list = text_string_list[currentPos].split(maxsplit=total)
                currentPos += 1

                temp_list = list(map(int, temp_list))
                self.arrai_list.append(Arrai(temp_list))

            elif VectorOrMatrix == 'M':
                (rows, cols) = list(map(int, text_string_list[currentPos].split()))
                currentPos += 1
                arrai = []

                for r in range(rows):
                    temp_list = text_string_list[currentPos].split(maxsplit=cols)
                    currentPos += 1
                    temp_list = list(map(int, temp_list))
                    arrai.append(temp_list)

                self.arrai_list.append(Arrai(arrai))

    def run_result(self, text_string: str) -> str:
        text_list = text_string.splitlines()

        for problem in text_list:
            pass
