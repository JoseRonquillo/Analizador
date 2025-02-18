import Analizador_lexico

#Ejemplo de uso

codigo_fuente = """
int suma(int a, int b) {

    int x = a + b * 2;
    int y = x - 5;
    for (int i = 0; i < 10; i++){
        int z = x + 5;
    }
    return y;
}

"""

#Analisis lexico
tokens = Analizador_lexico.identificar(codigo_fuente)
print("Tokens encontrados: ")
for tipo, valor in tokens:
    print(f"{tipo}: {valor}")

#Analisis sintactico
try:
    print("\nIniciando analisis sintáctico...")
    parser = Analizador_lexico.Parser(tokens)
    parser.parsear()
    print("Analisis sintáctico completado sin errores.")
except SyntaxError as e:
    print(e)
