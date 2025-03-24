
import re

tokens_patron = {
    "KEYWORD": r"\b(if|else|while|return|int|float|void)\b",
    "IDENTIFIER": r"\b[a-zA-Z_][a-zA-Z0-9_]*\b",
    "NUMBER": r"\b\d+(\.\d+)?\b",
    "OPERATOR": r"[+\-*/=<>!]=?",
    "DELIMITER": r"[(),;{}]",
    "WHITESPACE": r"\s+"
}


class NodoAST():
    def __init__(self):
        pass

    def traducir(self):
        raise NotImplementedError("Método traducir() No implementado en este nodo.")

    def generar_codigo(self):
        raise NotImplementedError("Método generar_codigo() No implementado en este nodo.")


class NodoIf(NodoAST):
    def __init__(self, condicion, cuerpo_if, cuerpo_else=None):
        super().__init__()
        self.condicion = condicion
        self.cuerpo_if = cuerpo_if
        self.cuerpo_else = cuerpo_else

    def traducir(self):
        traduccion = f"if {self.condicion.traducir()}:\n"
        traduccion += "\n".join(f"    {inst.traducir()}" for inst in self.cuerpo_if)
        
        if self.cuerpo_else:
            traduccion += "\nelse:\n"
            traduccion += "\n".join(f"    {inst.traducir()}" for inst in self.cuerpo_else)
            
        return traduccion

    def generar_codigo(self):
        codigo = []
        codigo.append(self.condicion.generar_codigo())
        codigo.append("    cmp eax, 0")
        codigo.append(f"    je etiqueta_else_{id(self)}")
        
        for inst in self.cuerpo_if:
            codigo.append(inst.generar_codigo())
        
        if self.cuerpo_else:
            codigo.append(f"    jmp etiqueta_fin_if_{id(self)}")
            codigo.append(f"etiqueta_else_{id(self)}:")
            
            for inst in self.cuerpo_else:
                codigo.append(inst.generar_codigo())
                
        codigo.append(f"etiqueta_fin_if_{id(self)}:")
        return "\n".join(codigo)


class NodoFuncion(NodoAST):
    def __init__(self, nombre, parametros, cuerpo):
        super().__init__()
        self.nombre = nombre
        self.parametros = parametros
        self.cuerpo = cuerpo

    def traducir(self):
        params = ", ".join(p.traducir() for p in self.parametros)
        cuerpo = "\n    ".join(c.traducir() for c in self.cuerpo)
        return f"def {self.nombre[1]}({params}):\n    {cuerpo}"

    def generar_codigo(self):
        codigo = []
        codigo.append(f"{self.nombre[1]}:")
        codigo.append("    push ebp")
        codigo.append("    mov ebp, esp")
        
        for inst in self.cuerpo:
            codigo.append(inst.generar_codigo())
            
        codigo.append("    mov esp, ebp")
        codigo.append("    pop ebp")
        codigo.append("    ret")
        return "\n".join(codigo)


class NodoParametro(NodoAST):
    def __init__(self, tipo, nombre):
        super().__init__()
        self.tipo = tipo
        self.nombre = nombre

    def traducir(self):
        return self.nombre[1]


class NodoAsignacion(NodoAST):
    def __init__(self, nombre, expresion):
        super().__init__()
        self.nombre = nombre
        self.expresion = expresion

    def traducir(self):
        return f"{self.nombre[1]} = {self.expresion.traducir()}"

    def generar_codigo(self):
        codigo = self.expresion.generar_codigo()
        codigo += f"\n    mov [{self.nombre[1]}], eax"
        return codigo


class NodoOperacion(NodoAST):
    def __init__(self, izquierda, operador, derecha):
        super().__init__()
        self.izquierda = izquierda
        self.operador = operador
        self.derecha = derecha

    def traducir(self):
        return f"{self.izquierda.traducir()} {self.operador[1]} {self.derecha.traducir()}"

    def generar_codigo(self):
        codigo = []
        codigo.append(self.izquierda.generar_codigo())
        codigo.append("    push eax")
        codigo.append(self.derecha.generar_codigo())
        codigo.append("    pop ebx")

        if self.operador[1] == "+":
            codigo.append("    add eax, ebx")
        elif self.operador[1] == "-":
            codigo.append("    sub ebx, eax")
            codigo.append("    mov eax, ebx")
        elif self.operador[1] == "*":
            codigo.append("    imul eax, ebx")
        elif self.operador[1] == "/":
            codigo.append("    xchg eax, ebx")
            codigo.append("    cdq")
            codigo.append("    idiv ebx")
        elif self.operador[1] == "==":
            codigo.append("    cmp ebx, eax")
            codigo.append("    sete al")
            codigo.append("    movzx eax, al")
        elif self.operador[1] == "!=":
            codigo.append("    cmp ebx, eax")
            codigo.append("    setne al")
            codigo.append("    movzx eax, al")
        elif self.operador[1] == "<":
            codigo.append("    cmp ebx, eax")
            codigo.append("    setl al")
            codigo.append("    movzx eax, al")
        elif self.operador[1] == ">":
            codigo.append("    cmp ebx, eax")
            codigo.append("    setg al")
            codigo.append("    movzx eax, al")
            
        return "\n".join(codigo)

    def optimizar(self):
        if isinstance(self.izquierda, NodoOperacion):
            izquierda = self.izquierda.optimizar()
        else:
            izquierda = self.izquierda
            
        if isinstance(self.derecha, NodoOperacion):
            derecha = self.derecha.optimizar()
        else:
            derecha = self.derecha

        if isinstance(izquierda, NodoNumero) and isinstance(derecha, NodoNumero):
            if self
