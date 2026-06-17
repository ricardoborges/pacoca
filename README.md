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
└── src/                    # Raiz do projeto Godot (res://)
    ├── project.godot
    ├── Paçoca.csproj
    ├── scenes/             # Cenas: menu, main, hud, player, inimigos, fases...
    │   └── levels/         # level_01.tscn, debug.tscn
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

## Arquitetura

- **`Main.cs`** é o coordenador do gameplay (raiz de `main.tscn`): lê `GameSettings.LevelToLoad`, instancia a fase dentro de um `LevelWrapper` e posiciona o jogador no `SpawnPoint` (`Marker3D`) da fase. As fases são cenas intercambiáveis em `scenes/levels/`.
- **`GameSettings.cs`** é um estado estático global que guarda a fase selecionada e o joystick escolhido, persistindo entre as trocas de cena.
- **Fluxo de cenas**: `menu.tscn` → `main.tscn` → `game_over.tscn` → `menu.tscn`, com `pause_menu.tscn` sobreposto durante o jogo.
- **Comunicação com a UI**: o `Player` emite o sinal `PlayerStatsChanged(rings, score, speed, lives)`, ao qual o `HUD` se conecta. Objetos como `Ring`, `Spring`, `DashPad` e `Enemy` chamam métodos públicos do `Player` (`CollectRing()`, `ApplyBoost()`, `Hurt()`).

Para detalhes de desenvolvimento, veja `src/CLAUDE.md`.
