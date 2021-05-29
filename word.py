class LexicalAnalyser:
    """
    词法分析程序
    """

    # 要读取的代码文件名称
    filename = 'code.txt'
    # 关键字
    key_word = ["begin", "if", "then", "else", "while", "do", "end", "print"]
    # 操作符
    operator = ['+', '-', '*', '/', ':', '<', '<=', '>', '>=', '=', ';', '(', ')', '#']
    # 存放结果二元组
    res = []

    def analyse(self, string: str) -> str:
        """
        调用的分析函数
        :param string:此时分析行内的代码
        :return:返回除去分析结果后的代码
        """
        try:
            # 首先除去空格类
            i = 0
            while string[i] == ' ' or string[i] == '\n' or string[i] == '\t':
                i += 1
            string = string[i:]
            if string[0] == '+' or string[0] == '-' or string[0] == '*' or string[0] == '/' or string[0] == '=' or \
                    string[0] == ';' or string[0] == '(' or string[0] == ')' or string[0] == '#' or string[0] == ':':
                self.res.append((13 + self.operator.index(string[0]), string[0]))
                string = string[1:]
            elif string[0] == '<' or string[0] == '>':
                if len(string) > 1 and string[1] == '=':
                    self.res.append((13 + self.operator.index(string[0:2]), string[0:2]))
                    string = string[2:]
                else:
                    self.res.append((13 + self.operator.index(string[0]), string[0]))
                    string = string[1:]
            elif string[0:5] == "begin":
                self.res.append((1 + self.key_word.index("begin"), "begin"))
                string = string[5:]
            elif string[0:2] == "if":
                self.res.append((1 + self.key_word.index("if"), "if"))
                string = string[2:]
            elif string[0:4] == "then":
                self.res.append((1 + self.key_word.index("then"), "then"))
                string = string[4:]
            elif string[0:4] == "else":
                self.res.append((1 + self.key_word.index("else"), "else"))
                string = string[4:]
            elif string[0:5] == "while":
                self.res.append((1 + self.key_word.index("while"), "while"))
                string = string[5:]
            elif string[0:2] == "do":
                self.res.append((1 + self.key_word.index("do"), "do"))
                string = string[2:]
            elif string[0:3] == "end":
                self.res.append((1 + self.key_word.index("end"), "end"))
                string = string[3:]
            elif string[0:5] == "print":
                self.res.append((1 + self.key_word.index("print"), "print"))
                string = string[5:]
            else:
                i = 0
                while string[i].isalpha() or string[i].isnumeric():
                    i += 1
                if string[0:i].isalpha():
                    self.res.append((10, string[0:i]))
                elif string[0:i].isnumeric():
                    self.res.append((11, string[0:i]))
                string = string[i:]
                # 如果到最后一个情况都是没有向前推进，代表此时地方出错
                if i == 0:
                    print("warning::未识别的符号", string[0])
                    return string[1:0]
            return string
        # 上述操作很可能最后会操作越界，那么就顺便抓一下越界错误，返回空字符串表明此行已经完成，会忽略掉并不该出现的错误
        except IndexError:
            return ""

    def start(self) -> None:
        with open(self.filename, 'r') as file:
            # 从文件中将全部信息读取出来
            txt = file.readlines()
            print("初始要处理的源代码为：")
            for line in txt:
                print(line, end='')
            for line in txt:
                # 如果不为空才继续，否则直接看下一行
                while len(line) != 0:
                    line = self.analyse(line)

            # 有正规格式地显示结果
            i = 0
            print("经过词法分析后的二元组结果为：")
            for res_tuple in self.res:
                print("({},{})".format(res_tuple[0], res_tuple[1]), end=' ')
                i += 1
                if i == 10:
                    print()
                    i = 0


