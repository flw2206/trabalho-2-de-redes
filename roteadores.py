# roteadores.py
class Router:
    def __init__(self, name):
        """
        Inicializa um roteador com nome e tabela de roteamento vazia.
        """
        self.name = name
        self.routing_table = []  # Formato: [{destino, mascara, gateway, interface}]

    def add_route(self, destino, mascara, gateway, interface):
        """
        Adiciona uma entrada estática à tabela de roteamento.
        """
        self.routing_table.append({
            "destino": destino,
            "mascara": mascara,
            "gateway": gateway,
            "interface": interface
        })

    def get_routes(self):
        """
        Retorna a tabela de roteamento formatada para exibição.
        """
        return self.routing_table

    def find_route(self, destino_ip):
        """
        Busca a melhor rota para um IP de destino (usando longest prefix match).
        Retorna a entrada da tabela ou None.
        """
        best_match = None
        longest_prefix = 0

        for route in self.routing_table:
            # Simula o cálculo de máscara (para simplificação, compara strings)
            dest_network = route["destino"]
            dest_mask = route["mascara"]
            
            # Verifica se o destino_ip está na sub-rede (implementação simplificada)
            if destino_ip.startswith(dest_network.split('/')[0]):
                # Atualiza a melhor rota com o prefixo mais longo
                prefix_length = int(dest_mask.split('/')[1])
                if prefix_length > longest_prefix:
                    best_match = route
                    longest_prefix = prefix_length

        return best_match