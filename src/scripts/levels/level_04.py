"""Generated level definition for level 04 ("Parque do Pacoca").
Generated automatically from level_04_map.txt. Do not edit directly if you want to keep changes synced!
"""

from __future__ import annotations
import re
from generate_level import NodeBuilder, apply_modification

ANCHOR = '[node name="Platform_0"'

def base_edits(content: str) -> str:
    # Safely position the SpawnPoint
    spawn_pattern = r'(\[node name="SpawnPoint"[^\]]*\]\s*\ntransform = Transform3D\(1, 0, 0, 0, 1, 0, 0, 0, 1, )([^,]+), ([^,]+), ([^\)]+)'
    spawn_replacement = rf'\g<1>12.00, 1.50, 0'
    content = re.sub(spawn_pattern, spawn_replacement, content)
    return content

def build(b: NodeBuilder) -> None:
    b.add_platform("Platform_0", 17.00, 0.00, width=36.00)
    b.add_platform("Platform_1", 58.00, 0.00, width=34.00)
    b.add_platform("Platform_2", 113.00, 0.00, width=64.00)
    b.add_platform("Platform_3", 137.00, 3.00, width=20.00)
    b.add_platform("Platform_4", 138.00, 6.00, width=18.00)
    b.add_platform("Platform_5", 139.00, 9.00, width=16.00)
    b.add_platform("Platform_6", 34.00, 12.00, width=6.00, rock_height=1.00)
    b.add_platform("Platform_7", 60.00, 12.00, width=18.00, rock_height=1.00)
    b.add_platform("Platform_8", 140.00, 12.00, width=14.00)
    b.add_platform("Platform_9", 85.00, 15.00, width=4.00, rock_height=1.00)
    b.add_platform("Platform_10", 119.00, 15.00, width=4.00, rock_height=1.00)
    b.add_platform("Platform_11", 142.00, 15.00, width=14.00)
    b.add_platform("Platform_12", 64.00, 18.00, width=14.00, rock_height=1.00)
    b.add_platform("Platform_13", 143.00, 18.00, width=12.00)
    b.add_platform("Platform_14", 144.00, 21.00, width=10.00)
    b.add_platform("Platform_15", 145.00, 24.00, width=8.00)
    b.add_platform("Platform_16", 146.00, 27.00, width=6.00)
    b.add_platform("Platform_17", 147.00, 30.00, width=4.00)
    b.add_platform("Platform_18", 148.00, 33.00, width=2.00)
    b.add_ring("Ring_0", 10.00, 4.20)
    b.add_ring("Ring_1", 12.00, 4.20)
    b.add_ring("Ring_2", 14.00, 4.20)
    b.add_ring("Ring_3", 26.00, 4.20)
    b.add_ring("Ring_4", 28.00, 4.20)
    b.add_ring("Ring_5", 30.00, 4.20)
    b.add_ring("Ring_6", 14.00, 7.20)
    b.add_ring("Ring_7", 16.00, 7.20)
    b.add_ring("Ring_8", 18.00, 7.20)
    b.add_ring("Ring_9", 20.00, 7.20)
    b.add_ring("Ring_10", 22.00, 7.20)
    b.add_ring("Ring_11", 24.00, 7.20)
    b.add_ring("Ring_12", 26.00, 7.20)
    b.add_ring("Ring_13", 18.00, 10.20)
    b.add_ring("Ring_14", 20.00, 10.20)
    b.add_ring("Ring_15", 22.00, 10.20)
    b.add_ring("Ring_16", 66.00, 19.20)
    b.add_ring("Ring_17", 68.00, 19.20)
    b.add_ring("Ring_18", 70.00, 19.20)
    b.add_ring("Ring_19", 88.00, 19.20)
    b.add_ring("Ring_20", 90.00, 19.20)
    b.add_ring("Ring_21", 92.00, 19.20)
    b.add_ring("Ring_22", 112.00, 19.20)
    b.add_ring("Ring_23", 114.00, 19.20)
    b.add_ring("Ring_24", 116.00, 19.20)
    b.add_ring("Ring_25", 92.00, 22.20)
    b.add_ring("Ring_26", 94.00, 22.20)
    b.add_ring("Ring_27", 96.00, 22.20)
    b.add_ring("Ring_28", 108.00, 22.20)
    b.add_ring("Ring_29", 110.00, 22.20)
    b.add_ring("Ring_30", 112.00, 22.20)
    b.add_ring("Ring_31", 96.00, 25.20)
    b.add_ring("Ring_32", 98.00, 25.20)
    b.add_ring("Ring_33", 100.00, 25.20)
    b.add_ring("Ring_34", 102.00, 25.20)
    b.add_ring("Ring_35", 104.00, 25.20)
    b.add_ring("Ring_36", 106.00, 25.20)
    b.add_ring("Ring_37", 108.00, 25.20)
    b.add_ring("Ring_38", 100.00, 28.20)
    b.add_ring("Ring_39", 102.00, 28.20)
    b.add_ring("Ring_40", 104.00, 28.20)
    b.add_spring_vert("SpringV_0", 86.00, 15.50, force=22.00)
    b.add_spring_vert("SpringV_1", 118.00, 15.50, force=22.00)
    b.add_dash_pad("DashPad_0", 60.00, 18.50)
    b.add_cactus("Cactus_0", 34.00, 13.00, speed=1.25)
    b.add_level_finish("Goal_0", 148.00, 35.00)
