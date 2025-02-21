# simulador.py
import networkx as nx
import random

class NetworkSimulator:
    def __init__(self):
        self.network = nx.DiGraph()  # Grafo direcionado para modelar a rede
        self.devices = {}            # Dicionário de dispositivos: {nome: {tipo, IPs}}
        self.ip_to_device = {}       # Mapeamento de IPs para nomes de dispositivos
        self.routers = {}            # Tabelas de roteamento (instâncias da classe Router)
        self.packet_loss_rate = 0.1  # Taxa de perda de pacotes (10%)

    def add_device(self, name, device_type, ip_addresses):
        """
        Adiciona um dispositivo (roteador, switch, host) ao simulador.
        """
        self.devices[name] = {
            'type': device_type,
            'ip_addresses': ip_addresses
        }
        for ip in ip_addresses:
            self.ip_to_device[ip] = name
        self.network.add_node(name)

    def add_link(self, device1, device2, link_type, capacity, latency=1):
        """
        Adiciona um enlace entre dois dispositivos.
        - latency: em milissegundos (padrão: 1ms)
        """
        self.network.add_edge(device1, device2,
                             link_type=link_type,
                             capacity=capacity,
                             latency=latency)
        # Adiciona enlace reverso (rede não direcionada)
        self.network.add_edge(device2, device1,
                             link_type=link_type,
                             capacity=capacity,
                             latency=latency)

    def get_path(self, source_ip, dest_ip):
        """
        Retorna o caminho mais curto entre dois IPs, usando Dijkstra.
        """
        source_device = self.ip_to_device.get(source_ip)
        dest_device = self.ip_to_device.get(dest_ip)

        if not source_device or not dest_device:
            return None

        try:
            path = nx.shortest_path(self.network, source_device, dest_device, weight='latency')
            return path
        except nx.NetworkXNoPath:
            return None

    def ping(self, source_ip, dest_ip):
        path = self.get_path(source_ip, dest_ip)
        if not path:
            return "Erro: Destino inalcançável."

    # Calcula latência total do caminho
        total_latency = sum(
            self.network.edges[path[i], path[i+1]]['latency']  # <-- CORREÇÃO AQUI (alinhamento)
            for i in range(len(path) - 1)
        )  # <-- Garanta que este parêntese esteja alinhado com o "sum"

    # Simula perda de pacotes (4 pacotes enviados)
        received = 0
        for _ in range(4):
            if random.random() >= self.packet_loss_rate:
                received += 1

        loss_percent = (4 - received) * 25
        return f"Ping: {4} transmitidos, {received} recebidos, {loss_percent}% perda, latência {total_latency}ms"

    def traceroute(self, source_ip, dest_ip):
        """
        Simula o comando traceroute, mostrando o caminho percorrido.
        """
        path = self.get_path(source_ip, dest_ip)
        if not path:
            return "Erro: Destino inalcançável."

        hops = []
        for device in path:
            ips = self.devices[device]['ip_addresses']
            # Pega o primeiro IP do dispositivo (ex: roteador tem múltiplos IPs)
            hops.append(f"{device} ({ips[0]})")
        
        return " -> ".join(hops)