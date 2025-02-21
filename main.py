# main.py
from simulador import NetworkSimulator
from config_rede import setup_network
from cli import interactive_cli

if __name__ == "__main__":
    # Inicializa a rede com a topologia definida na Fase 1
    rede_simulada = setup_network()
    
    # Inicia a interface de linha de comando interativa
    print("=== Simulador de Rede - Projeto 2 ===")
    print("Comandos disponíveis:")
    print("- ping <IP_origem> <IP_destino>")
    print("- traceroute <IP_origem> <IP_destino>")
    print("- exit")
    interactive_cli(rede_simulada)