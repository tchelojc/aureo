"""
╔══════════════════════════════════════════════════════════════════╗
║          UNIVERSO ÁUREO — ALMAFLUXO STUDIO QUANTUM              ║
║          Motor: FluxoMatemático + Mecânica Kepleriana NASA       ║
║          φ=1.618 | MARC=0.54 | JUBILO=0.45 | DEUS=0.18         ║
║          GRATIDÃO=1.80 | CICLO=0.99                             ║
╚══════════════════════════════════════════════════════════════════╝
"""

import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import math
import os
import urllib.request
from datetime import datetime

# ══════════════════════════════════════════════════════════════════
# TENTAR IMPORTAR BIBLIOTECAS CIENTÍFICAS (OPCIONAIS)
# ══════════════════════════════════════════════════════════════════
try:
    import rebound
    import assist
    REBOUND_AVAILABLE = True
except ImportError:
    REBOUND_AVAILABLE = False

# ══════════════════════════════════════════════════════════════════
# CONSTANTES FÍSICAS E FLUXOMATEMÁTICO
# ══════════════════════════════════════════════════════════════════
G       = 6.67430e-11        # Constante gravitacional (m³ kg⁻¹ s⁻²)
c       = 2.99792458e8       # Velocidade da luz (m/s)
h_planck = 6.62607015e-34    # Constante de Planck (J·s)
e_carga = 1.602176634e-19    # Carga do elétron (C)
AU      = 1.495978707e11     # Unidade Astronômica (m)
ano_luz = 9.4607304725808e15 # Metro por ano-luz

# ── FluxoMatemático ──────────────────────────────────────────────
PHI        = 1.61803398875   # Proporção Áurea
MARC       = 0.54            # Descida céu→terra (aplicação)
JUBILO     = 0.45            # Subida terra→céu (expansão)
DEUS       = 0.18            # Equilíbrio / observação pura
GRATIDAO   = 1.80            # PHI + DEUS = participação consciente ativa
CICLO      = 0.99            # MARC + JUBILO = completude real (não perfeição)

# ── Dados NASA dos Planetas ──────────────────────────────────────
PLANETAS_NASA = {
    'sol': {
        'raio_orbita': 0.0, 'periodo': 1.0, 'excentricidade': 0.0,
        'inclinacao': 7.25,   # Inclinação do equador solar em relação à eclíptica
        'cor': '#FFD700', 'tamanho_relativo': 109.0,
        'elemento': 'Fogo', 'influencia': 'Consciência Central & Fonte',
        'velocidade_orbital': 0.0, 'massa_relativa': 333000.0,
        'temperatura_superficie': 5778, 'luas': [],
        'eh_sol': True
    },
    'mercurio': {
        'raio_orbita': 0.3871, 'periodo': 87.97, 'excentricidade': 0.2056,
        'inclinacao': 7.00, 'cor': '#A0A0A0', 'tamanho_relativo': 0.38,
        'elemento': 'Fogo', 'influencia': 'Comunicação & Intelecto',
        'velocidade_orbital': 47.87, 'massa_relativa': 0.055,
        'temperatura_superficie': 167, 'luas': []
    },
    'venus': {
        'raio_orbita': 0.7233, 'periodo': 224.70, 'excentricidade': 0.0068,
        'inclinacao': 3.39, 'cor': '#FFC649', 'tamanho_relativo': 0.95,
        'elemento': 'Terra', 'influencia': 'Amor & Valores',
        'velocidade_orbital': 35.02, 'massa_relativa': 0.815,
        'temperatura_superficie': 464, 'luas': []
    },
    'terra': {
        'raio_orbita': 1.0000, 'periodo': 365.26, 'excentricidade': 0.0167,
        'inclinacao': 0.00, 'cor': '#1E90FF', 'tamanho_relativo': 1.00,
        'elemento': 'Água', 'influencia': 'Consciência & Manifestação',
        'velocidade_orbital': 29.78, 'massa_relativa': 1.000,
        'temperatura_superficie': 15,
        'luas': [{'nome': 'Lua', 'raio_orbita_planeta': 0.00257, 'periodo_orbital': 27.32,
                  'tamanho_relativo': 0.27, 'cor': '#C0C0C0', 'influencia': 'Emoções & Ciclos',
                  'inclinacao': 5.14}]
    },
    'marte': {
        'raio_orbita': 1.5237, 'periodo': 686.98, 'excentricidade': 0.0934,
        'inclinacao': 1.85, 'cor': '#FF6B6B', 'tamanho_relativo': 0.53,
        'elemento': 'Fogo', 'influencia': 'Ação & Coragem',
        'velocidade_orbital': 24.07, 'massa_relativa': 0.107,
        'temperatura_superficie': -65,
        'luas': [
            {'nome': 'Fobos', 'raio_orbita_planeta': 0.000062, 'periodo_orbital': 0.319,
             'tamanho_relativo': 0.003, 'cor': '#8B7355', 'influencia': 'Urgência'},
            {'nome': 'Deimos', 'raio_orbita_planeta': 0.000157, 'periodo_orbital': 1.263,
             'tamanho_relativo': 0.002, 'cor': '#696969', 'influencia': 'Distanciamento'}
        ]
    },
    'jupiter': {
        'raio_orbita': 5.2028, 'periodo': 4332.59, 'excentricidade': 0.0489,
        'inclinacao': 1.31, 'cor': '#FFA500', 'tamanho_relativo': 11.21,
        'elemento': 'Ar', 'influencia': 'Expansão & Sabedoria',
        'velocidade_orbital': 13.07, 'massa_relativa': 317.8,
        'temperatura_superficie': -110,
        'luas': [
            {'nome': 'Io',        'raio_orbita_planeta': 0.00282, 'periodo_orbital': 1.769,
             'tamanho_relativo': 0.29, 'cor': '#FFD700', 'influencia': 'Transformação'},
            {'nome': 'Europa',    'raio_orbita_planeta': 0.00448, 'periodo_orbital': 3.551,
             'tamanho_relativo': 0.25, 'cor': '#87CEEB', 'influencia': 'Intuição'},
            {'nome': 'Ganimedes', 'raio_orbita_planeta': 0.00716, 'periodo_orbital': 7.155,
             'tamanho_relativo': 0.41, 'cor': '#A0522D', 'influencia': 'Liderança'},
            {'nome': 'Calisto',   'raio_orbita_planeta': 0.01259, 'periodo_orbital': 16.69,
             'tamanho_relativo': 0.38, 'cor': '#8B4513', 'influencia': 'Resiliência'}
        ]
    },
    'saturno': {
        'raio_orbita': 9.5388, 'periodo': 10759.22, 'excentricidade': 0.0565,
        'inclinacao': 2.49, 'cor': '#F0E68C', 'tamanho_relativo': 9.45,
        'elemento': 'Terra', 'influencia': 'Estrutura & Limites',
        'velocidade_orbital': 9.69, 'massa_relativa': 95.2,
        'temperatura_superficie': -140,
        'luas': [
            {'nome': 'Titã',     'raio_orbita_planeta': 0.00817, 'periodo_orbital': 15.945,
             'tamanho_relativo': 0.40, 'cor': '#FFA500', 'influencia': 'Mistério'},
            {'nome': 'Encélado', 'raio_orbita_planeta': 0.00159, 'periodo_orbital': 1.370,
             'tamanho_relativo': 0.04, 'cor': '#FFFFFF', 'influencia': 'Potencial'}
        ]
    },
    'urano': {
        'raio_orbita': 19.1914, 'periodo': 30688.5, 'excentricidade': 0.0461,
        'inclinacao': 0.77, 'cor': '#4ECDC4', 'tamanho_relativo': 4.01,
        'elemento': 'Ar', 'influencia': 'Inovação & Revolução',
        'velocidade_orbital': 6.81, 'massa_relativa': 14.5,
        'temperatura_superficie': -195,
        'luas': [
            {'nome': 'Titânia', 'raio_orbita_planeta': 0.0104, 'periodo_orbital': 8.706,
             'tamanho_relativo': 0.12, 'cor': '#C0C0C0', 'influencia': 'Magia'},
            {'nome': 'Oberon',  'raio_orbita_planeta': 0.0143, 'periodo_orbital': 13.46,
             'tamanho_relativo': 0.12, 'cor': '#808080', 'influencia': 'Segredos'}
        ]
    },
    'netuno': {
        'raio_orbita': 30.0611, 'periodo': 60182.0, 'excentricidade': 0.0097,
        'inclinacao': 1.77, 'cor': '#4169E1', 'tamanho_relativo': 3.88,
        'elemento': 'Água', 'influencia': 'Intuição & Profundidade',
        'velocidade_orbital': 5.43, 'massa_relativa': 17.1,
        'temperatura_superficie': -200,
        'luas': [
            {'nome': 'Tritão', 'raio_orbita_planeta': 0.01574, 'periodo_orbital': 5.877,
             'tamanho_relativo': 0.21, 'cor': '#ADD8E6', 'influencia': 'Retrógrado & Único',
             'retrogrado': True}
        ]
    }
}

# ══════════════════════════════════════════════════════════════════
# FUNÇÃO DE DOWNLOAD DAS EFEMÉRIDES DE440 (NASA JPL)
# ══════════════════════════════════════════════════════════════════
def baixar_de440():
    """Baixa o arquivo de efemérides DE440.bsp se não existir."""
    url = "https://naif.jpl.nasa.gov/pub/naif/generic_kernels/spk/planets/de440.bsp"
    destino = "de440.bsp"
    if not os.path.exists(destino):
        with st.spinner("📡 Baixando efemérides DE440 (NASA JPL) - ~100 MB. Aguarde..."):
            urllib.request.urlretrieve(url, destino)
    return destino

