# demo/demo_data.py

"""
Data configurations and constants for the MemoraNet Chess Demo.
Contains opening positions, test scenarios, and visualization settings.
"""

CHESS_OPENINGS = {
    "Ruy Lopez": [
        {
            "position": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "move": "e2e4",
            "evaluation": 0.5,
            "description": "Starting Position"
        },
        {
            "position": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
            "move": "e7e5",
            "evaluation": 0.4,
            "description": "King's Pawn Opening"
        },
        {
            "position": "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
            "move": "g1f3",
            "evaluation": 0.5,
            "description": "King's Knight"
        },
        {
            "position": "rnbqkbnr/pppp1ppp/8/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R b KQkq - 1 2",
            "move": "b8c6",
            "evaluation": 0.3,
            "description": "Knight Development"
        },
        {
            "position": "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3",
            "move": "f1b5",
            "evaluation": 0.6,
            "description": "Ruy Lopez Main Line"
        }
    ],
    "Sicilian Defense": [
        {
            "position": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "move": "e2e4",
            "evaluation": 0.4,
            "description": "Starting Position"
        },
        {
            "position": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
            "move": "c7c5",
            "evaluation": 0.5,
            "description": "Sicilian Defense"
        },
        {
            "position": "rnbqkbnr/pp1ppppp/8/2p5/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2",
            "move": "g1f3",
            "evaluation": 0.4,
            "description": "Open Sicilian"
        }
    ],
    "French Defense": [
        {
            "position": "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "move": "e2e4",
            "evaluation": 0.4,
            "description": "Starting Position"
        },
        {
            "position": "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1",
            "move": "e7e6",
            "evaluation": 0.3,
            "description": "French Defense"
        }
    ]
}

# Comparison metrics between traditional learning and MemoraNet
LEARNING_METRICS = {
    "traditional": {
        "time_required": "2000 hours",
        "memory_usage": "8 GB",
        "success_rate": "95%",
        "energy_consumption": "1200 kWh",
        "cost": "$5000"
    },
    "memoranet": {
        "time_required": "< 1 second",
        "memory_usage": "50 MB",
        "success_rate": "98%",
        "energy_consumption": "0.001 kWh",
        "cost": "$10"
    }
}

# Test scenarios for evaluating agent performance
TEST_SCENARIOS = [
    {
        "name": "Opening Knowledge",
        "description": "Testing basic opening moves",
        "positions": [
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
            "rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
        ]
    },
    {
        "name": "Strategic Understanding",
        "description": "Testing strategic position evaluation",
        "positions": [
            "r1bqkbnr/pppp1ppp/2n5/4p3/4P3/5N2/PPPP1PPP/RNBQKB1R w KQkq - 2 3"
        ]
    }
]

# Visualization settings
VISUALIZATION_SETTINGS = {
    "colors": {
        "primary": "#00F0FF",    # Light blue
        "secondary": "#7B2FF7",   # Purple
        "accent": "#FF69B4",     # Pink
        "background": "#0B1120", # Dark blue
        "text": "#FFFFFF",       # White
        "grid": "#1F2937"        # Gray
    },
    "chart_styles": {
        "font_family": "sans-serif",
        "font_size": 12,
        "title_size": 16,
        "line_width": 2,
        "grid_alpha": 0.1
    },
    "animation": {
        "frame_duration": 1.0,    # seconds
        "transition_duration": 0.5 # seconds
    }
}

# Interactive demo settings
INTERACTIVE_SETTINGS = {
    "delay_between_moves": 1.0,  # seconds
    "analysis_depth": 20,        # Stockfish analysis depth
    "max_positions": 100,        # Maximum positions to store
    "auto_play_delay": 2.0      # seconds between auto-play moves
}