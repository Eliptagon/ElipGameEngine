rbmk_rod = r'''
Ra226BE RBMK Neutron Source (from HBM's Nuclear tech mod):
    ╔═══════════════╗
    ║   .-------.   ║
    ║   |       |   ║
    ║   |#######|   ║
    ║   \       /   ║
    ║   |##|R|##|   ║
    ║   |##|A|##|   ║
    ║   |##|2|##|   ║
    ║   |##|2|##|   ║
    ║   |##|6|##|   ║
    ║   |##|B|##|   ║
    ║   |##|E|##|   ║
    ║   /       \   ║
    ║   |#######|   ║
    ║   |       |   ║
    ║   '-------'   ║
    ╚═══════════════╝
    ┌───────────────────────────────────┐
    │ - self-igniting                   │
    │                                   │
    │ - Splits with: Slow Neutrons      │
    │ - Splits into: Slow Neutrons      │
    │                                   │
    │ - Flux Function: 20               │
    │ - Function type: SAFE/PASSIVE     │
    │                                   │
    │ - Xenon gen function: X * 0       │
    │ - Xenon burn function: X^2 / 50   │
    │                                   │
    │ - Heat per flux: 0.035 C          │
    │ - Diffusion: 0.5                  │
    │                                   │
    │ - Melting point: 700              │
    └───────────────────────────────────┘
'''

print(f"Welcome to Eliptagons game engine\nPrepare for bugs.\n Enjoy this Ra226BE rod:\n{rbmk_rod}")