# ══════════════════════════════════════════════════════════════════
# MOTOR ORBITAL KEPLERIANO (NASA-GRADE) – MODO PADRÃO
# ══════════════════════════════════════════════════════════════════
def calcular_posicoes_keplerianas(data_hora):
    """
    Calcula posições 3D de todos os planetas via mecânica Kepleriana.
    O Sol fica em (0,0,0) com vetor de rotação inclinado 7.25° em relação
    ao plano da eclíptica — mostrando a diferença de 'altura/direção'
    do eixo solar em comparação aos planetas.
    """
    epoch_j2000 = datetime(2000, 1, 1, 12, 0, 0)
    dias_julianos = (data_hora - epoch_j2000).total_seconds() / 86400.0

    posicoes = {}

    # ── Sol: posição central + eixo de rotação inclinado ──────────
    inc_sol_rad = math.radians(7.25)
    eixo_sol = np.array([
        math.sin(inc_sol_rad),   # componente X da inclinação
        0.0,
        math.cos(inc_sol_rad)    # componente Z dominante
    ])
    posicoes['sol'] = {
        'posicao': (0.0, 0.0, 0.0),
        'angulo': 0.0,
        'raio_orbita': 0.0,
        'inclinacao': 7.25,
        'cor': PLANETAS_NASA['sol']['cor'],
        'tamanho_relativo': PLANETAS_NASA['sol']['tamanho_relativo'],
        'elemento': PLANETAS_NASA['sol']['elemento'],
        'influencia': PLANETAS_NASA['sol']['influencia'],
        'massa_relativa': PLANETAS_NASA['sol']['massa_relativa'],
        'temperatura_superficie': PLANETAS_NASA['sol']['temperatura_superficie'],
        'velocidade_orbital_km_s': 0.0,
        'eixo_rotacao': eixo_sol.tolist(),
        'eh_sol': True,
        'luas': []
    }

    # ── Planetas: equação de Kepler + rotação 3D ──────────────────
    for nome, cfg in PLANETAS_NASA.items():
        if nome == 'sol':
            continue

        M = (2 * math.pi * dias_julianos / cfg['periodo']) % (2 * math.pi)
        e = cfg['excentricidade']

        E = M
        for _ in range(15):
            dE = (M - (E - e * math.sin(E))) / (1 - e * math.cos(E))
            E += dE
            if abs(dE) < 1e-10:
                break

        a = cfg['raio_orbita']
        x_orb = a * (math.cos(E) - e)
        y_orb = a * math.sqrt(1 - e ** 2) * math.sin(E)

        arg_peri = math.radians(102.9 + 0.001 * dias_julianos / 365.25)
        cos_w, sin_w = math.cos(arg_peri), math.sin(arg_peri)
        x1 = x_orb * cos_w - y_orb * sin_w
        y1 = x_orb * sin_w + y_orb * cos_w

        incl_rad = math.radians(cfg['inclinacao'])
        x_f = x1
        y_f = y1 * math.cos(incl_rad)
        z_f = y1 * math.sin(incl_rad)

        posicoes[nome] = {
            'posicao': (float(x_f), float(y_f), float(z_f)),
            'angulo': float(math.atan2(y_f, x_f) % (2 * math.pi)),
            'raio_orbita': a,
            'excentricidade': e,
            'inclinacao': cfg['inclinacao'],
            'cor': cfg['cor'],
            'tamanho_relativo': cfg['tamanho_relativo'],
            'elemento': cfg['elemento'],
            'influencia': cfg['influencia'],
            'massa_relativa': cfg['massa_relativa'],
            'temperatura_superficie': cfg['temperatura_superficie'],
            'velocidade_orbital_km_s': cfg['velocidade_orbital'],
            'velocidade_angular': 2 * math.pi / cfg['periodo'],
            'periodo_orbital': cfg['periodo'],
            'eh_sol': False,
            'luas': cfg['luas']
        }

    return posicoes, dias_julianos

# ══════════════════════════════════════════════════════════════════
# MOTOR ORBITAL DE ALTA PRECISÃO (N-CORPOS + RELATIVIDADE)
# ══════════════════════════════════════════════════════════════════
def calcular_posicoes_n_corpos(data_hora, incluir_relatividade=True):
    """
    Calcula posições planetárias usando integração de N-corpos com REBOUND + ASSIST.
    Precisão comparável à NASA HORIZONS (DE440).
    """
    if not REBOUND_AVAILABLE:
        st.error("Bibliotecas REBOUND/ASSIST não instaladas. Use o modo Kepleriano.")
        return None, None

    arquivo_bsp = baixar_de440()
    ephem = assist.Ephem(arquivo_bsp, data_hora)
    sim = rebound.Simulation()
    sim.integrator = "ias15"
    sim.dt = 0.1

    assist.add_planets(sim, ephem)

    if incluir_relatividade:
        sim.additional_forces = rebound.InterpolatingGRForce()

    epoch_j2000 = datetime(2000, 1, 1, 12, 0, 0)
    t_segundos = (data_hora - epoch_j2000).total_seconds()
    sim.integrate(t_segundos)

    nomes = ['mercurio', 'venus', 'terra', 'marte', 'jupiter', 'saturno', 'urano', 'netuno']
    posicoes = {}
    for i, nome in enumerate(nomes):
        p = sim.particles[i+1]  # partícula 0 é o Sol
        posicoes[nome] = {
            'posicao': (p.x, p.y, p.z),
            'angulo': float(math.atan2(p.y, p.x) % (2*math.pi)),
            'raio_orbita': np.linalg.norm([p.x, p.y, p.z]),
            'excentricidade': PLANETAS_NASA[nome]['excentricidade'],
            'inclinacao': PLANETAS_NASA[nome]['inclinacao'],
            'cor': PLANETAS_NASA[nome]['cor'],
            'tamanho_relativo': PLANETAS_NASA[nome]['tamanho_relativo'],
            'elemento': PLANETAS_NASA[nome]['elemento'],
            'influencia': PLANETAS_NASA[nome]['influencia'],
            'massa_relativa': PLANETAS_NASA[nome]['massa_relativa'],
            'temperatura_superficie': PLANETAS_NASA[nome]['temperatura_superficie'],
            'velocidade_orbital_km_s': np.linalg.norm([p.vx, p.vy, p.vz]) * 1e-3,
            'velocidade_angular': 0.0,
            'periodo_orbital': PLANETAS_NASA[nome]['periodo'],
            'eh_sol': False,
            'luas': PLANETAS_NASA[nome]['luas']
        }

    # Sol
    posicoes['sol'] = {
        'posicao': (0.0, 0.0, 0.0),
        'angulo': 0.0,
        'raio_orbita': 0.0,
        'inclinacao': 7.25,
        'cor': PLANETAS_NASA['sol']['cor'],
        'tamanho_relativo': PLANETAS_NASA['sol']['tamanho_relativo'],
        'elemento': PLANETAS_NASA['sol']['elemento'],
        'influencia': PLANETAS_NASA['sol']['influencia'],
        'massa_relativa': PLANETAS_NASA['sol']['massa_relativa'],
        'temperatura_superficie': PLANETAS_NASA['sol']['temperatura_superficie'],
        'velocidade_orbital_km_s': 0.0,
        'eixo_rotacao': [0.0, 0.0, 1.0],
        'eh_sol': True,
        'luas': []
    }

    dias_julianos = (data_hora - epoch_j2000).total_seconds() / 86400.0
    return posicoes, dias_julianos

# ══════════════════════════════════════════════════════════════════
# FUNÇÕES AUXILIARES (ALINHAMENTOS, TECIDO, ETC.) – MANTIDAS COMO ESTAVAM
# ══════════════════════════════════════════════════════════════════

def calcular_alinhamentos(posicoes):
    """Detecta aspectos astrológicos/astronômicos entre pares de planetas."""
    pares = [
        ('mercurio', 'venus'),   ('venus', 'terra'),    ('terra', 'marte'),
        ('marte', 'jupiter'),    ('jupiter', 'saturno'),('saturno', 'urano'),
        ('urano', 'netuno'),     ('mercurio', 'marte'),  ('venus', 'jupiter'),
        ('terra', 'saturno'),    ('marte', 'urano'),     ('jupiter', 'netuno'),
        ('venus', 'saturno'),    ('terra', 'jupiter')
    ]

    aspectos = {
        'Conjunção':  (0,   2.0, 0.95, '#FFD700'),
        'Sextil':     (60,  3.0, 0.75, '#00FF88'),
        'Quadratura': (90,  3.0, 0.85, '#FF4444'),
        'Trígono':    (120, 3.0, 0.90, '#4488FF'),
        'Quincunce':  (150, 2.5, 0.70, '#FF88FF'),
        'Oposição':   (180, 2.0, 0.88, '#FF8800'),
    }

    alinhamentos = []
    for p1, p2 in pares:
        if p1 not in posicoes or p2 not in posicoes:
            continue
        v1 = np.array(posicoes[p1]['posicao'])
        v2 = np.array(posicoes[p2]['posicao'])
        n1, n2 = np.linalg.norm(v1), np.linalg.norm(v2)
        if n1 < 1e-12 or n2 < 1e-12:
            continue

        cos_ang = np.clip(np.dot(v1, v2) / (n1 * n2), -1.0, 1.0)
        ang_deg = math.degrees(math.acos(cos_ang))

        for tipo, (alvo, tol, intens, cor) in aspectos.items():
            if abs(ang_deg - alvo) <= tol:
                e1 = posicoes[p1]['elemento']
                e2 = posicoes[p2]['elemento']
                compat = 'Neutra'
                if (e1, e2) in [('Fogo','Ar'), ('Ar','Fogo'), ('Água','Terra'), ('Terra','Água')]:
                    compat = 'Alta'
                elif e1 == e2:
                    compat = 'Média'
                elif (e1, e2) in [('Fogo','Água'), ('Água','Fogo'), ('Ar','Terra'), ('Terra','Ar')]:
                    compat = 'Baixa'

                alinhamentos.append({
                    'planeta1': p1, 'planeta2': p2, 'tipo': tipo,
                    'angulo_graus': ang_deg, 'intensidade': intens,
                    'compatibilidade': compat, 'cor': cor,
                    'distancia_ua': np.linalg.norm(v2 - v1)
                })
                break
    return alinhamentos

