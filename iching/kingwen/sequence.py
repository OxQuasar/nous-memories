"""
King Wen sequence — the 64 hexagrams in traditional order.

Each hexagram is a 6-bit string, bottom line first (line 1 = LSB).
1 = yang (solid), 0 = yin (broken).

Example: Hexagram 1 (Qian/Creative) = 111111, Hexagram 2 (Kun/Receptive) = 000000
"""

# King Wen sequence: index 0 = hexagram 1, index 63 = hexagram 64
# Each tuple: (number, name, binary bottom-to-top)
KING_WEN = [
    (1,  "Qian",      "111111"),  # Creative
    (2,  "Kun",       "000000"),  # Receptive
    (3,  "Zhun",      "100010"),  # Difficulty at Beginning
    (4,  "Meng",      "010001"),  # Youthful Folly
    (5,  "Xu",        "111010"),  # Waiting
    (6,  "Song",      "010111"),  # Conflict
    (7,  "Shi",       "010000"),  # Army
    (8,  "Bi",        "000010"),  # Holding Together
    (9,  "Xiao Chu",  "111011"),  # Small Taming
    (10, "Lu",        "110111"),  # Treading
    (11, "Tai",       "111000"),  # Peace
    (12, "Pi",        "000111"),  # Standstill
    (13, "Tong Ren",  "101111"),  # Fellowship
    (14, "Da You",    "111101"),  # Great Possession
    (15, "Qian",      "001000"),  # Modesty
    (16, "Yu",        "000100"),  # Enthusiasm
    (17, "Sui",       "100110"),  # Following
    (18, "Gu",        "011001"),  # Decay/Work on What's Spoiled
    (19, "Lin",       "110000"),  # Approach
    (20, "Guan",      "000011"),  # Contemplation
    (21, "Shi He",    "100101"),  # Biting Through
    (22, "Bi",        "101001"),  # Grace
    (23, "Bo",        "000001"),  # Splitting Apart
    (24, "Fu",        "100000"),  # Return
    (25, "Wu Wang",   "100111"),  # Innocence
    (26, "Da Chu",    "111001"),  # Great Taming
    (27, "Yi",        "100001"),  # Nourishment
    (28, "Da Guo",    "011110"),  # Great Exceeding
    (29, "Kan",       "010010"),  # Abysmal Water
    (30, "Li",        "101101"),  # Clinging Fire
    (31, "Xian",      "001110"),  # Influence
    (32, "Heng",      "011100"),  # Duration
    (33, "Dun",       "001111"),  # Retreat
    (34, "Da Zhuang", "111100"),  # Great Power
    (35, "Jin",       "000101"),  # Progress
    (36, "Ming Yi",   "101000"),  # Darkening of the Light
    (37, "Jia Ren",   "101011"),  # The Family
    (38, "Kui",       "110101"),  # Opposition
    (39, "Jian",      "001010"),  # Obstruction
    (40, "Xie",       "010100"),  # Deliverance
    (41, "Sun",       "110001"),  # Decrease
    (42, "Yi",        "100011"),  # Increase
    (43, "Guai",      "111110"),  # Breakthrough
    (44, "Gou",       "011111"),  # Coming to Meet
    (45, "Cui",       "000110"),  # Gathering Together
    (46, "Sheng",     "011000"),  # Pushing Upward
    (47, "Kun",       "010110"),  # Oppression
    (48, "Jing",      "011010"),  # The Well
    (49, "Ge",        "101110"),  # Revolution
    (50, "Ding",      "011101"),  # The Cauldron
    (51, "Zhen",      "100100"),  # Arousing Thunder
    (52, "Gen",       "001001"),  # Keeping Still
    (53, "Jian",      "001011"),  # Development
    (54, "Gui Mei",   "110100"),  # Marrying Maiden
    (55, "Feng",      "101100"),  # Abundance
    (56, "Lu",        "001101"),  # Wanderer
    (57, "Xun",       "011011"),  # Gentle Wind
    (58, "Dui",       "110110"),  # Joyous Lake
    (59, "Huan",      "010011"),  # Dispersion
    (60, "Jie",       "110010"),  # Limitation
    (61, "Zhong Fu",  "110011"),  # Inner Truth
    (62, "Xiao Guo",  "001100"),  # Small Exceeding
    (63, "Ji Ji",     "101010"),  # After Completion
    (64, "Wei Ji",    "010101"),  # Before Completion
]


def bits(hex_idx):
    """Return the 6-bit list for hexagram at index hex_idx (0-based)."""
    return [int(b) for b in KING_WEN[hex_idx][2]]


def name(hex_idx):
    """Return the name for hexagram at index hex_idx (0-based)."""
    return KING_WEN[hex_idx][1]


def number(hex_idx):
    """Return the King Wen number for hexagram at index hex_idx (0-based)."""
    return KING_WEN[hex_idx][0]


def all_bits():
    """Return list of all 64 hexagrams as 6-bit lists."""
    return [bits(i) for i in range(64)]


# Trigram decomposition
TRIGRAMS = {
    "111": "Heaven",
    "000": "Earth",
    "010": "Water",
    "101": "Fire",
    "100": "Thunder",
    "011": "Wind",
    "001": "Mountain",
    "110": "Lake",
}


def lower_trigram(hex_idx):
    """Lower trigram (lines 1-3) as 3-bit string."""
    return KING_WEN[hex_idx][2][:3]


def upper_trigram(hex_idx):
    """Upper trigram (lines 4-6) as 3-bit string."""
    return KING_WEN[hex_idx][2][3:]


def trigram_name(tri):
    """Name for a 3-bit trigram string."""
    return TRIGRAMS.get(tri, "?")
