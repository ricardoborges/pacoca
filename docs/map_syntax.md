# Guia de Desenho de Mapas — Paçoca 2.5D

Este documento descreve como desenhar fases do Paçoca em **Texto (Grid ASCII)** ou **JSON**, como o editor visual e o conversor funcionam, e como transformar um mapa em um nível jogável (`.tscn`) do Godot.

> **Fonte da verdade:** o comportamento descrito aqui reflete `src/scripts/convert_map.py` (parser) e `src/scripts/generate_level.py` (gerador de cena). Se a doc e o código divergirem, o código vence — veja a seção [Inconsistências conhecidas](#inconsistências-conhecidas).

---

## Visão geral do pipeline

```
mapa .txt / .json
      │
      ▼
src/scripts/convert_map.py        ← faz o parse e gera os dados do nível
      │   ├─ cria src/scripts/levels/level_XX.py     (módulo de dados: build())
      │   └─ cria src/scenes/levels/level_XX.tscn    (cena base, só se não existir)
      ▼
src/scripts/generate_level.py     ← compila a geometria/objetos na .tscn
      │
      ▼
src/scenes/levels/level_XX.tscn   ← nível jogável, abrir no Godot
```

Três formas de produzir o mapa de entrada:

1. **Editor visual** (`tools/map_editor/index.html`) — desenha clicando, exporta `.txt` ou `.json`.
2. **Grid ASCII** escrito à mão em qualquer editor de texto.
3. **JSON estruturado** — para coordenadas decimais exatas e parâmetros customizados.

---

## Sistema de coordenadas

O mapa é uma vista lateral (plano XY). O jogo é 3D renderizado, mas a física vive no plano XY (o Z é fixado em 0).

| Eixo | Significado | Conversão a partir do grid |
| :--- | :--- | :--- |
| **X** (horizontal) | Cada **coluna** vale **2,0 m**. | `x = coluna * 2.0` |
| **Y** (vertical) | Cada **linha** vale `ystep` metros (ver abaixo). | `y = linha * ystep` |

- A **coluna 0** (extrema esquerda) é o início da fase.
- A **última linha não-vazia** do bloco `[grid]` é o chão mais baixo, `Y = 0`. Linhas acima aumentam a altura.
- O conversor **mescla** sequências horizontais de `#` em um único colisor de física, evitando que o jogador prenda nas emendas.

### O parâmetro `ystep` (leia com atenção)

`ystep` define quantos metros vale cada linha vertical do grid. Ele é lido do cabeçalho do arquivo:

```text
ystep: 3.0
```

- **A altura padrão é `3.0` m por linha.** Tanto o editor visual quanto o default do `convert_map.py` usam esse valor, então todo nível novo nasce com a mesma escala vertical — você não precisa pensar nisso.
- O editor grava `ystep: 3.0` automaticamente no `.txt` exportado, e o `.json` carrega coordenadas absolutas equivalentes.
- O cabeçalho `ystep:` existe só como escape para casos legados ou experimentais (ex.: `level_01.txt` foi feito com `ystep: 1.0`). **Para padronizar, não defina `ystep` ao criar fases novas** — deixe o default de 3.0 valer.

---

## Legenda dos caracteres

| Caractere | Elemento | Cena / Comportamento |
| :--- | :--- | :--- |
| ` ` (espaço) ou `.` | **Ar / Vazio** | Espaço vazio |
| `#` | **Plataforma de grama** | Bloco sólido (`CSGBox3D`) com base de pedra |
| `/` | **Rampa subindo** | Rampa diagonal para a direita (`CSGPolygon3D`) |
| `\` | **Rampa descendo** | Rampa diagonal para a esquerda (`CSGPolygon3D`) |
| `o` | **Anel (ring)** | Colecionável (`ring.tscn`) |
| `V` | **Mola vertical** | Lança o jogador para cima (`spring.tscn`, força 22) |
| `F` | **Mola diagonal** | Lança para frente e cima (`spring.tscn`, força 25) |
| `D` ou `>` | **Acelerador (dash pad)** | Acelera o jogador para frente (`dash_pad.tscn`) |
| `E` | **Inimigo comum** | Robô patrulheiro (`enemy.tscn`, velocidade 3.0) |
| `C` | **Inimigo cacto** | Cacto patrulheiro (`cactus_enemy.tscn`, velocidade 1.25) |
| `S` | **Espinhos** | Fileira de espinhos que causa dano (`spikes.tscn`) |
| `P` | **Spawn do player** | Posição inicial do jogador (`Marker3D` SpawnPoint) |
| `G` | **Moeda de fim de fase** | Moeda gigante giratória que finaliza o nível (`level_finish.tscn`) |

> `>` é aceito como alias de `D` apenas pelo conversor Python. O editor visual só conhece `D`.

### Regra de altura dos objetos (importante)

Plataformas (`#`) e rampas ocupam a própria linha em que são desenhadas. **Já os objetos (anéis, molas, inimigos, espinhos, spawn, goal) são ancorados à linha logo ABAIXO deles.** Ou seja, eles flutuam acima da superfície que estaria uma linha abaixo:

| Objeto | Altura final (`r` = linha, base 0) |
| :--- | :--- |
| Anel `o` | `(r-1) * ystep + 1.2` |
| Mola `V` / `F`, dash `D`, espinhos `S` | `(r-1) * ystep + 0.5` |
| Inimigo `E` / `C` | `(r-1) * ystep + 1.0` |
| Spawn `P` | `(r-1) * ystep + 1.5` |
| Goal `G` | `(r-1) * ystep + 2.0` |

**Na prática:** para colocar um anel, inimigo ou spawn **em cima** de uma plataforma, desenhe-o na linha **imediatamente acima** do `#`. Veja no exemplo abaixo como `P`, `C` e `o` ficam todos na linha acima do chão.

### Plataformas flutuantes vs. ancoradas

O conversor decide automaticamente a profundidade da base de pedra de cada `#`:

- **Ancorada (`rock_height = 4.0`)**: existe `#`, `/` ou `\` diretamente abaixo de qualquer coluna do bloco — pedra desce até o chão.
- **Flutuante (`rock_height = 1.0`)**: nada sólido abaixo — fina laje suspensa.

No JSON você pode forçar isso com o campo `rock_height` em cada plataforma.

---

## Opção 1 — Grid ASCII

Cabeçalho com pares `chave: valor`, seguido de uma seção `[grid]` com o desenho.

```text
level: 03
name: Ruínas Celestes

[grid]

                                  G
                                  #
                ooo oo  o        #
              ooo                #
             o#################  #
          ooo                    #
          o#########             #
        o o                      #
       o #####       ########    #
      o   C   ####           #  ##
    oo  #    ##       C         #
   o   ##C   ##  ########       #
 oo  ##########                 #
  P     C             C         #
#################################
```

### Regras do grid

- Linhas em branco no topo são preservadas (dão altura); linhas em branco no final são descartadas (a última linha com conteúdo é `Y = 0`).
- A largura final é a da maior linha; linhas mais curtas são preenchidas com espaços à direita.
- `#` em sequência horizontal vira um único colisor.
- `/` formam uma cadeia diagonal subindo para a direita (coluna +1, linha +1); `\` descem para a direita (coluna +1, linha −1). Desenhe cada degrau adjacente na diagonal para que se fundam em uma rampa só.

---

## Opção 2 — JSON estruturado

Ideal para posições decimais exatas, parâmetros customizados (velocidade de inimigos, força/direção de molas) ou geração externa.

```json
{
  "level": "03",
  "name": "Templo do Caos",
  "spawn": [4.0, 1.5],
  "platforms": [
    { "x": 3.0, "y": 0.0, "width": 8.0 },
    { "x": 20.0, "y": 0.0, "width": 14.0, "rock_height": 1.0 }
  ],
  "ramps_up": [
    { "x": 73.0, "y": -0.5, "width": 2.0, "height": 1.0 }
  ],
  "ramps_down": [
    { "x": 79.0, "y": -0.5, "width": 2.0, "height": 1.0 }
  ],
  "rings": [
    [16.0, 1.2],
    [20.0, 1.2]
  ],
  "springs_vert": [
    { "x": 42.0, "y": -0.5, "force": 22.0 }
  ],
  "springs_diag": [
    { "x": 102.0, "y": 14.5, "force": 25.0, "dx": 1.2, "dy": 1.5, "lock": 0.6 }
  ],
  "dash_pads": [
    [34.0, -0.5]
  ],
  "enemies": [
    { "x": 50.0, "y": 0.0, "speed": 3.0 }
  ],
  "cactus_enemies": [
    { "x": 88.0, "y": 0.0, "speed": 1.25 }
  ],
  "spikes": [
    [106.0, 0.5]
  ],
  "goals": [
    [120.0, 2.0]
  ]
}
```

| Chave | Tipo | Campos |
| :--- | :--- | :--- |
| `spawn` | `[x, y]` | — |
| `platforms` | objetos | `x` (centro), `y`, `width`, `rock_height?` |
| `ramps_up` / `ramps_down` | objetos | `x`, `y`, `width`, `height` |
| `rings` | `[x, y]` | — |
| `springs_vert` | objetos | `x`, `y`, `force` |
| `springs_diag` | objetos | `x`, `y`, `force`, `dx`, `dy`, `lock` |
| `dash_pads` | `[x, y]` | — |
| `enemies` / `cactus_enemies` | objetos | `x`, `y`, `speed` |
| `spikes` | `[x, y]` | — |
| `goals` | `[x, y]` | — |

> No JSON, `x` de plataforma é o **centro** do bloco; `width` é a largura total em metros. `rock_height` é opcional — se omitido, o conversor detecta sozinho se a plataforma flutua.

---

## Compilando para o Godot

O conversor vive em `src/scripts/`, e os caminhos de `--input` são relativos ao diretório onde você roda o comando. **Execute a partir da raiz do projeto Godot (`src/`)**, não da raiz do repositório Git.

```powershell
# A partir de D:\dev\games\Paçoca\src
python scripts/convert_map.py --input scripts/levels/level_04_map.txt --level 04
python scripts/convert_map.py --input scripts/levels/level_04_map.json --level 04
```

O comando irá:

1. Fazer o parse do `.txt`/`.json` em estruturas de nível.
2. Criar `src/scenes/levels/level_04.tscn` (água, montanhas de fundo, SpawnPoint) **se ainda não existir**.
3. Gerar `src/scripts/levels/level_04.py` (módulo de dados com `build()`).
4. Chamar `generate_level.py`, que compila a geometria e distribui itens/inimigos na cena.

Depois, abra/recarregue o projeto no Godot 4.6 (Mono/.NET) para testar.

### Re-geração é idempotente

`generate_level.py` localiza o bloco gerado pela âncora `[node name="Platform_0"` e o substitui inteiro a cada execução, faz backup `.tscn.bak` e reposiciona o SpawnPoint via `base_edits`. Pode recompilar quantas vezes quiser sem acumular nós duplicados. **Não edite à mão a parte gerada do `.tscn`** — ela é sobrescrita.

### Rodar uma fase específica direto (flag `--level`)

Os níveis (`level_XX.tscn`) não são jogáveis isolados: são carregados pelo `main.tscn` via `Main.cs`. Para abrir o jogo **direto em uma fase** (útil para iteração), passe o nível por linha de comando — `Main.cs` lê o argumento e sobrescreve `GameSettings.LevelToLoad`:

```powershell
# Por id (vira res://scenes/levels/level_04.tscn)
& "<godot>.exe" --path .\src scenes/main.tscn -- --level=04

# Ou por caminho completo res://
& "<godot>.exe" --path .\src scenes/main.tscn -- --level=res://scenes/levels/level_04.tscn
```

O `--` separa os argumentos do Godot dos argumentos do jogo; `--level=` precisa vir depois dele. Sem essa flag, o jogo carrega a fase padrão.

---

## O editor visual (`tools/map_editor/`)

App web com servidor local opcional. Para o fluxo completo (compilar/testar/executar), rode:

```powershell
python tools/map_editor/server.py   # abra http://localhost:8000
```

Sem o servidor (abrindo `index.html` via `file://`) o editor funciona para desenhar e exportar, mas os botões que executam processos ficam indisponíveis.

**Interface**
- **Dock lateral** com ferramentas (Pintar / Borracha / Limpar) e a **paleta em ícones** (tooltip no hover) com os 12 elementos.
- **Top bar** com id/nome do nível, dimensões do grid, zoom e linhas do grid.
- **Canvas** dominante; barra inferior com coordenadas e navegação horizontal.
- **Drawer** (botão **Código**) com abas **ASCII**, **JSON**, **Importar** e **Compilar**.
- Apenas **um** spawn `P` é permitido (pintar outro remove o anterior).
- Exporta `.txt` (`level_XX_map.txt`) e `.json` (`level_XX_map.json`).

**Ações (exigem o servidor local)**
- **Compilar** — gera o `.tscn` da fase.
- **Testar fase** (atalho **F5**) — compila a fase atual e abre o Godot **direto nela** (faz um `dotnet build` incremental antes, para a flag `--level` valer).
- **Executar** — abre o jogo a partir do menu.

**Atalhos de teclado**
- **B** = pintar · **E** = borracha · **F5** = testar fase · **Esc** = fechar o drawer.

> Configuração do Godot: o servidor usa a variável de ambiente `GODOT_BIN` (com um caminho padrão). Ex.: `GODOT_BIN="C:\...\Godot.exe" python tools/map_editor/server.py`.

> O editor usa `Y_STEP = 3.0` internamente para gerar tanto o ASCII (gravando `ystep: 3.0` no cabeçalho) quanto o JSON (coordenadas absolutas).

---

## Métricas de design (Platformer Kit)

- **Bloco / rampa:** 2 m de largura por coluna.
- **Linha do grid:** 3 m de altura (`ystep` padrão).
- **Salto:** ~4 m parado, até ~15 m em velocidade máxima.
- **Mola vertical:** lança ~22 m de altura.
- **Queda fatal:** evite plataformas alcançáveis abaixo de `Y < -15 m` (há água/abismo).
- **Spawn padrão da cena base:** `(-12, 1.5)` até ser reposicionado pelo `P`/`spawn`.

### Tamanho do jogador e headroom (vãos passáveis)

A colisão do player é uma **esfera de raio 0.55 → diâmetro 1.1 m** (fixa; não encolhe ao rolar). Para passar por um vão, o mínimo físico é **~1.1 m**; mire em **≥1.5 m** para folga visual.

Cada linha do grid vale 3 m, então **uma linha totalmente vazia = 3 m de espaço vertical livre** — já mais que suficiente para o boneco.

**Túnel sob uma plataforma flutuante (chão embaixo, flutuante em cima).** Duas regras antes da conta:

- Nunca empilhe `#` diretamente sobre `#`: o bloco de cima é detectado como **ancorado** (base de pedra de 4 m) e tampa o vão.
- A plataforma flutuante tem a parte sólida descendo **1.5 m abaixo do seu centro** (grama + pedra), e a linha logo abaixo dela precisa estar **vazia** para que ela conte como flutuante.

Com **N linhas vazias** entre o chão e a flutuante, o vão livre é `(N+1) × 3 − 2.0` m:

| Linhas vazias (N) | Vão livre | Passa? (player 1.1 m) |
| :--- | :--- | :--- |
| 1 | **4.0 m** | ✅ folgado |
| 2 | 7.0 m | ✅ |
| 3 | 10.0 m | ✅ |

Ou seja, a `ystep: 3.0`, **uma única linha vazia já abre um corredor de 4 m** — confortável. (`level_01`, com `ystep: 1.0`, é o caso apertado: precisaria de ~3 linhas vazias.)

---

## Inconsistências conhecidas

Pontos onde editor, conversor e docs antigas divergiam — registrados aqui para evitar surpresas:

1. **Altura vertical — PADRONIZADA em 3.0.** Editor e `convert_map.py` usam o mesmo default (`3.0`), e o editor grava `ystep: 3.0` no `.txt`. Não há mais divergência de escala para fases novas.
   - **Níveis legados:** `level_01.txt` fixa `ystep: 1.0` no cabeçalho e continua valendo. `level_04_map.txt` não tem cabeçalho e já compilava a 3.0, então segue inalterado.

2. **Caminhos relativos.** Os comandos exibidos no editor usam `scripts/...`, que só funcionam se executados de dentro de `src/` (raiz do projeto Godot), não da raiz do repositório.

3. **Alias `>`.** Aceito pelo conversor como dash pad, mas ausente no editor visual.