# ══════════════════════════════════════════════════════════════════
# TECIDO ESPAÇO-TEMPO 3D COM MASSA PROPORCIONAL + DIREÇÃO SOLAR
# ══════════════════════════════════════════════════════════════════
def gerar_tecido_espaco_tempo_3d(posicoes, modelo="FluxoMatemático"):
    """
    Gera o tecido espaço-tempo 3D mostrando:
    - Curvatura proporcional à MASSA de cada corpo
    - O Sol com deformação central profunda + seta de eixo inclinado 7.25°
    - Planetas como poços gravitacionais de profundidade correta
    - Curvatura via soma de potenciais gravitacionais normalizados
    """
    # Grid para o tecido (em UA)
    resolucao = 80
    x_range = np.linspace(-12, 12, resolucao)
    y_range = np.linspace(-12, 12, resolucao)
    X, Y = np.meshgrid(x_range, y_range)
    Z = np.zeros_like(X)

    # Soma dos potenciais gravitacionais de todos os corpos
    for nome, dados in posicoes.items():
        px, py, _ = dados['posicao']
        massa_rel = dados['massa_relativa']

        # Raio de influência escalado
        dx = X - px
        dy = Y - py
        r = np.sqrt(dx**2 + dy**2)
        r_safe = np.maximum(r, 0.15)  # evitar singularidade

        # Potencial: − G·M / r  (normalizado)
        if nome == 'sol':
            # Sol tem massa 333.000× Terra → deformação dominante
            pot = -massa_rel / (r_safe * 3000)
        else:
            pot = -massa_rel / (r_safe * 800)

        # Aplicar pilares FluxoMatemático ao potencial
        if modelo == "FluxoMatemático":
            pot = pot * GRATIDAO * CICLO

        Z += pot

    # Normalizar: tecido entre -5 e 0
    Z_min = Z.min()
    Z_max = Z.max()
    if abs(Z_max - Z_min) > 1e-10:
        Z = (Z - Z_max) / (Z_max - Z_min) * -5.0

    fig = go.Figure()

    # ── Superfície do tecido ──────────────────────────────────────
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z,
        colorscale=[
            [0.0,  'rgb(5,5,30)'],
            [0.2,  'rgb(20,30,80)'],
            [0.4,  'rgb(60,10,120)'],
            [0.6,  'rgb(120,20,80)'],
            [0.8,  'rgb(200,100,20)'],
            [1.0,  'rgb(255,220,50)']
        ],
        opacity=0.85,
        name='Tecido Espaço-Tempo',
        showscale=True,
        colorbar=dict(
            title=dict(text='Curvatura', font=dict(color='white')),
            tickfont=dict(color='white')
        )
    ))

    # ── Sol: marcador + eixo de rotação inclinado 7.25° ──────────
    sol_z = float(np.interp(0, x_range, Z[resolucao//2, :]))
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[sol_z],
        mode='markers+text',
        marker=dict(size=20, color='#FFD700', symbol='circle',
                    line=dict(color='#FF8C00', width=3)),
        text=['☀ SOL'], textposition='top center',
        textfont=dict(color='#FFD700', size=13),
        name='Sol'
    ))

    # Eixo de rotação solar (seta inclinada 7.25°)
    comprimento_eixo = 2.5
    inc_sol = math.radians(7.25)
    eixo_x = [0, comprimento_eixo * math.sin(inc_sol)]
    eixo_y = [0, 0]
    eixo_z = [sol_z, sol_z + comprimento_eixo * math.cos(inc_sol)]

    fig.add_trace(go.Scatter3d(
        x=eixo_x, y=eixo_y, z=eixo_z,
        mode='lines+text',
        line=dict(color='#FF4500', width=6),
        text=['', f'Eixo Solar\n7.25°'],
        textfont=dict(color='#FF4500', size=10),
        name='Eixo Rotação Solar (7.25°)'
    ))

    # ── Planetas sobre o tecido ───────────────────────────────────
    planetas_visiveis = [n for n in posicoes if n != 'sol' and
                         abs(posicoes[n]['posicao'][0]) < 12 and
                         abs(posicoes[n]['posicao'][1]) < 12]

    for nome in planetas_visiveis:
        dados = posicoes[nome]
        px, py, _ = dados['posicao']

        # Interpolar Z do tecido na posição do planeta
        ix = int(np.interp(px, x_range, range(resolucao)))
        iy = int(np.interp(py, y_range, range(resolucao)))
        ix = max(0, min(resolucao - 1, ix))
        iy = max(0, min(resolucao - 1, iy))
        pz = float(Z[iy, ix])

        tamanho = max(6, min(18, dados['tamanho_relativo'] * 6))
        fig.add_trace(go.Scatter3d(
            x=[px], y=[py], z=[pz],
            mode='markers+text',
            marker=dict(size=tamanho, color=dados['cor'],
                        line=dict(color='white', width=1), opacity=0.9),
            text=[nome.capitalize()],
            textposition='top center',
            textfont=dict(color=dados['cor'], size=9),
            name=nome.capitalize()
        ))

        # Linha vertical ao fundo (mostra profundidade real no tecido)
        fig.add_trace(go.Scatter3d(
            x=[px, px], y=[py, py], z=[pz, pz - 0.3],
            mode='lines',
            line=dict(color=dados['cor'], width=2, dash='dot'),
            showlegend=False
        ))

    fig.update_layout(
        title=dict(text='🌌 Tecido Espaço-Tempo — Curvatura por Massa (UA)', x=0.5,
                   font=dict(color='white', size=16)),
        scene=dict(
            xaxis=dict(title='X (UA)', backgroundcolor='rgb(5,5,20)',
                       gridcolor='rgba(100,100,200,0.3)', color='white'),
            yaxis=dict(title='Y (UA)', backgroundcolor='rgb(5,5,20)',
                       gridcolor='rgba(100,100,200,0.3)', color='white'),
            zaxis=dict(title='Curvatura Gravitacional', backgroundcolor='rgb(5,5,20)',
                       gridcolor='rgba(100,100,200,0.2)', color='white'),
            bgcolor='rgb(5,5,20)',
            camera=dict(eye=dict(x=1.5, y=1.5, z=1.0))
        ),
        paper_bgcolor='rgb(5,5,20)',
        plot_bgcolor='rgb(5,5,20)',
        font=dict(color='white'),
        height=650,
        margin=dict(l=0, r=0, t=50, b=0),
        showlegend=False
    )
    return fig


# ══════════════════════════════════════════════════════════════════
# MAPA SOLAR SISTEMA — VISTA ORBITAL 3D
# ══════════════════════════════════════════════════════════════════
def gerar_sistema_solar_3d(posicoes, dias_julianos):
    """
    Renderiza o sistema solar em 3D com:
    - Órbitas elípticas reais + inclinação orbital
    - Planetas nas posições calculadas
    - Sol com eixo de rotação diferenciado (7.25°)
    - Escala logarítmica opcional para exibir planetas externos
    """
    fig = go.Figure()

    # Fundo estelar simulado
    n_estrelas = 300
    sx = np.random.uniform(-35, 35, n_estrelas)
    sy = np.random.uniform(-35, 35, n_estrelas)
    sz = np.random.uniform(-5, 5, n_estrelas)
    fig.add_trace(go.Scatter3d(
        x=sx, y=sy, z=sz, mode='markers',
        marker=dict(size=0.8, color='white', opacity=0.4),
        name='Estrelas', showlegend=False
    ))

    # Órbitas elípticas para cada planeta
    for nome, cfg in PLANETAS_NASA.items():
        if nome == 'sol':
            continue
        a = cfg['raio_orbita']
        e = cfg['excentricidade']
        incl = math.radians(cfg['inclinacao'])
        theta = np.linspace(0, 2 * math.pi, 200)
        # Órbita no plano orbital
        r = a * (1 - e**2) / (1 + e * np.cos(theta))
        x_orb = r * np.cos(theta)
        y_orb = r * np.sin(theta)
        # Inclinação
        x_3d = x_orb
        y_3d = y_orb * math.cos(incl)
        z_3d = y_orb * math.sin(incl)

        fig.add_trace(go.Scatter3d(
            x=x_3d, y=y_3d, z=z_3d, mode='lines',
            line=dict(color=cfg['cor'], width=1.5, dash='dot' if cfg['raio_orbita'] > 5 else 'solid'),
            opacity=0.4, name=f'Órbita {nome.capitalize()}', showlegend=False
        ))

    # Sol com eixo inclinado
    inc_sol = math.radians(7.25)
    comp = 1.8
    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0], mode='markers+text',
        marker=dict(size=22, color='#FFD700', symbol='circle',
                    line=dict(color='#FF8C00', width=4)),
        text=['☀ SOL'], textposition='top center',
        textfont=dict(color='#FFD700', size=14),
        name='Sol'
    ))
    # Eixo de rotação solar (7.25° de inclinação — diferente dos planetas)
    fig.add_trace(go.Scatter3d(
        x=[-comp * math.sin(inc_sol), comp * math.sin(inc_sol)],
        y=[0, 0],
        z=[-comp * math.cos(inc_sol), comp * math.cos(inc_sol)],
        mode='lines+text',
        line=dict(color='#FF6600', width=5),
        text=['', 'Eixo Sol 7.25°'],
        textfont=dict(color='#FF6600', size=9),
        name='Eixo Rotação Solar'
    ))

    # Planetas
    planetas_nomes = list(posicoes.keys())
    for nome in planetas_nomes:
        if nome == 'sol':
            continue
        dados = posicoes[nome]
        px, py, pz = dados['posicao']
        tamanho = max(5, min(20, dados['tamanho_relativo'] * 5))

        # Eixo de rotação do planeta (inclinação axial simplificada)
        inc_ax = math.radians(dados['inclinacao'])
        ea = 0.6
        fig.add_trace(go.Scatter3d(
            x=[px - ea * math.sin(inc_ax), px + ea * math.sin(inc_ax)],
            y=[py, py],
            z=[pz - ea * math.cos(inc_ax), pz + ea * math.cos(inc_ax)],
            mode='lines',
            line=dict(color='rgba(180,180,255,0.5)', width=2),
            showlegend=False
        ))

        fig.add_trace(go.Scatter3d(
            x=[px], y=[py], z=[pz],
            mode='markers+text',
            marker=dict(size=tamanho, color=dados['cor'],
                        line=dict(color='white', width=1.5), opacity=1.0),
            text=[f'{nome.capitalize()}\n{dados["influencia"]}'],
            textposition='top center',
            textfont=dict(color=dados['cor'], size=8),
            name=nome.capitalize()
        ))

    fig.update_layout(
        title=dict(text='🪐 Sistema Solar — Posições Orbitais 3D (Data Atual)',
                   x=0.5, font=dict(color='white', size=15)),
        scene=dict(
            xaxis=dict(title='X (UA)', backgroundcolor='rgb(3,3,15)',
                       gridcolor='rgba(80,80,160,0.25)', color='white'),
            yaxis=dict(title='Y (UA)', backgroundcolor='rgb(3,3,15)',
                       gridcolor='rgba(80,80,160,0.25)', color='white'),
            zaxis=dict(title='Z (UA)', backgroundcolor='rgb(3,3,15)',
                       gridcolor='rgba(80,80,160,0.15)', color='white'),
            bgcolor='rgb(3,3,15)',
            camera=dict(eye=dict(x=1.2, y=1.2, z=0.8))
        ),
        paper_bgcolor='rgb(3,3,15)',
        font=dict(color='white'),
        height=650,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    return fig


# ══════════════════════════════════════════════════════════════════
# MÓDULO 1 — BURACOS NEGROS E ANOMALIAS
# ══════════════════════════════════════════════════════════════════
def modulo_buracos_negros():
    st.markdown("## ⚫ Buracos Negros e Anomalias Gravitacionais")
    st.markdown("""
    Simulação gravitacional com mecânica Newtoniana + relatividade geral aproximada.
    A curvatura do espaço-tempo é calculada via potencial de Schwarzschild.
    """)

    col1, col2 = st.columns(2)
    with col1:
        massa_bn = st.number_input("Massa do Buraco Negro (M☉)", value=10.0, min_value=1.0,
                                   help="Em massas solares. Sol = 1. Buracos negros estelares: 5-100 M☉")
        massa_bn_kg = massa_bn * 1.989e30  # conversão para kg

    with col2:
        modelo = st.selectbox("Modelo Físico", ["Clássico (Newton)", "FluxoMatemático (Relativístico)"])
        num_passos = st.slider("Resolução da Simulação", 500, 5000, 2000, 250)

    perturbacao = st.slider("Perturbação por Matéria Escura", 0.0, 0.15, 0.02, 0.005)

    # ── Raio de Schwarzschild ──────────────────────────────────────
    rs = 2 * G * massa_bn_kg / c**2
    st.metric("Raio de Schwarzschild", f"{rs/1000:.2f} km",
              help="Abaixo deste raio, nem a luz escapa")

    # ── Simulação de órbita ────────────────────────────────────────
    if st.button("⚡ Simular Órbita", use_container_width=True):
        with st.spinner("Calculando trajetória orbital..."):
            posicao = np.array([1.0, 0.0])
            velocidade = np.array([0.0, np.sqrt(G * massa_bn_kg / AU)])
            trajetoria = []
            energia = []
            dt = 0.05
            massa_planeta_kg = 5.972e24

            for _ in range(num_passos):
                r = np.linalg.norm(posicao)
                r3 = r**3

                if modelo == "FluxoMatemático (Relativístico)":
                    # Correção pós-Newtoniana (1PN): precession relativístico
                    fator_rel = 1 + 3 * (G * massa_bn_kg) / (r * c**2)
                    aceleracao = -G * massa_bn_kg / r3 * posicao * fator_rel
                    aceleracao *= GRATIDAO * CICLO
                else:
                    aceleracao = -G * massa_bn_kg / r3 * posicao

                aceleracao += perturbacao * np.random.normal(0, 1, 2) * G * massa_bn_kg / (r3 * 10)
                velocidade += aceleracao * dt
                posicao += velocidade * dt
                trajetoria.append(posicao.copy())
                ec = 0.5 * massa_planeta_kg * np.linalg.norm(velocidade)**2
                ep = -G * massa_bn_kg * massa_planeta_kg / (np.linalg.norm(posicao) * AU)
                energia.append(ec + ep)

        T = np.array(trajetoria)
        E = np.array(energia)

        # Gráfico órbita 3D
        z_spiral = np.linspace(0, 2, num_passos)
        if modelo == "FluxoMatemático (Relativístico)":
            z_spiral = z_spiral * MARC  # precessão adicional

        fig_orb = go.Figure()
        fig_orb.add_trace(go.Scatter3d(
            x=T[:, 0], y=T[:, 1], z=z_spiral,
            mode='lines',
            line=dict(color=np.arange(num_passos), colorscale='Plasma', width=2),
            name='Trajetória'
        ))
        fig_orb.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[z_spiral[0]],
            mode='markers', marker=dict(size=15, color='black', symbol='circle'),
            name='Buraco Negro'
        ))
        fig_orb.update_layout(
            title='Órbita em Campo Gravitacional Intenso',
            scene=dict(bgcolor='rgb(5,5,15)',
                       xaxis=dict(color='white'), yaxis=dict(color='white'), zaxis=dict(color='white')),
            paper_bgcolor='rgb(5,5,15)', font=dict(color='white'), height=500
        )
        st.plotly_chart(fig_orb, use_container_width=True)

        # Gráfico energia
        fig_e = go.Figure()
        fig_e.add_trace(go.Scatter(y=E, mode='lines', name='Energia Total (J)',
                                   line=dict(color='#00FF88', width=2)))
        fig_e.update_layout(
            title='Conservação de Energia Orbital',
            xaxis_title='Passo de Tempo', yaxis_title='Energia (J)',
            paper_bgcolor='rgb(5,5,15)', plot_bgcolor='rgb(10,10,25)',
            font=dict(color='white'), height=300
        )
        st.plotly_chart(fig_e, use_container_width=True)

        # Distorção espaço-tempo local
        st.markdown("### 🌀 Distorção Local do Espaço-Tempo")
        xg = np.linspace(-3, 3, 60)
        yg = np.linspace(-3, 3, 60)
        Xg, Yg = np.meshgrid(xg, yg)
        Rg = np.sqrt(Xg**2 + Yg**2)
        Rg = np.maximum(Rg, 0.3)
        rs_norm = (rs / AU)
        Zg = -rs_norm / Rg
        if modelo == "FluxoMatemático (Relativístico)":
            Zg *= GRATIDAO

        fig_st = go.Figure(data=[go.Surface(
            x=Xg, y=Yg, z=Zg,
            colorscale='Inferno', opacity=0.9, showscale=False
        )])
        fig_st.update_layout(
            title='Curvatura do Espaço-Tempo (escala UA)',
            scene=dict(bgcolor='rgb(5,5,15)',
                       xaxis=dict(color='white', title='X (UA)'),
                       yaxis=dict(color='white', title='Y (UA)'),
                       zaxis=dict(color='white', title='Curvatura')),
            paper_bgcolor='rgb(5,5,15)', font=dict(color='white'), height=450
        )
        st.plotly_chart(fig_st, use_container_width=True)


