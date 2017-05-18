
class SqlReader:
    def __init__(self, inp, table_name):
        self.input = inp
        self.matchLinePrefix = "INSERT INTO `" + table_name + "` VALUES "
        self.matchLineSuffix = ";"

    def read_insertion_tuples(self):
        for line in self.input:
            line = line.strip()
            if line == "" or line.startswith("--"):
                continue
            elif not line.startswith(self.matchLinePrefix) or not line.endswith(self.matchLineSuffix):
                continue
        
            values_text = line[len(self.matchLinePrefix): len(line)-len(self.matchLineSuffix)]
            return self.parse_tuples(values_text)
        return None

    @staticmethod
    def parse_tuples(text):
        result = []

        state = 0
        tup = []
        token_start = -1
        for i in range(0, len(text)):
            c = text[i]
            if state == 0:
                if c == '(':
                    state = 1
                else:
                    raise Exception("Wrong argument")
            elif state == 1:
                if ord('0') <= ord(c) <= ord('9') or c == '-' or c == '.':
                    state = 2
                elif c == '\'':
                    state = 3
                elif c == 'N':
                    state = 5
                elif c == ')':
                    result.append(tup)
                    tup = []
                    state = 8
                else:
                    raise Exception("Wrong argument")
                token_start = i
                if state == 3:
                    token_start += 1
            elif state == 2:
                if ord('0') <= ord(c) <= ord('9') or c == '-' or c == '.':
                    pass
                elif c == ',' or c == ')':
                    s = text[token_start: i]
                    token_start = -1
                    if s.find(".") == -1:
                        tup.append(int(s))
                    else:
                        tup.append(float(s))
                    if c == ',':
                        state = 7
                    elif c == ')':
                        result.append(tup)
                        tup = []
                        state = 8
                else:
                    raise Exception("Wrong argument")
            elif state == 3:
                if c == '\'':
                    s = text[token_start: i]
                    token_start = -1
                    if s.find('\\') != -1:
                        s = s.replace("\\\\(.)", "$1")
                    tup.append(s)
                    state = 6
                elif c == '\\':
                    state = 4
            elif state == 4:
                if c == '\'' or c == '"' or c == '\\':
                    state = 3
                else:
                    raise Exception("Wrong argument")
            elif state == 5:
                if ord('A') <= ord(c) <= ord('Z'):
                    pass
                elif c == ',' or c == ')':
                    if text[token_start: i] == "NULL":
                        tup.append(None)
                    else:
                        raise Exception("Wrong argument")
                    token_start = -1
                    if c == ',':
                        state = 7
                    elif c == ')':
                        result.append(tup)
                        tup = []
                        state = 8
                else:
                    raise Exception("Wrong argument")
            elif state == 6:
                if c == ',':
                    state = 7
                elif c == ')':
                    result.append(tup)
                    tup = []
                    state = 8
                else:
                    raise Exception("Wrong argument")
            elif state == 7:
                if ord('0') <= ord(c) <= ord('9') or c == '-' or c == '.':
                    state = 2
                elif c == '\'':
                    state = 3
                elif c == 'N':
                    state = 5
                else:
                    raise Exception("Wrong argument")
                token_start = i
                if state == 3:
                    token_start += 1
            elif state == 8:
                if c == ',':
                    state = 9
                else:
                    raise Exception("Wrong argument")
            elif state == 9:
                if c == '(':
                    state = 1
                else:
                    raise Exception("Wrong argument")
            else:
                raise Exception("Assertion Error")

        if state != 8:
            raise Exception("Illegal Argument Exception")
        return result
