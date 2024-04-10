class Lease:
    def __init__(self, metal):
        _kg_ozt_conversao = 32.1507

        cotacao_metal = metal["value"]
        rate = metal["interest"]
        prazo_em_dias = metal["period_in_days"]
        desconto_usd_ozt = metal["deduction_in_usd"]

        self.taxa_lease = rate * prazo_em_dias / 360
        self.cotacao_aplicada_usd_ozt = (cotacao_metal - desconto_usd_ozt) * (1 - self.taxa_lease)
        self.cotacao_aplicada_usd_kg = self.cotacao_aplicada_usd_ozt * _kg_ozt_conversao
        self.pagavel = self.cotacao_aplicada_usd_ozt / cotacao_metal

    def __repr__(self):
        return f"Lease calculado: {self.taxa_lease},\n " \
               f"Cotação aplicada kg: {self.cotacao_aplicada_usd_kg}\n" \
               f"Porcentagem pagável: {self.pagavel}\n\n"


class Metal:
    def __init__(self, teor, lease: Lease, calibracao, retorno_umicore):
        _peso_seco = 2600.000

        self.teor_calibrado = teor - (teor * calibracao)
        self.metal_contido = round(self.teor_calibrado * _peso_seco / 1000, 4)
        self.valor_total = lease.cotacao_aplicada_usd_kg * self.metal_contido

        self.deducao_minima = 0.02 * _peso_seco / 1000
        self.deducao = self.metal_contido - (self.metal_contido * retorno_umicore)
        self.metal_a_receber = round(self.metal_contido - max(self.deducao_minima, self.deducao), 4)

        self.valor_antes_operacao = self.metal_a_receber * lease.cotacao_aplicada_usd_kg

    def __repr__(self):
        return f"Teor calibrado: {self.teor_calibrado}\n" \
               f"Metal contido: {self.metal_contido}\n" \
               f"Valor total dos metais: {self.valor_total}\n" \
               f"Deducao: {self.deducao}\n" \
               f"Metal a receber: {self.metal_a_receber}\n" \
               f"Valor antes das operações: {self.valor_antes_operacao}\n\n"


class Analise:
    def __init__(self, peso: int, pd: Metal, pt: Metal, rh: Metal, cotacao_dolar, tipo):
        self.peso = peso
        self.pd = pd
        self.pt = pt
        self.rh = rh
        self.calcula_dolar(cotacao_dolar, tipo)
        self.custos = self.custos_operacao_usd()
        self.valor_kg = self.valor_a_receber()

        # python arredonda 5 para baixo, diferentemente do excel, que arredonda para cima
        # para isso, é necessário usar esse hack. Adicionamos .5 ao número, de forma que
        # 1. se a casa decimal de milhares for menor que .5, continuará na mesma casa de
        # centenas, então depois de usar o floor, continuará sendo o mesmo número
        # 2. se a casa decimal de milhares for maior que cinco, subirá uma casa de centenas
        # e, depois de arredondada para baixo, retornará o valor desejado
        from math import floor
        self.valor_a_receber =  floor((self.valor_kg * self.peso)*100 + .5)/100

    def custos_operacao_usd(self):
        _peso_liquido = 2600.000
        # custos com pesagem, amostragem e análises
        custos = {
                    "_custos_paa" : 1000,
                    "custos_tratamento" : 2.50 * _peso_liquido,
                    "desconto_tratamento" : 0.25 * _peso_liquido * -1,
                    "custo_refino_pd" : 500 * self.pd.metal_a_receber,
                    "custo_refino_pt" : 500 * self.pt.metal_a_receber,
                    "custo_refino_rh" : 2500 * self.rh.metal_a_receber,
                    "custo_logistica" : 0.6 * _peso_liquido
                }

        return sum(custos.values())
    
    def valor_a_receber(self):
        _peso_liquido_nfe = 2600.000

        valor = sum(metal.valor_antes_operacao for metal in [self.pd, self.pt, self.rh]) - self.custos

        custo_financeiro_1 = .01
        bonus_1 = 0.04
        bonus_2 = 0.03788
        desconto_1 = 0.0673
        desconto_dif_peso = 0.004
        desconto_umidade = 0.008
        custo_financeiro_2 = .0075
        
        valor -= valor * custo_financeiro_1
        valor += valor * bonus_1
        valor /= _peso_liquido_nfe
        valor *= self.dolar
        valor += valor * bonus_2
        valor -= valor * desconto_1
        valor -= valor * desconto_dif_peso
        valor -= valor * desconto_umidade
        valor -= valor * custo_financeiro_2
        
        return round(valor, 2)
    
    def calcula_dolar(self, cotacao_dolar, tipo):
        tipo = load_config("types")[tipo]
        self.dolar = cotacao_dolar * tipo

    def __repr__(self):
        return f"Custos: {self.custos}\n" \
               f"Valor KG:  {self.valor_kg}\n" \
               f"Valor a receber: {self.valor_a_receber}\n\n"


def calculate(sn, analises, tipo):
    lease_info = load_config("lease")["br"]
    calibracao = load_config("calibration")[sn]
    pd_lease = Lease(lease_info["pd"])
    pt_lease = Lease(lease_info["pt"])
    rh_lease = Lease(lease_info["rh"])
    analises_processadas = list()

    for analise in analises:
        analises_processadas.append(Analise(analise["peso"],
                                            Metal(analise["pd"], pd_lease, calibracao["pd"], 
                                                  lease_info["pd"]["received_percentage"]),
                                            Metal(analise["pt"], pt_lease, calibracao["pt"], 
                                                  lease_info["pt"]["received_percentage"]),
                                            Metal(analise["rh"], rh_lease, calibracao["rh"], 
                                                  lease_info["rh"]["received_percentage"]),
                                            lease_info["dolar"], tipo))

    valor_a_receber = sum([analise.valor_a_receber for analise in analises_processadas]) 
    return valor_a_receber


def load_config(filename):
    with open(f"modules/calc/{filename}.json") as f:
        file = f.read()
    from json import loads
    return loads(file)


if __name__ == "__main__":
    ans = calculate("119121", [{"peso": 1, "pd": 1, "pt": 1, "rh": 1}], "1")
    print(ans)