# ══════════════════════════════════════════════════════════════════
# MÓDULO 2 — CAPTAÇÃO E TRANSFORMAÇÃO DE ENERGIA
# ══════════════════════════════════════════════════════════════════
def modulo_captacao_energia():
    st.markdown("## ⚡ Captação e Transformação de Energia")

    col1, col2 = st.columns(2)
    with col1:
        frequencia = st.number_input("Frequência do Fluxo (Hz)", value=432.0, min_value=0.001,
                                     help="432 Hz = frequência natural harmônica")
        potencia = st.number_input("Potência (W)", value=200.0, min_value=0.0)
        resistencia = st.number_input("Resistência Ω", value=3.0, min_value=0.001)

    with col2:
        angulo = st.slider("Ângulo do Fluxo (°)", 0, 360, 130)
        fator_alpha = st.slider("Fator α de Ajuste", -50.0, 50.0, -23.8, 0.1)
        aplicar_fluxo = st.checkbox("Aplicar Constantes FluxoMatemático", value=True)

    # ── Cálculos quânticos ────────────────────────────────────────
    E_foton = h_planck * frequencia
    V_fluxo = E_foton / e_carga
    I_fluxo = potencia / (V_fluxo * abs(math.cos(math.radians(angulo))) + 1e-30)
    E_bobina = 0.5 * 1e-3 * (frequencia / resistencia)**2
    E_perdida = E_foton * abs(fator_alpha) * resistencia
    E_sing = E_foton * (1 + abs(fator_alpha)) / resistencia

    # Aplicar FluxoMatemático
    if aplicar_fluxo:
        E_bobina_aureo = E_bobina * PHI * GRATIDAO
        E_sing_aureo = E_sing * CICLO
        E_foton_aureo = E_foton * MARC / JUBILO  # razão expansão/aplicação
    else:
        E_bobina_aureo = E_bobina
        E_sing_aureo = E_sing
        E_foton_aureo = E_foton

    # Exibição
    cols = st.columns(4)
    metricas = [
        ("Energia Fóton", f"{E_foton:.3e} J"),
        ("Tensão Fluxo", f"{V_fluxo:.3e} V"),
        ("Corrente Fluxo", f"{I_fluxo:.3e} A"),
        ("Bobina Áurea", f"{E_bobina_aureo:.3e} J"),
    ]
    for col, (label, val) in zip(cols, metricas):
        col.metric(label, val)

    st.caption(f"E. Singularidade: {E_sing_aureo:.3e} J  |  E. Perdida: {E_perdida:.3e} J")

    # ── Harmônicos áureos ─────────────────────────────────────────
    num_harm = st.slider("Número de Harmônicos Áureos", 5, 20, 10)
    harmonicos = [frequencia * (PHI ** i) for i in range(num_harm)]

    fig_harm = go.Figure()
    t = np.linspace(0, 0.01, 2000)
    sinal_soma = np.zeros_like(t)
    for i, f_h in enumerate(harmonicos):
        amplitude = 1.0 / (PHI ** i)
        sinal = amplitude * np.sin(2 * math.pi * f_h * t)
        sinal_soma += sinal
        if i < 5:  # mostrar só os primeiros
            fig_harm.add_trace(go.Scatter(
                x=t * 1000, y=sinal,
                mode='lines', name=f'H{i+1} = {f_h:.1f} Hz',
                line=dict(width=1.5, dash='dot'), opacity=0.5
            ))
    fig_harm.add_trace(go.Scatter(
        x=t * 1000, y=sinal_soma, mode='lines',
        name='Sinal Resultante', line=dict(color='#FFD700', width=3)
    ))
    fig_harm.update_layout(
        title='Harmônicos Áureos — φⁿ × f₀',
        xaxis_title='Tempo (ms)', yaxis_title='Amplitude',
        paper_bgcolor='rgb(5,5,15)', plot_bgcolor='rgb(10,10,25)',
        font=dict(color='white'), height=400, legend=dict(bgcolor='rgba(0,0,0,0.5)')
    )
    st.plotly_chart(fig_harm, use_container_width=True)

    # ── Campo energético 3D ───────────────────────────────────────
    st.markdown("### 🌊 Campo de Energia no Espaço-Tempo")
    x = np.linspace(-10, 10, 50)
    y = np.linspace(-10, 10, 50)
    Xg, Yg = np.meshgrid(x, y)
    R = np.sqrt(Xg**2 + Yg**2)
    Z_campo = np.sin(R * frequencia / 100) * np.exp(-R / 8) * I_fluxo

    fig_campo = go.Figure(data=[go.Surface(
        x=Xg, y=Yg, z=Z_campo,
        colorscale='Plasma', opacity=0.85, showscale=True,
        colorbar=dict(
            title=dict(text='Intensidade', font=dict(color='white')),
            tickfont=dict(color='white')
        )
    )])
    fig_campo.update_layout(
        title='Campo de Energia — Bobina Áurea 3D',
        scene=dict(bgcolor='rgb(5,5,15)',
                   xaxis=dict(color='white', title='X (m)'),
                   yaxis=dict(color='white', title='Y (m)'),
                   zaxis=dict(color='white', title='Energia (J)')),
        paper_bgcolor='rgb(5,5,15)', font=dict(color='white'), height=500
    )
    st.plotly_chart(fig_campo, use_container_width=True)


