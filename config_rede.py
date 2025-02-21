# config_rede.py
from ipaddress import IPv4Network
from simulador import NetworkSimulator
from roteadores import Router

def setup_network():
    """
    Configura a topologia da rede em árvore conforme especificado na Fase 1.
    Retorna uma instância do NetworkSimulator pronta para uso.
    """
    simulator = NetworkSimulator()

    # --- Camada de Núcleo (Core) ---
    # Roteador principal R1 com interfaces para agregação
    simulator.add_device("R1", "router", ["172.16.0.1", "172.16.0.5"])
    r1 = Router("R1")
    r1.add_route("172.16.1.0", "255.255.255.0", "172.16.0.2", "172.16.0.1")  # Rota para a1
    r1.add_route("172.16.2.0", "255.255.255.0", "172.16.0.6", "172.16.0.5")  # Rota para a2
    simulator.routers["R1"] = r1

    # --- Camada de Agregação ---
    # Roteador a1 (conectado a R1 e switches de borda e1/e2)
    simulator.add_device("a1", "router", ["172.16.0.2", "172.16.1.30"])
    a1 = Router("a1")
    a1.add_route("172.16.1.0", "255.255.255.0", "0.0.0.0", "172.16.1.30")     # Rota local
    a1.add_route("0.0.0.0", "0.0.0.0", "172.16.0.1", "172.16.0.2")           # Rota padrão para R1
    simulator.routers["a1"] = a1

    # Roteador a2 (conectado a R1 e switches de borda e3/e4)
    simulator.add_device("a2", "router", ["172.16.0.6", "172.16.2.30"])
    a2 = Router("a2")
    a2.add_route("172.16.2.0", "255.255.255.0", "0.0.0.0", "172.16.2.30")    # Rota local
    a2.add_route("0.0.0.0", "0.0.0.0", "172.16.0.5", "172.16.0.6")           # Rota padrão para R1
    simulator.routers["a2"] = a2

    # --- Camada de Borda (Switches) ---
    simulator.add_device("e1", "switch", ["172.16.1.1"])
    simulator.add_device("e2", "switch", ["172.16.1.33"])
    simulator.add_device("e3", "switch", ["172.16.2.1"])
    simulator.add_device("e4", "switch", ["172.16.2.33"])

    # --- Enlaces ---
    # Core (R1) <-> Agregação (a1/a2)
    simulator.add_link("R1", "a1", "fibra", "10 Gbps", latency=2)
    simulator.add_link("R1", "a2", "fibra", "10 Gbps", latency=2)

    # Agregação (a1/a2) <-> Borda (e1/e2/e3/e4)
    simulator.add_link("a1", "e1", "par trançado", "1 Gbps", latency=5)
    simulator.add_link("a1", "e2", "par trançado", "1 Gbps", latency=5)
    simulator.add_link("a2", "e3", "par trançado", "1 Gbps", latency=5)
    simulator.add_link("a2", "e4", "par trançado", "1 Gbps", latency=5)

    # --- Geração de Hosts ---
    generate_hosts(simulator, "e1", "172.16.1.0/27", 24)  # e1: 24 hosts
    generate_hosts(simulator, "e2", "172.16.1.32/27", 24) # e2: 24 hosts
    generate_hosts(simulator, "e3", "172.16.2.0/27", 15)  # e3: 15 hosts
    generate_hosts(simulator, "e4", "172.16.2.32/27", 15) # e4: 15 hosts

    return simulator

def generate_hosts(simulator, switch_name, subnet, num_hosts):
    """
    Gera hosts em uma sub-rede específica e conecta-os a um switch.
    """
    network = IPv4Network(subnet, strict=False)
    for i in range(1, num_hosts + 1):  # Evita o IP de rede (i=0)
        host_ip = str(network[i])
        host_name = f"host_{switch_name}_{i}"
        simulator.add_device(host_name, "host", [host_ip])
        simulator.add_link(switch_name, host_name, "par trançado", "100 Mbps", latency=1)