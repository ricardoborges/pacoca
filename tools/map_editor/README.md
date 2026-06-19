# Paçoca — Editor Visual de Mapas

Editor web para desenhar fases e compilá-las em cenas `.tscn` do Godot, sem sair do navegador.

## Como rodar (modo completo, com botão "Compilar agora")

A partir da raiz do repositório:

```bash
python tools/map_editor/server.py
```

Depois abra **http://localhost:8000** no navegador.

- Desenhe a fase no grid.
- **Mapas** — salva o mapa atual em disco (`tools/map_editor/levels/level_<id>_map.txt`),
  lista os custom levels criados e permite **abrir para editar** ou **excluir**.
- **Compilar** — gera `src/scenes/levels/level_<id>.tscn` a partir do mapa.
- **Testar fase** (**F5**) — compila a fase atual e abre o Godot **direto nela**.
- **Executar** — abre o jogo a partir do menu.

### Atalhos

- **B** = pintar · **E** = borracha · **F5** = testar fase · **Esc** = fechar o painel de código.

### Caminho do Godot

Os botões **Testar fase** / **Executar** precisam do executável do Godot. O servidor o resolve
nesta ordem: **caminho salvo no editor → variável `GODOT_BIN` → detecção no PATH → padrão**.

- Clique na **engrenagem** (top bar) para ver/definir o caminho. Se o Godot estiver no PATH,
  ele é detectado e preenchido automaticamente na inicialização; caso contrário, informe o caminho
  e clique em **Salvar** (persiste em `editor_config.json`, ignorado pelo git).

### Variáveis de ambiente

- `PORT` — porta do servidor (padrão `8000`).
- `GODOT_BIN` — caminho do Godot (usado se nenhum caminho foi salvo no editor).

## Modo simples (sem servidor)

Você pode abrir `index.html` direto via `file://` para desenhar, copiar/baixar o
ASCII/JSON e compilar manualmente. Nesse modo o botão **Compilar agora** não funciona
(o navegador não permite rodar processos) — use o comando mostrado na aba Compilar.

## Arquitetura

- `index.html` / `app.js` / `styles.css` — o editor (estático).
- `icons/` — ícones SVG dos blocos da paleta.
- `levels/` — **mapas-fonte** (`.txt`/`.json`) salvos pelo editor (custom levels).
- `server.py` — servidor local (stdlib, sem dependências). Serve o editor e expõe a API
  (`/api/compile`, `/api/run`, `/api/config`, `/api/maps`).
- Os scripts de build (`convert_map.py`, `generate_level.py`) permanecem em
  `src/scripts/` — o servidor apenas os orquestra. Ao compilar, ele lê o mapa de
  `levels/` e os artefatos gerados (`.py`/`.tscn`) vão para o projeto Godot (`src/`).

Sintaxe dos mapas e métricas de design: veja [`docs/map_syntax.md`](../../docs/map_syntax.md).