# ══════════════════════════════════════════════════════════════════
# MÓDULO 3 — SISTEMA PLANETÁRIO E ESPAÇO-TEMPO
# ══════════════════════════════════════════════════════════════════
# ══════════════════════════════════════════════════════════════════
# MÓDULO 3 — SISTEMA PLANETÁRIO E ESPAÇO-TEMPO (ATUALIZADO)
# ══════════════════════════════════════════════════════════════════
def modulo_sistema_planetario():
    st.markdown("## 🪐 Sistema Planetário e Espaço-Tempo")

    col1, col2 = st.columns(2)
    with col1:
        data_calc = st.date_input("Data de Referência", value=datetime.now().date())
    with col2:
        hora_calc = st.time_input("Hora (UTC)", value=datetime.now().time())
        modelo_st = st.selectbox("Modelo do Espaço-Tempo", ["FluxoMatemático", "Clássico (Newton)"])

    data_hora = datetime.combine(data_calc, hora_calc)

    # Escolha do método de cálculo
    metodo = st.radio(
        "⚙️ Método de cálculo orbital:",
        ["Kepleriano (rápido, educacional)", "N-Corpos + Relatividade (alta precisão, requer REBOUND)"],
        index=0,
        help="O método N-Corpos utiliza efemérides DE440 da NASA e integração numérica completa."
    )

    if "N-Corpos" in metodo and not REBOUND_AVAILABLE:
        st.warning("Bibliotecas científicas (rebound, assist) não instaladas. Usando método Kepleriano.")
        metodo = "Kepleriano"

    with st.spinner("Calculando posições planetárias..."):
        if "N-Corpos" in metodo:
            posicoes, dias_j2000 = calcular_posicoes_n_corpos(data_hora, incluir_relatividade=True)
            if posicoes is None:
                st.error("Falha no cálculo N-Corpos. Usando método Kepleriano.")
                posicoes, dias_j2000 = calcular_posicoes_keplerianas(data_hora)
        else:
            posicoes, dias_j2000 = calcular_posicoes_keplerianas(data_hora)

        alinhamentos = calcular_alinhamentos(posicoes)

    st.success(f"✅ Calculado para J2000+{dias_j2000:.2f} dias | Método: {metodo} | {len(alinhamentos)} aspectos detectados")

    # Tabs de visualização (as mesmas de antes)
    tab1, tab2, tab3 = st.tabs(["🌌 Tecido Espaço-Tempo", "🪐 Órbitas 3D", "📊 Alinhamentos"])

    with tab1:
        st.markdown("""
        **Visualização do tecido espaço-tempo:** a profundidade de cada poço é proporcional
        à massa do corpo celeste. O **Sol** cria a maior deformação (≈333.000× a Terra).
        O eixo laranja indica a inclinação real de **7.25°** do equador solar em relação
        à eclíptica — diferente de todos os planetas.
        """)
        fig_st = gerar_tecido_espaco_tempo_3d(posicoes, modelo_st)
        st.plotly_chart(fig_st, use_container_width=True)

    with tab2:
        fig_sol = gerar_sistema_solar_3d(posicoes, dias_j2000)
        st.plotly_chart(fig_sol, use_container_width=True)

        # Tabela de posições
        rows = []
        for nome, dados in posicoes.items():
            px, py, pz = dados['posicao']
            r = math.sqrt(px**2 + py**2 + pz**2)
            rows.append({
                'Corpo': nome.capitalize(),
                'X (UA)': f"{px:.4f}",
                'Y (UA)': f"{py:.4f}",
                'Z (UA)': f"{pz:.5f}",
                'Dist. Sol (UA)': f"{r:.4f}",
                'Inclinação (°)': f"{dados['inclinacao']:.2f}",
                'Influência': dados['influencia']
            })
        st.dataframe(pd.DataFrame(rows), use_container_width=True)

    with tab3:
        if alinhamentos:
            df_al = pd.DataFrame(alinhamentos)
            fig_al = go.Figure()
            for tipo in df_al['tipo'].unique():
                sub = df_al[df_al['tipo'] == tipo]
                fig_al.add_trace(go.Bar(
                    x=[f"{r['planeta1'].capitalize()} - {r['planeta2'].capitalize()}" for _, r in sub.iterrows()],
                    y=sub['intensidade'],
                    name=tipo,
                    marker_color=sub['cor'].iloc[0]
                ))
            fig_al.update_layout(
                title='Intensidade dos Aspectos Planetários',
                xaxis_title='Par Planetário', yaxis_title='Intensidade (0-1)',
                paper_bgcolor='rgb(5,5,15)', plot_bgcolor='rgb(10,10,25)',
                font=dict(color='white'), barmode='group', height=400
            )
            st.plotly_chart(fig_al, use_container_width=True)

            df_show = df_al[['planeta1', 'planeta2', 'tipo', 'angulo_graus', 'intensidade',
                              'compatibilidade', 'distancia_ua']].copy()
            df_show.columns = ['Planeta 1', 'Planeta 2', 'Aspecto', 'Ângulo (°)',
                                'Intensidade', 'Compatibilidade', 'Distância (UA)']
            df_show['Ângulo (°)'] = df_show['Ângulo (°)'].round(2)
            df_show['Intensidade'] = df_show['Intensidade'].round(3)
            df_show['Distância (UA)'] = df_show['Distância (UA)'].round(4)
            st.dataframe(df_show, use_container_width=True)
        else:
            st.info("Nenhum aspecto significativo detectado para esta data/hora.")
            
