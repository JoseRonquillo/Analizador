#Analisis léxico
#Definir los patrones
import re

token_patron = {
    "KEYWORD": r"\b(if|else|while|return|int|float|void|for|print)\b",
    "IDENTIFIER": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    "NUMBER": r"\b\d+(\.\d+)?\b",
    "OPERATOR": r"[+\-*/=<>]",
    "DELIMITER": r"[(),;{}]",
    "WHITESPACE": r"\s+",
    "LOGICAL_OPERATOR": r"&&|\|\||!",
    "INCREMENT_DECREMENT": r"\+\+|--",
    "COMPARISON_OPERATOR": r"<=|>=|==|!=",
}

def identificar(texto):
    patron_general = "|".join(f"(?P<{token}>{patron})" for token, patron in token_patron.items())
    patron_regex = re.compile(patron_general)
    tokens_encontrados = []
    for match in patron_regex.finditer(texto):
        for token, valor in match.groupdict().items():
            if valor is not None and token != "WHITESPACE":
                tokens_encontrados.append((token,valor))
    return tokens_encontrados

#Analizador sintáctico
class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def obtener_token_actual(self):
        return self.tokens[self.pos]  if self.pos < len(self.tokens) else None

    def coincidir(self, tipo_esperado):
        token_actual = self.obtener_token_actual()
        if token_actual and token_actual[0] == tipo_esperado:
            self.pos += 1
            return token_actual
        raise SyntaxError(f'Error Sintáctico, se esperaba {tipo_esperado}, pero se encontró {token_actual}')

    def parsear(self):
        self.funcion()

    def funcion(self):
        self.coincidir("KEYWORD")
        self.coincidir("IDENTIFIER")
        self.coincidir("DELIMITER")
        self.parametros()
        self.coincidir("DELIMITER")

        self.coincidir("DELIMITER")

        self.cuerpo()
        self.coincidir("DELIMITER")

    def parametros(self):
        if self.obtener_token_actual() and self.obtener_token_actual()[0] == "KEYWORD":
            self.coincidir("KEYWORD")
            self.coincidir("IDENTIFIER")

            while self.obtener_token_actual() and self.obtener_token_actual()[1] == ",":
                self.coincidir("DELIMITER")
                self.coincidir("KEYWORD")
                self.coincidir("IDENTIFIER")

    def asignacion(self):
        self.coincidir("KEYWORD")
        self.coincidir("IDENTIFIER")
        self.coincidir("OPERATOR")
        self.expresion()
        self.coincidir("DELIMITER")

    def asignacion_ciclos_for(self):
        self.coincidir("KEYWORD")
        self.coincidir("DELIMITER")
        self.coincidir("KEYWORD")
        self.coincidir("IDENTIFIER")
        self.coincidir("OPERATOR")
        self.coincidir("NUMBER")
        self.coincidir("DELIMITER")
        self.coincidir("IDENTIFIER")
        self.coincidir("OPERATOR")
        self.coincidir("NUMBER")
        self.coincidir("DELIMITER")
        self.coincidir("IDENTIFIER")
        self.coincidir("OPERATOR")
        self.coincidir("OPERATOR")
        self.coincidir("DELIMITER")
        self.coincidir("DELIMITER")
        self.cuerpo()
        self.coincidir("DELIMITER")
    def expresion(self):
        self.termino()
        while self.obtener_token_actual() and self.obtener_token_actual()[1] in "+-":
            self.coincidir("OPERATOR")
            self.termino()

    def termino(self):
        self.factor()
        while self.obtener_token_actual() and self.obtener_token_actual()[1] in "*/":
            self.coincidir("OPERATOR")
            self.factor()

    def factor(self):
        if self.obtener_token_actual()[0] == "IDENTIFIER" or self.obtener_token_actual()[0] == "NUMBER":
            self.coincidir(self.obtener_token_actual()[0])
        elif self.obtener_token_actual()[1] == "(":
            self.coincidir("DELIMITER")
            self.expresion()
            self.coincidir("DELIMITER")
        else:
            raise SyntaxError(
                f"Error Sintáctico: Se esperaba un número, variable o paréntesis, pero se encontró {self.obtener_token_actual()}")

    def retorna(self):
        self.coincidir("KEYWORD")
        self.expresion()
        self.coincidir("DELIMITER")

    def cuerpo(self):
        while self.obtener_token_actual() and self.obtener_token_actual()[1] != "}":
            if self.obtener_token_actual()[0] == "KEYWORD" and self.obtener_token_actual()[1] == "return":
                self.retorna()
            elif self.obtener_token_actual()[0] == "KEYWORD" and self.obtener_token_actual()[1] == "for":
                self.asignacion_ciclos_for()
            else:
                self.asignacion()