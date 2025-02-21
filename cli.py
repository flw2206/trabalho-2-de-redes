# cli.py
def interactive_cli(simulator):
    """
    Interface de linha de comando interativa para executar comandos de rede.
    """
    print("\n=== Interface de Comando do Simulador ===")
    print("Comandos disponíveis:")
    print("  ping <IP_origem> <IP_destino>      - Testa conectividade entre dois IPs")
    print("  traceroute <IP_origem> <IP_destino> - Mostra o caminho entre dois IPs")
    print("  exit                                - Encerra o programa")
    print("--------------------------------------")

    while True:
        try:
            command = input("\n>> ").strip().split()
            if not command:
                continue

            # Comando: ping
            if command[0].lower() == "ping" and len(command) == 3:
                source_ip = command[1]
                dest_ip = command[2]
                result = simulator.ping(source_ip, dest_ip)
                print(f"\n{result}")

            # Comando: traceroute
            elif command[0].lower() == "traceroute" and len(command) == 3:
                source_ip = command[1]
                dest_ip = command[2]
                print("\nTraceroute:")
                path = simulator.traceroute(source_ip, dest_ip)
                print(f"Rota: {path}")

            # Comando: exit
            elif command[0].lower() == "exit":
                print("Encerrando o simulador...")
                break

            else:
                print("Erro: Comando inválido. Use:")
                print("  ping <IP_origem> <IP_destino>")
                print("  traceroute <IP_origem> <IP_destino>")
                print("  exit")

        except KeyboardInterrupt:
            print("\nOperação cancelada pelo usuário.")
            break
        except Exception as e:
            print(f"Erro: {str(e)}")