# ══════════════════════════════════════════════════════════════════
# MÓDULO 4 — PLANETAS, LUAS E ESPAÇO-TEMPO (VISÃO DETALHADA)
# ══════════════════════════════════════════════════════════════════
def modulo_planeta_detalhado():
    st.markdown("## 🪐 Planetas, Luas e Espaço-Tempo")
    st.markdown("Selecione um planeta para explorar seu sistema de luas e características únicas.")

    # Lista de planetas (todos, exceto o Sol)
    planetas_disponiveis = [nome.capitalize() for nome in PLANETAS_NASA.keys() if nome != 'sol']
    planeta_escolhido_nome = st.selectbox("🌍 Escolha o planeta:", planetas_disponiveis)
    planeta_nome = planeta_escolhido_nome.lower()

    cfg = PLANETAS_NASA[planeta_nome]

    col1, col2 = st.columns(2)
    with col1:
        data_calc = st.date_input("Data de observação", value=datetime.now().date(), key="planeta_data")
    with col2:
        hora_calc = st.time_input("Hora (UTC)", value=datetime.now().time(), key="planeta_hora")
        mostrar_aneis = st.checkbox("Mostrar anéis (se existirem)", value=True)
        mostrar_asteroides = st.checkbox("Mostrar cinturão de asteroides", value=True)
        mostrar_campo = st.checkbox("Mostrar linhas de campo magnético", value=False)

    data_hora = datetime.combine(data_calc, hora_calc)

    # Calcular posições para obter as luas
    with st.spinner(f"Calculando órbitas das luas de {planeta_escolhido_nome}..."):
        posicoes, dias_j2000 = calcular_posicoes_orbitais(data_hora)
        luas_info = cfg['luas']

        # Calcular posições das luas em relação ao planeta (coordenadas locais)
        luas_pos = {}
        horas = dias_j2000 * 24
        for lua in luas_info:
            periodo_horas = lua['periodo_orbital'] * 24
            ang_lua = (horas / periodo_horas) * 2 * math.pi
            if lua.get('retrogrado', False):
                ang_lua = -ang_lua
            incl_rad = math.radians(lua.get('inclinacao', 0.0))
            r_lua = lua['raio_orbita_planeta']  # em UA

            x_rel = r_lua * math.cos(ang_lua) * math.cos(incl_rad)
            y_rel = r_lua * math.sin(ang_lua) * math.cos(incl_rad)
            z_rel = r_lua * math.sin(incl_rad) * math.sin(ang_lua)

            luas_pos[lua['nome']] = {
                'pos_rel': (x_rel, y_rel, z_rel),
                'distancia': r_lua,
                'tamanho': lua['tamanho_relativo'],
                'cor': lua['cor'],
                'influencia': lua['influencia'],
                'periodo': lua['periodo_orbital']
            }

    # ── Visualização 3D ───────────────────────────────────────────
    fig = go.Figure()

    # Fundo estelar
    n_estrelas = 400
    fig.add_trace(go.Scatter3d(
        x=np.random.uniform(-5, 5, n_estrelas),
        y=np.random.uniform(-5, 5, n_estrelas),
        z=np.random.uniform(-5, 5, n_estrelas),
        mode='markers',
        marker=dict(size=0.6, color='white', opacity=0.7),
        name='Estrelas', showlegend=False
    ))

    # Cinturão de asteroides (entre Marte e Júpiter) - mostrado como pano de fundo para todos os planetas
    if mostrar_asteroides:
        n_ast = 800
        raio_ast = np.random.uniform(1.8, 3.2, n_ast)   # UA
        ang_ast = np.random.uniform(0, 2*np.pi, n_ast)
        z_ast = np.random.uniform(-0.3, 0.3, n_ast)
        x_ast = raio_ast * np.cos(ang_ast)
        y_ast = raio_ast * np.sin(ang_ast)
        fig.add_trace(go.Scatter3d(
            x=x_ast, y=y_ast, z=z_ast,
            mode='markers',
            marker=dict(size=1.2, color='#A0522D', opacity=0.5),
            name='Cinturão de Asteroides', showlegend=True
        ))

    # Planeta central
    tamanho_planeta = max(10, min(30, cfg['tamanho_relativo'] * 3.0))
    # Para planetas gasosos, adicionar um halo atmosférico
    if planeta_nome in ['jupiter', 'saturno', 'urano', 'netuno']:
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0],
            mode='markers',
            marker=dict(size=tamanho_planeta*1.4, color=cfg['cor'], opacity=0.15, sizemode='diameter'),
            showlegend=False
        ))

    fig.add_trace(go.Scatter3d(
        x=[0], y=[0], z=[0],
        mode='markers+text',
        marker=dict(
            size=tamanho_planeta,
            color=cfg['cor'],
            line=dict(color='white', width=1.8)
        ),
        text=[planeta_escolhido_nome],
        textposition='top center',
        textfont=dict(color=cfg['cor'], size=14, family='Arial Black'),
        name=planeta_escolhido_nome
    ))

    # --- EFEITOS ESPECÍFICOS DE CADA PLANETA ---
    # Mercúrio: crateras
    if planeta_nome == 'mercurio':
        for _ in range(40):
            ang = np.random.uniform(0, 2*np.pi)
            rad = np.random.uniform(0.2, 0.9)
            x_c = rad * np.cos(ang)
            y_c = rad * np.sin(ang)
            z_c = np.random.uniform(-0.2, 0.2)
            fig.add_trace(go.Scatter3d(
                x=[x_c], y=[y_c], z=[z_c],
                mode='markers',
                marker=dict(size=np.random.uniform(1,3), color='#505050', symbol='circle-open'),
                showlegend=False
            ))

    # Vênus: atmosfera densa (nuvens amareladas)
    if planeta_nome == 'venus':
        for _ in range(30):
            ang = np.random.uniform(0, 2*np.pi)
            rad = np.random.uniform(0.5, 1.0)
            x_c = rad * np.cos(ang)
            y_c = rad * np.sin(ang)
            z_c = np.random.uniform(-0.2, 0.2)
            fig.add_trace(go.Scatter3d(
                x=[x_c], y=[y_c], z=[z_c],
                mode='markers',
                marker=dict(size=4, color='#FFFACD', opacity=0.4, symbol='circle'),
                showlegend=False
            ))

    # Terra: continentes simplificados e nuvens
    if planeta_nome == 'terra':
        # Nuvens brancas
        for _ in range(25):
            ang = np.random.uniform(0, 2*np.pi)
            rad = np.random.uniform(0.4, 1.0)
            x_c = rad * np.cos(ang)
            y_c = rad * np.sin(ang)
            z_c = np.random.uniform(-0.15, 0.15)
            fig.add_trace(go.Scatter3d(
                x=[x_c], y=[y_c], z=[z_c],
                mode='markers',
                marker=dict(size=5, color='white', opacity=0.5, symbol='circle'),
                showlegend=False
            ))
        # Manchas verdes/marrons simulando continentes
        for _ in range(15):
            ang = np.random.uniform(0, 2*np.pi)
            rad = np.random.uniform(0.2, 0.9)
            x_c = rad * np.cos(ang)
            y_c = rad * np.sin(ang)
            z_c = np.random.uniform(-0.1, 0.1)
            fig.add_trace(go.Scatter3d(
                x=[x_c], y=[y_c], z=[z_c],
                mode='markers',
                marker=dict(size=3, color='#228B22', opacity=0.6, symbol='square'),
                showlegend=False
            ))

    # Marte: calotas polares e tom avermelhado
    if planeta_nome == 'marte':
        # Calota polar norte
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[0.9],
            mode='markers',
            marker=dict(size=6, color='white', opacity=0.8),
            showlegend=False
        ))
        fig.add_trace(go.Scatter3d(
            x=[0], y=[0], z=[-0.9],
            mode='markers',
            marker=dict(size=5, color='white', opacity=0.7),
            showlegend=False
        ))
        # Tempestades de poeira
        for _ in range(20):
            ang = np.random.uniform(0, 2*np.pi)
            rad = np.random.uniform(0.3, 0.9)
            x_c = rad * np.cos(ang)
            y_c = rad * np.sin(ang)
            z_c = np.random.uniform(-0.2, 0.2)
            fig.add_trace(go.Scatter3d(
                x=[x_c], y=[y_c], z=[z_c],
                mode='markers',
                marker=dict(size=3, color='#D2B48C', opacity=0.5),
                showlegend=False
            ))

    # Júpiter: faixas e Grande Mancha Vermelha
    if planeta_nome == 'jupiter':
        # Faixas horizontais
        for z in np.linspace(-0.8, 0.8, 12):
            cor = '#D2B48C' if np.random.rand() > 0.5 else '#CD853F'
            fig.add_trace(go.Scatter3d(
                x=np.linspace(-1.0, 1.0, 30),
                y=np.zeros(30),
                z=np.full(30, z),
                mode='markers',
                marker=dict(size=3, color=cor, opacity=0.5),
                showlegend=False
            ))
        # Grande Mancha Vermelha
        fig.add_trace(go.Scatter3d(
            x=[-0.4], y=[0.3], z=[-0.2],
            mode='markers',
            marker=dict(size=12, color='#B22222', opacity=0.7, symbol='circle'),
            name='Grande Mancha Vermelha'
        ))

    # Saturno: anéis detalhados
    if planeta_nome == 'saturno' and mostrar_aneis:
        # Anel A (externo)
        theta = np.linspace(0, 2*np.pi, 200)
        r_ext = 2.3
        r_int = 1.8
        for r in np.linspace(r_int, r_ext, 10):
            x_r = r * np.cos(theta)
            y_r = r * np.sin(theta)
            z_r = np.zeros_like(theta)
            fig.add_trace(go.Scatter3d(
                x=x_r, y=y_r, z=z_r,
                mode='lines',
                line=dict(color='#D2B48C', width=1.5),
                opacity=0.7, showlegend=False
            ))
        # Anel B (mais brilhante)
        r_ext2 = 1.6
        r_int2 = 1.2
        for r in np.linspace(r_int2, r_ext2, 8):
            x_r = r * np.cos(theta)
            y_r = r * np.sin(theta)
            z_r = np.zeros_like(theta)
            fig.add_trace(go.Scatter3d(
                x=x_r, y=y_r, z=z_r,
                mode='lines',
                line=dict(color='#F5DEB3', width=2.0),
                opacity=0.8, showlegend=False
            ))
        # Divisão de Cassini (espaço vazio)
        # Anel C (mais interno e tênue)
        r_int3 = 1.0
        r_ext3 = 1.1
        for r in np.linspace(r_int3, r_ext3, 4):
            x_r = r * np.cos(theta)
            y_r = r * np.sin(theta)
            z_r = np.zeros_like(theta)
            fig.add_trace(go.Scatter3d(
                x=x_r, y=y_r, z=z_r,
                mode='lines',
                line=dict(color='#C0C0C0', width=1),
                opacity=0.5, showlegend=False
            ))

    # Urano: anéis verticais (devido à inclinação extrema)
    if planeta_nome == 'urano' and mostrar_aneis:
        theta = np.linspace(0, 2*np.pi, 150)
        r_ring = 1.8
        x_r = r_ring * np.cos(theta)
        y_r = np.zeros_like(theta)
        z_r = r_ring * np.sin(theta)
        fig.add_trace(go.Scatter3d(
            x=x_r, y=y_r, z=z_r,
            mode='lines',
            line=dict(color='#ADD8E6', width=2),
            opacity=0.6, name='Anéis de Urano'
        ))

    # Netuno: Grande Mancha Escura
    if planeta_nome == 'netuno':
        fig.add_trace(go.Scatter3d(
            x=[0.3], y=[-0.4], z=[0.1],
            mode='markers',
            marker=dict(size=10, color='#00008B', opacity=0.8, symbol='circle'),
            name='Grande Mancha Escura'
        ))

    # --- LUAS ---
    for nome_lua, dados in luas_pos.items():
        xr, yr, zr = dados['pos_rel']
        tam_lua = max(4, min(12, dados['tamanho'] * 10))
        fig.add_trace(go.Scatter3d(
            x=[xr], y=[yr], z=[zr],
            mode='markers+text',
            marker=dict(size=tam_lua, color=dados['cor'], line=dict(color='white', width=1)),
            text=[nome_lua],
            textposition='top center',
            textfont=dict(color=dados['cor'], size=9),
            name=nome_lua
        ))
        # Órbita da lua
        theta_orb = np.linspace(0, 2*np.pi, 150)
        x_orb = dados['distancia'] * np.cos(theta_orb)
        y_orb = dados['distancia'] * np.sin(theta_orb)
        z_orb = np.zeros_like(theta_orb)
        fig.add_trace(go.Scatter3d(
            x=x_orb, y=y_orb, z=z_orb,
            mode='lines',
            line=dict(color=dados['cor'], width=1, dash='dot'),
            opacity=0.35,
            showlegend=False
        ))

    # Configuração da cena
    fig.update_layout(
        title=dict(text=f'🪐 {planeta_escolhido_nome} e suas Luas — {data_hora.strftime("%d/%m/%Y %H:%M")} UTC',
                   x=0.5, font=dict(color='white', size=18)),
        scene=dict(
            xaxis=dict(title='X (UA)', backgroundcolor='rgb(5,5,20)', color='white', gridcolor='rgba(100,100,200,0.2)'),
            yaxis=dict(title='Y (UA)', backgroundcolor='rgb(5,5,20)', color='white', gridcolor='rgba(100,100,200,0.2)'),
            zaxis=dict(title='Z (UA)', backgroundcolor='rgb(5,5,20)', color='white', gridcolor='rgba(100,100,200,0.2)'),
            bgcolor='rgb(5,5,20)',
            camera=dict(eye=dict(x=2.0, y=2.0, z=1.5))
        ),
        paper_bgcolor='rgb(5,5,20)',
        font=dict(color='white'),
        height=700,
        margin=dict(l=0, r=0, t=60, b=0),
        showlegend=True
    )

    st.plotly_chart(fig, use_container_width=True)

    # Informações adicionais do planeta
    colA, colB, colC = st.columns(3)
    with colA:
        st.metric("🌡️ Temperatura média", f"{cfg['temperatura_superficie']} °C")
        st.metric("⚖️ Massa (rel. Terra)", f"{cfg['massa_relativa']:.2f}")
    with colB:
        st.metric("📏 Diâmetro (rel. Terra)", f"{cfg['tamanho_relativo']:.2f}")
        st.metric("🔄 Período orbital", f"{cfg['periodo']:.1f} dias")
    with colC:
        st.metric("💫 Velocidade orbital", f"{cfg['velocidade_orbital']:.2f} km/s")
        st.metric("🌑 Número de luas", len(cfg['luas']))

    st.markdown(f"**Influência astrofísica:** {cfg['influencia']}")
    if cfg['luas']:
        st.markdown("**Luas principais:** " + ", ".join([l['nome'] for l in cfg['luas']]))

    # Descrição textual personalizada
    descricoes = {
        'mercurio': "Pequeno e craterizado, Mercúrio é o planeta mais próximo do Sol. Sua superfície é marcada por impactos e variações extremas de temperatura.",
        'venus': "Vênus possui uma atmosfera densa de dióxido de carbono e nuvens de ácido sulfúrico, criando um efeito estufa descontrolado. É o planeta mais quente do Sistema Solar.",
        'terra': "Nosso lar azul, coberto por oceanos e vida. A Terra é o único planeta conhecido com placas tectônicas ativas e uma biosfera rica.",
        'marte': "O Planeta Vermelho tem calotas polares de gelo, vulcões extintos gigantescos e evidências de água no passado. Alvo principal da exploração humana futura.",
        'jupiter': "O maior planeta, uma bola de gás com faixas coloridas e a Grande Mancha Vermelha, uma tempestade centenária. Possui dezenas de luas, incluindo as galileanas.",
        'saturno': "Famoso por seus magníficos anéis, Saturno é um gigante gasoso menos denso que a água. Suas luas, como Titã e Encélado, são mundos fascinantes.",
        'urano': "Inclinado de lado, Urano tem anéis escuros e uma atmosfera fria de metano que lhe confere a cor azul-esverdeada.",
        'netuno': "O último gigante, azul profundo e varrido por ventos supersônicos. Netuno possui a Grande Mancha Escura e a lua retrógrada Tritão."
    }
    st.info(descricoes.get(planeta_nome, "Planeta do Sistema Solar."))
            
