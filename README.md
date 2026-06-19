# Paçoca

Plataforma 2.5D no estilo Sonic, feito em **Godot 4.6** com **C# (.NET 8)**.

O jogador controla o Paçoca por fases corrido-rápidas: corre, pula, faz *roll*, carrega *spin dash* e *air dash*, coleta moedas (anéis) e desvia de inimigos — tudo com física customizada de aceleração, atrito e rampas.

## Funcionalidades

- **Física estilo Sonic**: aceleração/desaceleração, atrito, gravidade manual, força em rampas, *spin dash* carregável, *air dash* diagonal e altura de pulo variável.
- **Renderização 3D em plano 2D (2.5D)**: o jogador é um `CharacterBody3D` travado no plano XY, com modelos 3D animados.
- **Áudio 100% procedural**: todos os efeitos sonoros são gerados em tempo real como ondas senoidais — não há arquivos de áudio.
- **HUD**: pontuação, tempo, moedas, vidas e velocidade (km/h).
- **Suporte a gamepad**: seleção de joystick e mapeamento automático dos botões mais comuns.
- **Menu completo**: jogar, opções, créditos, conquistas e seleção de fase (incluindo fase de *debug*).

## Controles

| Ação | Teclado | Gamepad |
|------|---------|---------|
| Mover | Setas / `A` `D` | D-pad / analógico esquerdo |
| Pular / Air dash | `Espaço` / `Z` | A, B, X, Y |
| Agachar / Roll / Spin dash | `S` (segurar) + pular para carregar | D-pad ↓ |
| Dash | `X` / `Shift` | — |
| Pausar | `Esc` | Start |

## Requisitos

- **Godot 4.6** edição **.NET / Mono** (necessária para projetos C#)
- **.NET SDK 8.0**

## Como rodar

1. Abra o projeto no editor Godot apontando para `src/project.godot`.
2. O Godot compila o assembly C# automaticamente.
3. Execute o projeto (F5). A cena inicial é `res://scenes/menu.tscn`.

Para apenas compilar o C# pela linha de comando (a partir de `src/`, onde fica `Paçoca.csproj`):

```bash
dotnet build
```

## Estrutura do projeto

> Atenção à pasta `src` aninhada: o repositório git fica na raiz, mas o **projeto Godot** está em `src/`, e os **scripts C#** ficam em `src/src/`.

```
Paçoca/
├── assets/                 # Assets brutos (modelos exportados, etc.)
├── docs/                   # Documentação (ex.: map_syntax.md)
├── tools/
│   └── map_editor/         # Editor visual de mapas (web + server.py)
└── src/                    # Raiz do projeto Godot (res://)
    ├── project.godot
    ├── Paçoca.csproj
    ├── scenes/             # Cenas: menu, main, hud, player, inimigos, fases...
    │   └── levels/         # level_01.tscn, debug.tscn
    ├── scripts/            # Pipeline de fases (convert_map.py, generate_level.py)
    │   └── levels/         # Mapas-fonte (.txt/.json) e módulos gerados
    ├── models/             # Modelos FBX animados (Mixamo)
    ├── materials/
    ├── textures/
    └── src/                # Scripts C#  (res://src/*.cs)
        ├── Main.cs         # Coordena o gameplay e carrega as fases
        ├── Player.cs       # Jogador (CharacterBody3D) e física
        ├── GameSettings.cs # Estado global entre cenas (fase, gamepad)
        ├── CameraController.cs
        ├── HUD.cs, Menu.cs, PauseMenu.cs, GameOver.cs
        └── Ring.cs, Spring.cs, DashPad.cs, Enemy.cs
```

## Criação de fases (editor de mapas)

As fases são desenhadas como **mapas** (grid ASCII ou JSON) e convertidas em cenas Godot (`level_XX.tscn`) por um pipeline em Python. Há um **editor visual web** que cobre todo o ciclo: desenhar → compilar → testar.

### Editor visual (`tools/map_editor/`)

```bash
python tools/map_editor/server.py     # abra http://localhost:8000
```

- **Dock de paleta** (plataformas, rampas, anéis, molas, inimigos, espinhos, spawn, fim de fase) + ferramentas pintar/borracha.
- **Compilar** — gera o `.tscn` da fase a partir do desenho.
- **Testar fase** (`F5`) — compila a fase atual e abre o Godot **direto nela**.
- **Executar** — abre o jogo pelo menu.
- **Engrenagem** — configura o caminho do executável do Godot (detectado no PATH automaticamente; informe manualmente se não estiver).
- Atalhos: `B` pintar · `E` borracha · `F5` testar · `Esc` fechar.

> O editor também funciona aberto direto (`file://`) para desenhar e exportar, mas os botões que executam o Godot/compilam exigem o servidor local.

### Compilar pela linha de comando

A partir de `src/` (raiz do projeto Godot):

```powershell
python scripts/convert_map.py --input scripts/levels/level_04_map.txt --level 04
```

Isso gera/atualiza `src/scenes/levels/level_04.tscn`, pronto para abrir no Godot.

### Sintaxe rápida

Cada **coluna** do grid vale 2 m (X) e cada **linha** 3 m (Y, `ystep`); a última linha não-vazia é o chão (`Y = 0`).

| Char | Elemento | Char | Elemento |
|:----:|----------|:----:|----------|
| `#` | plataforma | `V` `F` | mola vertical / diagonal |
| `/` `\` | rampa sobe / desce | `D` | acelerador (dash) |
| `o` | anel | `E` `C` | inimigo / cacto |
| `P` | spawn do jogador | `S` | espinhos |
| `G` | moeda de fim de fase | ` ` | vazio |

📖 **Documentação completa** (regras do grid, alturas, headroom do jogador, formato JSON, flag `--level`): [`docs/map_syntax.md`](docs/map_syntax.md).

## Arquitetura

- **`Main.cs`** é o coordenador do gameplay (raiz de `main.tscn`): lê `GameSettings.LevelToLoad`, instancia a fase dentro de um `LevelWrapper` e posiciona o jogador no `SpawnPoint` (`Marker3D`) da fase. As fases são cenas intercambiáveis em `scenes/levels/`.
- **`GameSettings.cs`** é um estado estático global que guarda a fase selecionada e o joystick escolhido, persistindo entre as trocas de cena.
- **Fluxo de cenas**: `menu.tscn` → `main.tscn` → `game_over.tscn` → `menu.tscn`, com `pause_menu.tscn` sobreposto durante o jogo.
- **Comunicação com a UI**: o `Player` emite o sinal `PlayerStatsChanged(rings, score, speed, lives)`, ao qual o `HUD` se conecta. Objetos como `Ring`, `Spring`, `DashPad` e `Enemy` chamam métodos públicos do `Player` (`CollectRing()`, `ApplyBoost()`, `Hurt()`).

Para detalhes de desenvolvimento, veja `src/CLAUDE.md`.
