#Código Completo
#Aluno: Felipe Antelo M. de Oliveira
#Matrícula: 2210872
#Professor: Sérgio Colcher
#Polinômio gerador do exercício: P(x) = X^6 + X^4 + X^3 + X + 1  -> bits "1011011" (grau 6)

from typing import List, Tuple

GEN = "1011011"
R = len(GEN) - 1 #Feito para garantir grau 6

def _valida_bits(s: str) -> None:
    if not s or any(c not in "01" for c in s):
        raise ValueError("Forneça só 0/1.")

def _xor_inplace(buf: List[str], pat: str, i: int) -> None:
    for j, b in enumerate(pat):
        buf[i+j] = '0' if buf[i+j] == b else '1'

def _print_passo(k: int, i: int, antes: str, gen: str, depois: str, total: str) -> None:
    print(f"Passo {k:02d} | bit {i} = 1 -> XOR em {i}-{i+len(gen)-1}")
    print(f"Antes : {antes}")
    print(f"Div   : {gen}")
    print(f"Depois: {depois}")
    print(f"Estado: {total}\n")

def crc_divisao_com_passos(msg: str, gen: str = GEN) -> Tuple[str, str]:
    _valida_bits(msg)
    r = len(gen) - 1
    dividendo = msg + "0"*r
    a = list(dividendo)

    print("=== CONFIGURAÇÃO ===")
    print(f"Mensagem (D)        : {msg}  (len={len(msg)})")
    print(f"Polinômio (GEN)     : {gen}  (grau={r})")
    print(f"Dividendo inicial   : {dividendo}\n")

    k = 0
    for i in range(0, len(a) - len(gen) + 1):
        if a[i] == '1':
            k += 1
            janela_antes = ''.join(a[i:i+len(gen)])
            _xor_inplace(a, gen, i)
            janela_depois = ''.join(a[i:i+len(gen)])
            _print_passo(k, i, janela_antes, gen, janela_depois, ''.join(a))
        # se a[i]=='0': nenhum passo (como na divisão longa)

    crc = ''.join(a[-r:]) if r>0 else ""
    T = msg + crc
    print("=== RESULTADOS ===")
    print(f"CRC/FCS (r={r})     : {crc}")
    print(f"Transmitido (T=D||C): {T}")

    # verificação: T ÷ GEN deve ter resto zero
    ok = verifica_resto_zero(T, gen)
    print(f"\nVerificação (T ÷ GEN): resto {'0'*r} -> {'OK' if ok else 'ERRO'}")
    return crc, T

def verifica_resto_zero(bits: str, gen: str = GEN) -> bool:
    a = list(bits)
    m = len(gen)
    for i in range(0, len(a) - m + 1):
        if a[i] == '1':
            _xor_inplace(a, gen, i)
    resto = a[-(m-1):] if m > 1 else []
    return all(c == '0' for c in resto)

if __name__ == "__main__":
    import argparse
    p = argparse.ArgumentParser(description="CRC (divisão módulo-2) com passos. GEN=1011011.")
    p.add_argument("--msg", required=True, help="Mensagem binária (ex.: 32 bits).")
    args = p.parse_args()
    crc_divisao_com_passos(args.msg, GEN)