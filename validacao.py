# validacao.py
from ipaddress import IPv4Network, IPv4Address

def validar_subrede(subnet, hosts_necessarios):
    """
    Valida se uma sub-rede suporta o número de hosts requerido.
    Retorna (True, mensagem) se válida, (False, mensagem) se inválida.
    """
    try:
        rede = IPv4Network(subnet, strict=False)
        hosts_disponiveis = rede.num_addresses - 2  # Desconta rede e broadcast
        if hosts_disponiveis >= hosts_necessarios:
            return (True, f"Sub-rede {subnet} válida: suporta {hosts_necessarios} hosts.")
        else:
            return (False, f"Sub-rede {subnet} inválida: suporta apenas {hosts_disponiveis} hosts.")
    except ValueError as e:
        return (False, f"Erro na sub-rede {subnet}: {str(e)}")

def validar_ip(ip, subnets_permitidas):
    """
    Valida se um IP pertence a uma das sub-redes permitidas.
    Retorna (True, mensagem) se válido, (False, mensagem) se inválido.
    """
    try:
        endereco = IPv4Address(ip)
        for subnet in subnets_permitidas:
            rede = IPv4Network(subnet, strict=False)
            if endereco in rede:
                return (True, f"IP {ip} válido: pertence a {subnet}.")
        return (False, f"IP {ip} inválido: não está em nenhuma sub-rede permitida.")
    except ValueError as e:
        return (False, f"Erro no IP {ip}: {str(e)}")

# Exemplo de uso (testes):
if __name__ == "__main__":
    # Teste de validação de sub-rede
    print(validar_subrede("172.16.1.0/27", 24))  # Esperado: válido (30 hosts)
    print(validar_subrede("172.16.2.0/27", 15))  # Esperado: válido (30 hosts)
    print(validar_subrede("172.16.3.0/28", 15))  # Esperado: inválido (14 hosts)

    # Teste de validação de IP
    subnets = ["172.16.1.0/27", "172.16.2.0/27"]
    print(validar_ip("172.16.1.5", subnets))      # Esperado: válido
    print(validar_ip("172.16.3.10", subnets))     # Esperado: inválido