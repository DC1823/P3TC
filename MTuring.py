import yaml

class TuringMachine:
    def __init__(self, estados, alfabeto, cinta_alfabeto, transi, estado_inicial, blank_s, estado_final):
        self.estados = estados
        self.alfabeto = alfabeto
        self.cinta_alfabeto = cinta_alfabeto
        self.transi = transi
        self.estado_inicial = estado_inicial
        self.blank_s = blank_s
        self.estado_final = estado_final
        self.estado_act = estado_inicial
        self.cinta = []
        self.posicion_i = 0

    def reiniciar_cinta(self, cadena_entrada):
        self.cinta = list(cadena_entrada) + [self.blank_s]
        self.estado_act = self.estado_inicial
        self.posicion_i = 0

    def paso(self):
        c_debajo = self.cinta[self.posicion_i]
        if (self.estado_act, c_debajo) in self.transi:
            siguiente, escribir_c, mover = self.transi[(self.estado_act, c_debajo)]
            self.cinta[self.posicion_i] = escribir_c
            self.posicion_i += 1 if mover == 'R' else -1
            self.estado_act = siguiente
            if self.posicion_i == len(self.cinta):
                self.cinta.append(self.blank_s)
            return True
        return False

    def c_aceptado(self):
        return self.estado_act in self.estado_final

    def correr(self, cadena_entrada):
        self.reiniciar_cinta(cadena_entrada)
        while self.paso():
            pass
        return self.c_aceptado(), ''.join(self.cinta).rstrip(self.blank_s)

def cargar_maquina_t(file_path):
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    estados = set(data['estados_q']['lista_'])
    alfabeto = set(data['alfabeto'])
    cinta_alfabeto = set(data['cinta_alfabeto'])
    estado_inicial = data['estados_q']['inicial']
    blank_s = data['cinta_alfabeto'][0]
    estado_final = {data['estados_q']['final']}

    transi = {}
    for transicion in data['delta']:
        key = (transicion['parametros']['estado_inicial'], transicion['parametros']['entrada_cinta'])
        value = (transicion['salida']['estado_final'],
                 transicion['salida']['salida_cinta'],
                 transicion['salida']['despla_cinta'])
        transi[key] = value

    return TuringMachine(estados, alfabeto, cinta_alfabeto, transi, estado_inicial, blank_s, estado_final), data['simulador_cadena']

def revisarxy(cadena_entrada):
    xv = False
    yv = False
    for char in cadena_entrada:
        if char == 'Y':
            yv = True
        elif char == 'X' and yv:
            return False
        elif char == 'X':
            xv = True
        else:
            return False
    cx = cadena_entrada.count('X')
    cy = cadena_entrada.count('Y')
    return cx == cy and xv and yv

archi = 'yaml.yaml'
turingm, simulador_cadena = cargar_maquina_t(archi)
for string in simulador_cadena:
    c_aceptado, cintafinal = turingm.correr(string)
    accept= revisarxy(cintafinal)    
    print(f"Cadena: {string}, Aceptado: {accept}, Cinta Final: {cintafinal}")