# ══════════════════════════════════════════════════════════════════
# MÓDULO 5 — FREQUÊNCIAS ÁUREAS
# ══════════════════════════════════════════════════════════════════
def modulo_frequencias_aureas():
    st.markdown("## 🎵 Frequências Áureas e Ressonâncias")

    col1, col2, col3 = st.columns(3)
    with col1:
        freq_base = st.number_input("Frequência Base (Hz)", value=432.0, min_value=0.001)
    with col2:
        num_harm = st.slider("Harmônicos", 5, 30, 13)
    with col3:
        fator_escala = st.selectbox("Escala", ["Áurea (φ)", "Deus (0.18)", "CICLO (0.99)"])

    fator = {'Áurea (φ)': PHI, 'Deus (0.18)': 1 + DEUS, 'CICLO (0.99)': 1 + CICLO}[fator_escala]
    frequencias = [freq_base * (fator ** i) for i in range(num_harm)]
    energias = [h_planck * f for f in frequencias]
    tensoes = [e / e_carga for e in energias]

    df_freq = pd.DataFrame({
        'Harmônico': range(1, num_harm + 1),
        'Frequência (Hz)': [round(f, 4) for f in frequencias],
        'Energia (J)': [f"{e:.3e}" for e in energias],
        'Tensão (V)': [f"{v:.3e}" for v in tensoes],
    })

    # Visualização espiral áurea das frequências
    theta = np.linspace(0, num_harm * 2 * math.pi, 1000)
    r_espiral = [freq_base * (fator ** (t / (2 * math.pi))) for t in theta]
    x_esp = [r * math.cos(t) for r, t in zip(r_espiral, theta)]
    y_esp = [r * math.sin(t) for r, t in zip(r_espiral, theta)]
    z_esp = list(theta)

    fig_esp = go.Figure()
    fig_esp.add_trace(go.Scatter3d(
        x=x_esp, y=y_esp, z=z_esp, mode='lines',
        line=dict(color=theta, colorscale='Rainbow', width=4),
        name='Espiral Áurea de Frequências'
    ))
    for i, f in enumerate(frequencias):
        ang = i * 2 * math.pi
        ri = freq_base * (fator ** i)
        fig_esp.add_trace(go.Scatter3d(
            x=[ri * math.cos(ang)], y=[ri * math.sin(ang)], z=[ang],
            mode='markers+text',
            marker=dict(size=8, color=f'hsl({int(i * 360 / num_harm)},100%,60%)'),
            text=[f'H{i+1}: {f:.1f}Hz'], textfont=dict(size=7, color='white'),
            name=f'H{i+1}', showlegend=False
        ))
    fig_esp.update_layout(
        title='Espiral Áurea — Frequências no Espaço 3D',
        scene=dict(bgcolor='rgb(5,5,15)',
                   xaxis=dict(color='white'), yaxis=dict(color='white'), zaxis=dict(color='white')),
        paper_bgcolor='rgb(5,5,15)', font=dict(color='white'), height=550
    )
    st.plotly_chart(fig_esp, use_container_width=True)
    st.dataframe(df_freq, use_container_width=True)


