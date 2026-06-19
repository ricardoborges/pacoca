"""Generated level definition for level 04 ("Sky Ruins").
Generated automatically from level_04_map.txt. Do not edit directly if you want to keep changes synced!
"""

from __future__ import annotations
import re
from generate_level import NodeBuilder, apply_modification

ANCHOR = '[node name="Platform_0"'

def base_edits(content: str) -> str:
    # Safely position the SpawnPoint
    spawn_pattern = r'(\[node name="SpawnPoint"[^\]]*\]\s*\ntransform = Transform3D\(1, 0, 0, 0, 1, 0, 0, 0, 1, )([^,]+), ([^,]+), ([^\)]+)'
    spawn_replacement = rf'\g<1>14.00, 1.50, 0'
    content = re.sub(spawn_pattern, spawn_replacement, content)
    return content

def build(b: NodeBuilder) -> None:
    b.add_platform("Platform_0", 2.00, 0.00, width=6.00)
    b.add_platform("Platform_1", 19.00, 0.00, width=24.00)
    b.add_platform("Platform_2", 45.00, 0.00, width=24.00)
    b.add_platform("Platform_3", 63.00, 0.00, width=8.00)
    b.add_platform("Platform_4", 70.00, 0.00, width=2.00)
    b.add_platform("Platform_5", 6.00, 3.00, width=6.00)
    b.add_ring("Ring_0", 16.00, 1.20)
    b.add_ring("Ring_1", 18.00, 1.20)
    b.add_ring("Ring_2", 20.00, 1.20)
    b.add_ring("Ring_3", 22.00, 1.20)
    b.add_ring("Ring_4", 24.00, 1.20)
    b.add_cactus("Cactus_0", 44.00, 1.00, speed=1.25)
    b.add_level_finish("Goal_0", 64.00, 5.00)