class GrammaticalAnalyser:
    """
    递归下降语法分析器
    """
    def __init__(self, res: list) -> None:
        self.res = res
        self.i = 0

    def start(self):
        if self.res[self.i][0] == 1:  # begin
            self.i += 1
            if self.res[self.i][0] == 17:  # :
                self.i += 1
            else:
                raise Exception("识别失败")
        else:
            raise Exception("识别失败")

        self.sentences()  # 语句串

        if self.res[self.i][0] == 7:  # end
            self.i += 1
        else:
            raise Exception("识别失败")
        if self.i == len(self.res):  # 判断是否完成识别
            return True
        else:
            return False

    def sentences(self):
        self.sentence()  # 语句
        if self.res[self.i][0] == 2 or self.res[self.i][0] == 5 or self.res[self.i][0] == 8\
                or self.res[self.i][0] == 10:  # if while ID print
            self.sentences()  # 语句

    def sentence(self):
        if self.res[self.i][0] == 10:  # ID，赋值语句
            self.assign()  # 赋值语句
            if self.res[self.i][0] == 23:
                self.i += 1
            else:
                raise Exception("识别失败")
        elif self.res[self.i][0] == 2 or self.res[self.i][0] == 5:  # if and while
            self.repeat()  # 循环判断操作
        elif self.res[self.i][0] == 8:  # print
            self.print_function()  # 输出操作
            if self.res[self.i][0] == 23:
                self.i += 1
            else:
                raise Exception("识别失败")
        else:
            raise Exception("识别失败")

    def assign(self):
        if self.res[self.i][0] == 10:  # ID
            self.i += 1
            if self.res[self.i][0] == 22:  # =
                self.i += 1
                self.expression()  # 表达式
            else:
                raise Exception("识别失败")
        else:
            raise Exception("识别失败")

    def expression(self):
        self.term()  # 项
        if self.res[self.i][0] == 13 or self.res[self.i][0] == 14:  # + -
            self.i += 1
            self.term()  # 项

    def term(self):
        self.factor()  # 因子
        if self.res[self.i][0] == 15 or self.res[self.i][0] == 16:  # * /
            self.i += 1
            self.factor()  # 因子

    def factor(self):
        if self.res[self.i][0] == 10 or self.res[self.i][0] == 11:  # ID NUM
            self.i += 1
        elif self.res[self.i][0] == 24:  # (
            self.i += 1
            self.expression()  # 表达式
            if self.res[self.i][0] == 25:  # )
                self.i += 1
            else:
                raise Exception("识别失败")
        else:
            raise Exception("识别失败")

    def repeat(self):
        if self.res[self.i][0] == 5:  # while
            self.repeat_check()  # 判断循环
            if self.res[self.i][0] == 1:  # begin
                self.i += 1
                if self.res[self.i][0] == 17:  # :
                    self.i += 1
                    self.sentences()  # 语句串
                    if self.res[self.i][0] == 7:  # end
                        self.i += 1
                    else:
                        raise Exception("识别失败")
                else:
                    raise Exception("识别失败")
            else:
                raise Exception("识别失败")
        elif self.res[self.i][0] == 2:  # if
                self.repeat_check()  # 判断循环

    def repeat_check(self):
        if self.res[self.i][0] == 2 or self.res[self.i][0] == 5:  # if while
            self.i += 1
            if self.res[self.i][0] == 24:  # (
                self.i += 1
                self.judgment()  # 判断式
                if self.res[self.i][0] == 25:  # )
                    self.i += 1
                    if self.res[self.i][0] == 17:  # :
                        self.i += 1
                    else:
                        raise Exception("识别失败")
                else:
                    raise Exception("识别失败")
            else:
                raise Exception("识别失败")
        else:
            raise Exception("识别失败")

    def judgment(self):
        self.expression()  # 表达式
        self.judgment_symbol()  # 判断符号
        self.expression()  # 表达式

    def judgment_symbol(self):
        if self.res[self.i][0] == 18 or self.res[self.i][0] == 19 or self.res[self.i][0] == 20 or \
                self.res[self.i][0] == 21:  # < > <= >=
            self.i += 1
        else:
            raise Exception("识别失败")

    def print_function(self):
        if self.res[self.i][0] == 8:  # print
            self.i += 1
            if self.res[self.i][0] == 24:  # (
                self.i += 1
                self.expression()
                if self.res[self.i][0] == 25:  # )
                    self.i += 1
                else:
                    raise Exception("识别失败")
            else:
                raise Exception("识别失败")
        else:
            raise Exception("识别失败")


if __name__ == "__main__":
    a = LexicalAnalyser()
    a.start()
    print()
    res = a.res
    b = GrammaticalAnalyser(res)
    try:
        if b.start():
            print("语法分析成功")
        else:
            print("语法分析失败")
    except Exception:
        print("语法分析出现错误，失败")