# ══════════════════════════════════════════════════════════════════
# MÓDULO 6 — APLICAÇÕES CÓSMICAS & PROBABILIDADES
# ══════════════════════════════════════════════════════════════════
def modulo_aplicacoes_cosmicas():
    st.markdown("## 🌌 Aplicações Cósmicas & Projeções")

    st.markdown("""
    Modelagem de eventos cósmicos com ajuste pelo **Espaço-Tempo FluxoMatemático**.
    As probabilidades são modificadas pelo tempo decorrido e por eventos observados —
    análogo à dilatação temporal relativística aplicada à análise de cenários.
    """)

    eventos_config = {
        "Colisão de Asteroide":  (1.5, 2.0),
        "Explosão de Supernova": (3.0, 4.5),
        "Formação Buraco Negro": (3.2, 5.0),
        "Passagem de Cometa":    (2.0, 3.5),
        "Erupção Solar (X-class)":(2.5, 6.5),
        "Alinhamento Planetário":(1.5, 2.5),
        "Choque de Galáxias":    (5.5, 23.0),
        "Formação de Estrela":   (4.5, 13.5),
    }

    col1, col2, col3 = st.columns(3)
    with col1:
        tempo_decorrido = st.slider("Tempo Decorrido (min)", 0, 90, 30)
    with col2:
        n_eventos = st.number_input("Eventos Observados", 0, 20, 2)
    with col3:
        aplicar_pilares = st.checkbox("Pilares FluxoMatemático", value=True)

    # Ajuste probabilístico
    aplicacoes = {}
    for nome, (p_min, p_max) in eventos_config.items():
        fator_tempo = 1 + (tempo_decorrido / 90) * (p_max - p_min) / p_min
        fator_evento = 1 + n_eventos * 0.05
        prob_ajust = ((p_min + p_max) / 2) * fator_tempo * fator_evento
        if aplicar_pilares:
            prob_ajust *= GRATIDAO * CICLO / PHI
        aplicacoes[nome] = round(prob_ajust, 3)

    df_ev = pd.DataFrame(list(aplicacoes.items()), columns=['Evento', 'Probabilidade Ajustada'])

    # Gráfico radar
    categorias = list(aplicacoes.keys())
    valores = list(aplicacoes.values())
    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=valores + [valores[0]],
        theta=categorias + [categorias[0]],
        fill='toself', fillcolor='rgba(100,50,200,0.3)',
        line=dict(color='#AA55FF', width=2),
        name='Probabilidades'
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor='rgb(10,10,30)',
            radialaxis=dict(color='white', gridcolor='rgba(255,255,255,0.2)'),
            angularaxis=dict(color='white', gridcolor='rgba(255,255,255,0.2)')
        ),
        paper_bgcolor='rgb(5,5,15)', font=dict(color='white'),
        title='Probabilidades Cósmicas — Radar FluxoMatemático', height=500
    )
    st.plotly_chart(fig_radar, use_container_width=True)

    # Gráfico 3D de escala galáctica
    df_ev['Impacto'] = df_ev['Probabilidade Ajustada'] * np.random.uniform(0.8, 1.2, len(df_ev))
    fig_3d = px.scatter_3d(
        df_ev, x='Evento', y='Probabilidade Ajustada', z='Impacto',
        size='Probabilidade Ajustada', color='Evento',
        title='Eventos Cósmicos — Escala Galáctica 3D'
    )
    fig_3d.update_layout(
        paper_bgcolor='rgb(5,5,15)', font=dict(color='white'), height=500,
        scene=dict(bgcolor='rgb(5,5,15)',
                   xaxis=dict(color='white'), yaxis=dict(color='white'), zaxis=dict(color='white'))
    )
    st.plotly_chart(fig_3d, use_container_width=True)
    st.dataframe(df_ev, use_container_width=True)


# ══════════════════════════════════════════════════════════════════
# MÓDULO 7 — AJUDA E ORIENTAÇÃO
# ══════════════════════════════════════════════════════════════════
def modulo_ajuda():
    st.markdown("## 📖 Ajuda e Orientação")

    st.info("""
    **Universo Áureo** é uma plataforma de simulação física integrando:
    - **Mecânica Kepleriana** (NASA-grade) para posições orbitais reais
    - **Relatividade Geral** (aproximação pós-Newtoniana) para buracos negros
    - **FluxoMatemático** de Marcelo Jubilado Catharino — constantes φ, MARC, JUBILO, DEUS, GRATIDÃO, CICLO
    """)

    with st.expander("🔭 Módulos Disponíveis"):
        st.markdown("""
        | Módulo | Descrição |
        |--------|-----------|
        | Buracos Negros | Simulação orbital + Schwarzschild + curvatura local |
        | Captação de Energia | Harmônicos áureos, bobina quântica, campo 3D |
        | Sistema Planetário | Posições Keplerianas, tecido espaço-tempo 3D com massa |
        | Frequências Áureas | Espiral φⁿ em 3D, tabela de harmônicos |
        | Aplicações Cósmicas | Modelagem probabilística de eventos com ajuste temporal |
        """)

    with st.expander("⚙️ Constantes FluxoMatemático"):
        cols = st.columns(3)
        constantes = [
            ("φ", PHI, "Proporção Áurea"),
            ("MARC", MARC, "Descida céu→terra"),
            ("JUBILO", JUBILO, "Subida terra→céu"),
            ("DEUS", DEUS, "Equilíbrio / Observação"),
            ("GRATIDÃO", GRATIDAO, "φ + DEUS"),
            ("CICLO", CICLO, "MARC + JUBILO"),
        ]
        for i, (nome, val, desc) in enumerate(constantes):
            cols[i % 3].metric(f"{nome} = {val}", desc)

    with st.expander("📐 Fórmulas Físicas Utilizadas"):
        st.markdown(r"""
        **Raio de Schwarzschild**: $r_s = \dfrac{2GM}{c^2}$

        **Equação de Kepler** (iterativa): $E = M + e\sin(E)$

        **Coordenadas Orbitais 3D**:
        - $x = a(\cos E - e)$
        - $y = a\sqrt{1-e^2}\sin E$
        - Rotação por inclinação $i$: $z = y \sin i$

        **Curvatura do Espaço-Tempo** (potencial gravitacional):
        $\Phi = -\dfrac{GM}{r}$

        **Energia Quântica**: $E = h \cdot f$

        **FluxoMatemático** — corrector do espaço-tempo:
        $\mathcal{F} = \phi \cdot \text{MARC} \cdot \text{GRATIDÃO} = \phi \times 0.54 \times 1.80$
        """)

    with st.expander("📡 Fontes e Referências"):
        st.markdown("""
        - **NASA Solar System Dynamics**: [ssd.jpl.nasa.gov](https://ssd.jpl.nasa.gov)
        - **NASA CNEOS** (asteroides): [cneos.jpl.nasa.gov](https://cneos.jpl.nasa.gov)
        - **Event Horizon Telescope**: [eventhorizontelescope.org](https://eventhorizontelescope.org)
        - **LIGO** (anomalias gravitacionais): [ligo.org](https://www.ligo.org)
        - **ALMAFLUXO** — Marcelo Jubilado Catharino
        """)

    st.markdown("""
    ---
    *"Quem entra pela ALMA → fica pelo FLUXO | Quem entra pelo FLUXO → descobre a ALMA"*

    *"Não sou o Nada e não sou o Tudo. Sou o Trajeto."* — Marcelo Jubilado Catharino
    """)


# ══════════════════════════════════════════════════════════════════
# APLICATIVO PRINCIPAL
# ══════════════════════════════════════════════════════════════════
def main():
    st.set_page_config(
        page_title="Universo Áureo — ALMAFLUXO",
        page_icon="🌌",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # CSS global — tema espacial profundo
    st.markdown("""
    <style>
    .stApp { background-color: #03030f; color: #e8e8ff; }
    .stSidebar { background-color: #080820; }
    .stSidebar * { color: #ccccff !important; }
    .stButton > button {
        background: linear-gradient(135deg, #1a0a4a, #3a1a8a);
        color: white; border: 1px solid #6644cc;
        border-radius: 8px; font-weight: 600;
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, #2a1a6a, #5522cc);
        border-color: #aa88ff;
    }
    .stMetric { background: rgba(100,60,200,0.15); border-radius: 8px; padding: 8px; }
    div[data-testid="stMetricValue"] { color: #FFD700; font-size: 1.1em; font-weight: 700; }
    .stTabs [data-baseweb="tab"] { color: #aaaaee; }
    .stTabs [aria-selected="true"] { color: #FFD700 !important; border-bottom-color: #FFD700 !important; }
    hr { border-color: #2a2a6a; }
    </style>
    """, unsafe_allow_html=True)

    # Cabeçalho
    st.markdown("""
    <div style='text-align:center; padding: 1rem 0;'>
        <h1 style='color:#FFD700; font-size:2.4em; letter-spacing:0.08em;
                   text-shadow: 0 0 30px rgba(255,215,0,0.5); margin:0;'>
            🌌 UNIVERSO ÁUREO
        </h1>
        <p style='color:#8888cc; font-size:0.95em; margin:4px 0 0;'>
            φ=1.618 · MARC=0.54 · JUBILO=0.45 · DEUS=0.18 · GRATIDÃO=1.80 · CICLO=0.99
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("""
    <div style='text-align:center; padding:1rem 0;'>
        <div style='font-size:2em;'>🌌</div>
        <div style='color:#FFD700; font-weight:700; font-size:1.1em;'>ALMAFLUXO</div>
        <div style='color:#8888cc; font-size:0.8em;'>Universo Áureo</div>
    </div>
    """, unsafe_allow_html=True)

    modulo = st.sidebar.radio(
        "Navegação",
        [
            "⚫ Buracos Negros e Anomalias",
            "⚡ Captação e Transformação de Energia",
            "🪐 Sistema Planetário e Espaço-Tempo",
            "🪐 Planetas, Luas e Espaço-Tempo",
            "🎵 Frequências Áureas",
            "🌌 Aplicações Cósmicas",
            "📖 Ajuda e Orientação"
        ]
    )

    st.sidebar.markdown("---")
    st.sidebar.markdown(f"""
    <div style='font-size:0.78em; color:#6666aa;'>
    <b style='color:#9988cc;'>FluxoMatemático</b><br>
    φ = {PHI}<br>
    MARC = {MARC} | JUBILO = {JUBILO}<br>
    DEUS = {DEUS} | GRATIDÃO = {GRATIDAO}<br>
    CICLO = {CICLO}<br><br>
    <i>Todos reduzem teosoficamente a 9</i>
    </div>
    """, unsafe_allow_html=True)

    # Roteamento
    if "Buracos Negros" in modulo:
        modulo_buracos_negros()
    elif "Captação" in modulo:
        modulo_captacao_energia()
    elif "Sistema Planetário" in modulo:
        modulo_sistema_planetario()
    elif "Planetas, Luas" in modulo:
        modulo_planeta_detalhado()
    elif "Frequências" in modulo:
        modulo_frequencias_aureas()
    elif "Aplicações" in modulo:
        modulo_aplicacoes_cosmicas()
    elif "Ajuda" in modulo:
        modulo_ajuda()

if __name__ == "__main__":
    main()
