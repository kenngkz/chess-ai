# piece and symbols
SYMBOL_PIECE_INDEX_MAPPING = {
    "-": 0,
    "p": -1,
    "P": 1,
    "n": -2,
    "N": 2,
    "b": -3,
    "B": 3,
    "r": -4,
    "R": 4,
    "q": -5,
    "Q": 5,
    "k": -6,
    "K": 6,
}

# starting fen
STARTING_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"

# all moves in uci string format
LEN_UCI_MOVES = 1968
UCI_MOVES = {
    "a1a2": 0,
    "a1a3": 1,
    "a1a4": 2,
    "a1a5": 3,
    "a1a6": 4,
    "a1a7": 5,
    "a1a8": 6,
    "a1b1": 7,
    "a1b2": 8,
    "a1b3": 9,
    "a1c1": 10,
    "a1c2": 11,
    "a1c3": 12,
    "a1d1": 13,
    "a1d4": 14,
    "a1e1": 15,
    "a1e5": 16,
    "a1f1": 17,
    "a1f6": 18,
    "a1g1": 19,
    "a1g7": 20,
    "a1h1": 21,
    "a1h8": 22,
    "a2a1": 23,
    "a2a1b": 24,
    "a2a1n": 25,
    "a2a1q": 26,
    "a2a1r": 27,
    "a2a3": 28,
    "a2a4": 29,
    "a2a5": 30,
    "a2a6": 31,
    "a2a7": 32,
    "a2a8": 33,
    "a2b1": 34,
    "a2b1b": 35,
    "a2b1n": 36,
    "a2b1q": 37,
    "a2b1r": 38,
    "a2b2": 39,
    "a2b3": 40,
    "a2b4": 41,
    "a2c1": 42,
    "a2c2": 43,
    "a2c3": 44,
    "a2c4": 45,
    "a2d2": 46,
    "a2d5": 47,
    "a2e2": 48,
    "a2e6": 49,
    "a2f2": 50,
    "a2f7": 51,
    "a2g2": 52,
    "a2g8": 53,
    "a2h2": 54,
    "a3a1": 55,
    "a3a2": 56,
    "a3a4": 57,
    "a3a5": 58,
    "a3a6": 59,
    "a3a7": 60,
    "a3a8": 61,
    "a3b1": 62,
    "a3b2": 63,
    "a3b3": 64,
    "a3b4": 65,
    "a3b5": 66,
    "a3c1": 67,
    "a3c2": 68,
    "a3c3": 69,
    "a3c4": 70,
    "a3c5": 71,
    "a3d3": 72,
    "a3d6": 73,
    "a3e3": 74,
    "a3e7": 75,
    "a3f3": 76,
    "a3f8": 77,
    "a3g3": 78,
    "a3h3": 79,
    "a4a1": 80,
    "a4a2": 81,
    "a4a3": 82,
    "a4a5": 83,
    "a4a6": 84,
    "a4a7": 85,
    "a4a8": 86,
    "a4b2": 87,
    "a4b3": 88,
    "a4b4": 89,
    "a4b5": 90,
    "a4b6": 91,
    "a4c2": 92,
    "a4c3": 93,
    "a4c4": 94,
    "a4c5": 95,
    "a4c6": 96,
    "a4d1": 97,
    "a4d4": 98,
    "a4d7": 99,
    "a4e4": 100,
    "a4e8": 101,
    "a4f4": 102,
    "a4g4": 103,
    "a4h4": 104,
    "a5a1": 105,
    "a5a2": 106,
    "a5a3": 107,
    "a5a4": 108,
    "a5a6": 109,
    "a5a7": 110,
    "a5a8": 111,
    "a5b3": 112,
    "a5b4": 113,
    "a5b5": 114,
    "a5b6": 115,
    "a5b7": 116,
    "a5c3": 117,
    "a5c4": 118,
    "a5c5": 119,
    "a5c6": 120,
    "a5c7": 121,
    "a5d2": 122,
    "a5d5": 123,
    "a5d8": 124,
    "a5e1": 125,
    "a5e5": 126,
    "a5f5": 127,
    "a5g5": 128,
    "a5h5": 129,
    "a6a1": 130,
    "a6a2": 131,
    "a6a3": 132,
    "a6a4": 133,
    "a6a5": 134,
    "a6a7": 135,
    "a6a8": 136,
    "a6b4": 137,
    "a6b5": 138,
    "a6b6": 139,
    "a6b7": 140,
    "a6b8": 141,
    "a6c4": 142,
    "a6c5": 143,
    "a6c6": 144,
    "a6c7": 145,
    "a6c8": 146,
    "a6d3": 147,
    "a6d6": 148,
    "a6e2": 149,
    "a6e6": 150,
    "a6f1": 151,
    "a6f6": 152,
    "a6g6": 153,
    "a6h6": 154,
    "a7a1": 155,
    "a7a2": 156,
    "a7a3": 157,
    "a7a4": 158,
    "a7a5": 159,
    "a7a6": 160,
    "a7a8": 161,
    "a7a8b": 162,
    "a7a8n": 163,
    "a7a8q": 164,
    "a7a8r": 165,
    "a7b5": 166,
    "a7b6": 167,
    "a7b7": 168,
    "a7b8": 169,
    "a7b8b": 170,
    "a7b8n": 171,
    "a7b8q": 172,
    "a7b8r": 173,
    "a7c5": 174,
    "a7c6": 175,
    "a7c7": 176,
    "a7c8": 177,
    "a7d4": 178,
    "a7d7": 179,
    "a7e3": 180,
    "a7e7": 181,
    "a7f2": 182,
    "a7f7": 183,
    "a7g1": 184,
    "a7g7": 185,
    "a7h7": 186,
    "a8a1": 187,
    "a8a2": 188,
    "a8a3": 189,
    "a8a4": 190,
    "a8a5": 191,
    "a8a6": 192,
    "a8a7": 193,
    "a8b6": 194,
    "a8b7": 195,
    "a8b8": 196,
    "a8c6": 197,
    "a8c7": 198,
    "a8c8": 199,
    "a8d5": 200,
    "a8d8": 201,
    "a8e4": 202,
    "a8e8": 203,
    "a8f3": 204,
    "a8f8": 205,
    "a8g2": 206,
    "a8g8": 207,
    "a8h1": 208,
    "a8h8": 209,
    "b1a1": 210,
    "b1a2": 211,
    "b1a3": 212,
    "b1b2": 213,
    "b1b3": 214,
    "b1b4": 215,
    "b1b5": 216,
    "b1b6": 217,
    "b1b7": 218,
    "b1b8": 219,
    "b1c1": 220,
    "b1c2": 221,
    "b1c3": 222,
    "b1d1": 223,
    "b1d2": 224,
    "b1d3": 225,
    "b1e1": 226,
    "b1e4": 227,
    "b1f1": 228,
    "b1f5": 229,
    "b1g1": 230,
    "b1g6": 231,
    "b1h1": 232,
    "b1h7": 233,
    "b2a1": 234,
    "b2a1b": 235,
    "b2a1n": 236,
    "b2a1q": 237,
    "b2a1r": 238,
    "b2a2": 239,
    "b2a3": 240,
    "b2a4": 241,
    "b2b1": 242,
    "b2b1b": 243,
    "b2b1n": 244,
    "b2b1q": 245,
    "b2b1r": 246,
    "b2b3": 247,
    "b2b4": 248,
    "b2b5": 249,
    "b2b6": 250,
    "b2b7": 251,
    "b2b8": 252,
    "b2c1": 253,
    "b2c1b": 254,
    "b2c1n": 255,
    "b2c1q": 256,
    "b2c1r": 257,
    "b2c2": 258,
    "b2c3": 259,
    "b2c4": 260,
    "b2d1": 261,
    "b2d2": 262,
    "b2d3": 263,
    "b2d4": 264,
    "b2e2": 265,
    "b2e5": 266,
    "b2f2": 267,
    "b2f6": 268,
    "b2g2": 269,
    "b2g7": 270,
    "b2h2": 271,
    "b2h8": 272,
    "b3a1": 273,
    "b3a2": 274,
    "b3a3": 275,
    "b3a4": 276,
    "b3a5": 277,
    "b3b1": 278,
    "b3b2": 279,
    "b3b4": 280,
    "b3b5": 281,
    "b3b6": 282,
    "b3b7": 283,
    "b3b8": 284,
    "b3c1": 285,
    "b3c2": 286,
    "b3c3": 287,
    "b3c4": 288,
    "b3c5": 289,
    "b3d1": 290,
    "b3d2": 291,
    "b3d3": 292,
    "b3d4": 293,
    "b3d5": 294,
    "b3e3": 295,
    "b3e6": 296,
    "b3f3": 297,
    "b3f7": 298,
    "b3g3": 299,
    "b3g8": 300,
    "b3h3": 301,
    "b4a2": 302,
    "b4a3": 303,
    "b4a4": 304,
    "b4a5": 305,
    "b4a6": 306,
    "b4b1": 307,
    "b4b2": 308,
    "b4b3": 309,
    "b4b5": 310,
    "b4b6": 311,
    "b4b7": 312,
    "b4b8": 313,
    "b4c2": 314,
    "b4c3": 315,
    "b4c4": 316,
    "b4c5": 317,
    "b4c6": 318,
    "b4d2": 319,
    "b4d3": 320,
    "b4d4": 321,
    "b4d5": 322,
    "b4d6": 323,
    "b4e1": 324,
    "b4e4": 325,
    "b4e7": 326,
    "b4f4": 327,
    "b4f8": 328,
    "b4g4": 329,
    "b4h4": 330,
    "b5a3": 331,
    "b5a4": 332,
    "b5a5": 333,
    "b5a6": 334,
    "b5a7": 335,
    "b5b1": 336,
    "b5b2": 337,
    "b5b3": 338,
    "b5b4": 339,
    "b5b6": 340,
    "b5b7": 341,
    "b5b8": 342,
    "b5c3": 343,
    "b5c4": 344,
    "b5c5": 345,
    "b5c6": 346,
    "b5c7": 347,
    "b5d3": 348,
    "b5d4": 349,
    "b5d5": 350,
    "b5d6": 351,
    "b5d7": 352,
    "b5e2": 353,
    "b5e5": 354,
    "b5e8": 355,
    "b5f1": 356,
    "b5f5": 357,
    "b5g5": 358,
    "b5h5": 359,
    "b6a4": 360,
    "b6a5": 361,
    "b6a6": 362,
    "b6a7": 363,
    "b6a8": 364,
    "b6b1": 365,
    "b6b2": 366,
    "b6b3": 367,
    "b6b4": 368,
    "b6b5": 369,
    "b6b7": 370,
    "b6b8": 371,
    "b6c4": 372,
    "b6c5": 373,
    "b6c6": 374,
    "b6c7": 375,
    "b6c8": 376,
    "b6d4": 377,
    "b6d5": 378,
    "b6d6": 379,
    "b6d7": 380,
    "b6d8": 381,
    "b6e3": 382,
    "b6e6": 383,
    "b6f2": 384,
    "b6f6": 385,
    "b6g1": 386,
    "b6g6": 387,
    "b6h6": 388,
    "b7a5": 389,
    "b7a6": 390,
    "b7a7": 391,
    "b7a8": 392,
    "b7a8b": 393,
    "b7a8n": 394,
    "b7a8q": 395,
    "b7a8r": 396,
    "b7b1": 397,
    "b7b2": 398,
    "b7b3": 399,
    "b7b4": 400,
    "b7b5": 401,
    "b7b6": 402,
    "b7b8": 403,
    "b7b8b": 404,
    "b7b8n": 405,
    "b7b8q": 406,
    "b7b8r": 407,
    "b7c5": 408,
    "b7c6": 409,
    "b7c7": 410,
    "b7c8": 411,
    "b7c8b": 412,
    "b7c8n": 413,
    "b7c8q": 414,
    "b7c8r": 415,
    "b7d5": 416,
    "b7d6": 417,
    "b7d7": 418,
    "b7d8": 419,
    "b7e4": 420,
    "b7e7": 421,
    "b7f3": 422,
    "b7f7": 423,
    "b7g2": 424,
    "b7g7": 425,
    "b7h1": 426,
    "b7h7": 427,
    "b8a6": 428,
    "b8a7": 429,
    "b8a8": 430,
    "b8b1": 431,
    "b8b2": 432,
    "b8b3": 433,
    "b8b4": 434,
    "b8b5": 435,
    "b8b6": 436,
    "b8b7": 437,
    "b8c6": 438,
    "b8c7": 439,
    "b8c8": 440,
    "b8d6": 441,
    "b8d7": 442,
    "b8d8": 443,
    "b8e5": 444,
    "b8e8": 445,
    "b8f4": 446,
    "b8f8": 447,
    "b8g3": 448,
    "b8g8": 449,
    "b8h2": 450,
    "b8h8": 451,
    "c1a1": 452,
    "c1a2": 453,
    "c1a3": 454,
    "c1b1": 455,
    "c1b2": 456,
    "c1b3": 457,
    "c1c2": 458,
    "c1c3": 459,
    "c1c4": 460,
    "c1c5": 461,
    "c1c6": 462,
    "c1c7": 463,
    "c1c8": 464,
    "c1d1": 465,
    "c1d2": 466,
    "c1d3": 467,
    "c1e1": 468,
    "c1e2": 469,
    "c1e3": 470,
    "c1f1": 471,
    "c1f4": 472,
    "c1g1": 473,
    "c1g5": 474,
    "c1h1": 475,
    "c1h6": 476,
    "c2a1": 477,
    "c2a2": 478,
    "c2a3": 479,
    "c2a4": 480,
    "c2b1": 481,
    "c2b1b": 482,
    "c2b1n": 483,
    "c2b1q": 484,
    "c2b1r": 485,
    "c2b2": 486,
    "c2b3": 487,
    "c2b4": 488,
    "c2c1": 489,
    "c2c1b": 490,
    "c2c1n": 491,
    "c2c1q": 492,
    "c2c1r": 493,
    "c2c3": 494,
    "c2c4": 495,
    "c2c5": 496,
    "c2c6": 497,
    "c2c7": 498,
    "c2c8": 499,
    "c2d1": 500,
    "c2d1b": 501,
    "c2d1n": 502,
    "c2d1q": 503,
    "c2d1r": 504,
    "c2d2": 505,
    "c2d3": 506,
    "c2d4": 507,
    "c2e1": 508,
    "c2e2": 509,
    "c2e3": 510,
    "c2e4": 511,
    "c2f2": 512,
    "c2f5": 513,
    "c2g2": 514,
    "c2g6": 515,
    "c2h2": 516,
    "c2h7": 517,
    "c3a1": 518,
    "c3a2": 519,
    "c3a3": 520,
    "c3a4": 521,
    "c3a5": 522,
    "c3b1": 523,
    "c3b2": 524,
    "c3b3": 525,
    "c3b4": 526,
    "c3b5": 527,
    "c3c1": 528,
    "c3c2": 529,
    "c3c4": 530,
    "c3c5": 531,
    "c3c6": 532,
    "c3c7": 533,
    "c3c8": 534,
    "c3d1": 535,
    "c3d2": 536,
    "c3d3": 537,
    "c3d4": 538,
    "c3d5": 539,
    "c3e1": 540,
    "c3e2": 541,
    "c3e3": 542,
    "c3e4": 543,
    "c3e5": 544,
    "c3f3": 545,
    "c3f6": 546,
    "c3g3": 547,
    "c3g7": 548,
    "c3h3": 549,
    "c3h8": 550,
    "c4a2": 551,
    "c4a3": 552,
    "c4a4": 553,
    "c4a5": 554,
    "c4a6": 555,
    "c4b2": 556,
    "c4b3": 557,
    "c4b4": 558,
    "c4b5": 559,
    "c4b6": 560,
    "c4c1": 561,
    "c4c2": 562,
    "c4c3": 563,
    "c4c5": 564,
    "c4c6": 565,
    "c4c7": 566,
    "c4c8": 567,
    "c4d2": 568,
    "c4d3": 569,
    "c4d4": 570,
    "c4d5": 571,
    "c4d6": 572,
    "c4e2": 573,
    "c4e3": 574,
    "c4e4": 575,
    "c4e5": 576,
    "c4e6": 577,
    "c4f1": 578,
    "c4f4": 579,
    "c4f7": 580,
    "c4g4": 581,
    "c4g8": 582,
    "c4h4": 583,
    "c5a3": 584,
    "c5a4": 585,
    "c5a5": 586,
    "c5a6": 587,
    "c5a7": 588,
    "c5b3": 589,
    "c5b4": 590,
    "c5b5": 591,
    "c5b6": 592,
    "c5b7": 593,
    "c5c1": 594,
    "c5c2": 595,
    "c5c3": 596,
    "c5c4": 597,
    "c5c6": 598,
    "c5c7": 599,
    "c5c8": 600,
    "c5d3": 601,
    "c5d4": 602,
    "c5d5": 603,
    "c5d6": 604,
    "c5d7": 605,
    "c5e3": 606,
    "c5e4": 607,
    "c5e5": 608,
    "c5e6": 609,
    "c5e7": 610,
    "c5f2": 611,
    "c5f5": 612,
    "c5f8": 613,
    "c5g1": 614,
    "c5g5": 615,
    "c5h5": 616,
    "c6a4": 617,
    "c6a5": 618,
    "c6a6": 619,
    "c6a7": 620,
    "c6a8": 621,
    "c6b4": 622,
    "c6b5": 623,
    "c6b6": 624,
    "c6b7": 625,
    "c6b8": 626,
    "c6c1": 627,
    "c6c2": 628,
    "c6c3": 629,
    "c6c4": 630,
    "c6c5": 631,
    "c6c7": 632,
    "c6c8": 633,
    "c6d4": 634,
    "c6d5": 635,
    "c6d6": 636,
    "c6d7": 637,
    "c6d8": 638,
    "c6e4": 639,
    "c6e5": 640,
    "c6e6": 641,
    "c6e7": 642,
    "c6e8": 643,
    "c6f3": 644,
    "c6f6": 645,
    "c6g2": 646,
    "c6g6": 647,
    "c6h1": 648,
    "c6h6": 649,
    "c7a5": 650,
    "c7a6": 651,
    "c7a7": 652,
    "c7a8": 653,
    "c7b5": 654,
    "c7b6": 655,
    "c7b7": 656,
    "c7b8": 657,
    "c7b8b": 658,
    "c7b8n": 659,
    "c7b8q": 660,
    "c7b8r": 661,
    "c7c1": 662,
    "c7c2": 663,
    "c7c3": 664,
    "c7c4": 665,
    "c7c5": 666,
    "c7c6": 667,
    "c7c8": 668,
    "c7c8b": 669,
    "c7c8n": 670,
    "c7c8q": 671,
    "c7c8r": 672,
    "c7d5": 673,
    "c7d6": 674,
    "c7d7": 675,
    "c7d8": 676,
    "c7d8b": 677,
    "c7d8n": 678,
    "c7d8q": 679,
    "c7d8r": 680,
    "c7e5": 681,
    "c7e6": 682,
    "c7e7": 683,
    "c7e8": 684,
    "c7f4": 685,
    "c7f7": 686,
    "c7g3": 687,
    "c7g7": 688,
    "c7h2": 689,
    "c7h7": 690,
    "c8a6": 691,
    "c8a7": 692,
    "c8a8": 693,
    "c8b6": 694,
    "c8b7": 695,
    "c8b8": 696,
    "c8c1": 697,
    "c8c2": 698,
    "c8c3": 699,
    "c8c4": 700,
    "c8c5": 701,
    "c8c6": 702,
    "c8c7": 703,
    "c8d6": 704,
    "c8d7": 705,
    "c8d8": 706,
    "c8e6": 707,
    "c8e7": 708,
    "c8e8": 709,
    "c8f5": 710,
    "c8f8": 711,
    "c8g4": 712,
    "c8g8": 713,
    "c8h3": 714,
    "c8h8": 715,
    "d1a1": 716,
    "d1a4": 717,
    "d1b1": 718,
    "d1b2": 719,
    "d1b3": 720,
    "d1c1": 721,
    "d1c2": 722,
    "d1c3": 723,
    "d1d2": 724,
    "d1d3": 725,
    "d1d4": 726,
    "d1d5": 727,
    "d1d6": 728,
    "d1d7": 729,
    "d1d8": 730,
    "d1e1": 731,
    "d1e2": 732,
    "d1e3": 733,
    "d1f1": 734,
    "d1f2": 735,
    "d1f3": 736,
    "d1g1": 737,
    "d1g4": 738,
    "d1h1": 739,
    "d1h5": 740,
    "d2a2": 741,
    "d2a5": 742,
    "d2b1": 743,
    "d2b2": 744,
    "d2b3": 745,
    "d2b4": 746,
    "d2c1": 747,
    "d2c1b": 748,
    "d2c1n": 749,
    "d2c1q": 750,
    "d2c1r": 751,
    "d2c2": 752,
    "d2c3": 753,
    "d2c4": 754,
    "d2d1": 755,
    "d2d1b": 756,
    "d2d1n": 757,
    "d2d1q": 758,
    "d2d1r": 759,
    "d2d3": 760,
    "d2d4": 761,
    "d2d5": 762,
    "d2d6": 763,
    "d2d7": 764,
    "d2d8": 765,
    "d2e1": 766,
    "d2e1b": 767,
    "d2e1n": 768,
    "d2e1q": 769,
    "d2e1r": 770,
    "d2e2": 771,
    "d2e3": 772,
    "d2e4": 773,
    "d2f1": 774,
    "d2f2": 775,
    "d2f3": 776,
    "d2f4": 777,
    "d2g2": 778,
    "d2g5": 779,
    "d2h2": 780,
    "d2h6": 781,
    "d3a3": 782,
    "d3a6": 783,
    "d3b1": 784,
    "d3b2": 785,
    "d3b3": 786,
    "d3b4": 787,
    "d3b5": 788,
    "d3c1": 789,
    "d3c2": 790,
    "d3c3": 791,
    "d3c4": 792,
    "d3c5": 793,
    "d3d1": 794,
    "d3d2": 795,
    "d3d4": 796,
    "d3d5": 797,
    "d3d6": 798,
    "d3d7": 799,
    "d3d8": 800,
    "d3e1": 801,
    "d3e2": 802,
    "d3e3": 803,
    "d3e4": 804,
    "d3e5": 805,
    "d3f1": 806,
    "d3f2": 807,
    "d3f3": 808,
    "d3f4": 809,
    "d3f5": 810,
    "d3g3": 811,
    "d3g6": 812,
    "d3h3": 813,
    "d3h7": 814,
    "d4a1": 815,
    "d4a4": 816,
    "d4a7": 817,
    "d4b2": 818,
    "d4b3": 819,
    "d4b4": 820,
    "d4b5": 821,
    "d4b6": 822,
    "d4c2": 823,
    "d4c3": 824,
    "d4c4": 825,
    "d4c5": 826,
    "d4c6": 827,
    "d4d1": 828,
    "d4d2": 829,
    "d4d3": 830,
    "d4d5": 831,
    "d4d6": 832,
    "d4d7": 833,
    "d4d8": 834,
    "d4e2": 835,
    "d4e3": 836,
    "d4e4": 837,
    "d4e5": 838,
    "d4e6": 839,
    "d4f2": 840,
    "d4f3": 841,
    "d4f4": 842,
    "d4f5": 843,
    "d4f6": 844,
    "d4g1": 845,
    "d4g4": 846,
    "d4g7": 847,
    "d4h4": 848,
    "d4h8": 849,
    "d5a2": 850,
    "d5a5": 851,
    "d5a8": 852,
    "d5b3": 853,
    "d5b4": 854,
    "d5b5": 855,
    "d5b6": 856,
    "d5b7": 857,
    "d5c3": 858,
    "d5c4": 859,
    "d5c5": 860,
    "d5c6": 861,
    "d5c7": 862,
    "d5d1": 863,
    "d5d2": 864,
    "d5d3": 865,
    "d5d4": 866,
    "d5d6": 867,
    "d5d7": 868,
    "d5d8": 869,
    "d5e3": 870,
    "d5e4": 871,
    "d5e5": 872,
    "d5e6": 873,
    "d5e7": 874,
    "d5f3": 875,
    "d5f4": 876,
    "d5f5": 877,
    "d5f6": 878,
    "d5f7": 879,
    "d5g2": 880,
    "d5g5": 881,
    "d5g8": 882,
    "d5h1": 883,
    "d5h5": 884,
    "d6a3": 885,
    "d6a6": 886,
    "d6b4": 887,
    "d6b5": 888,
    "d6b6": 889,
    "d6b7": 890,
    "d6b8": 891,
    "d6c4": 892,
    "d6c5": 893,
    "d6c6": 894,
    "d6c7": 895,
    "d6c8": 896,
    "d6d1": 897,
    "d6d2": 898,
    "d6d3": 899,
    "d6d4": 900,
    "d6d5": 901,
    "d6d7": 902,
    "d6d8": 903,
    "d6e4": 904,
    "d6e5": 905,
    "d6e6": 906,
    "d6e7": 907,
    "d6e8": 908,
    "d6f4": 909,
    "d6f5": 910,
    "d6f6": 911,
    "d6f7": 912,
    "d6f8": 913,
    "d6g3": 914,
    "d6g6": 915,
    "d6h2": 916,
    "d6h6": 917,
    "d7a4": 918,
    "d7a7": 919,
    "d7b5": 920,
    "d7b6": 921,
    "d7b7": 922,
    "d7b8": 923,
    "d7c5": 924,
    "d7c6": 925,
    "d7c7": 926,
    "d7c8": 927,
    "d7c8b": 928,
    "d7c8n": 929,
    "d7c8q": 930,
    "d7c8r": 931,
    "d7d1": 932,
    "d7d2": 933,
    "d7d3": 934,
    "d7d4": 935,
    "d7d5": 936,
    "d7d6": 937,
    "d7d8": 938,
    "d7d8b": 939,
    "d7d8n": 940,
    "d7d8q": 941,
    "d7d8r": 942,
    "d7e5": 943,
    "d7e6": 944,
    "d7e7": 945,
    "d7e8": 946,
    "d7e8b": 947,
    "d7e8n": 948,
    "d7e8q": 949,
    "d7e8r": 950,
    "d7f5": 951,
    "d7f6": 952,
    "d7f7": 953,
    "d7f8": 954,
    "d7g4": 955,
    "d7g7": 956,
    "d7h3": 957,
    "d7h7": 958,
    "d8a5": 959,
    "d8a8": 960,
    "d8b6": 961,
    "d8b7": 962,
    "d8b8": 963,
    "d8c6": 964,
    "d8c7": 965,
    "d8c8": 966,
    "d8d1": 967,
    "d8d2": 968,
    "d8d3": 969,
    "d8d4": 970,
    "d8d5": 971,
    "d8d6": 972,
    "d8d7": 973,
    "d8e6": 974,
    "d8e7": 975,
    "d8e8": 976,
    "d8f6": 977,
    "d8f7": 978,
    "d8f8": 979,
    "d8g5": 980,
    "d8g8": 981,
    "d8h4": 982,
    "d8h8": 983,
    "e1a1": 984,
    "e1a5": 985,
    "e1b1": 986,
    "e1b4": 987,
    "e1c1": 988,
    "e1c2": 989,
    "e1c3": 990,
    "e1d1": 991,
    "e1d2": 992,
    "e1d3": 993,
    "e1e2": 994,
    "e1e3": 995,
    "e1e4": 996,
    "e1e5": 997,
    "e1e6": 998,
    "e1e7": 999,
    "e1e8": 1000,
    "e1f1": 1001,
    "e1f2": 1002,
    "e1f3": 1003,
    "e1g1": 1004,
    "e1g2": 1005,
    "e1g3": 1006,
    "e1h1": 1007,
    "e1h4": 1008,
    "e2a2": 1009,
    "e2a6": 1010,
    "e2b2": 1011,
    "e2b5": 1012,
    "e2c1": 1013,
    "e2c2": 1014,
    "e2c3": 1015,
    "e2c4": 1016,
    "e2d1": 1017,
    "e2d1b": 1018,
    "e2d1n": 1019,
    "e2d1q": 1020,
    "e2d1r": 1021,
    "e2d2": 1022,
    "e2d3": 1023,
    "e2d4": 1024,
    "e2e1": 1025,
    "e2e1b": 1026,
    "e2e1n": 1027,
    "e2e1q": 1028,
    "e2e1r": 1029,
    "e2e3": 1030,
    "e2e4": 1031,
    "e2e5": 1032,
    "e2e6": 1033,
    "e2e7": 1034,
    "e2e8": 1035,
    "e2f1": 1036,
    "e2f1b": 1037,
    "e2f1n": 1038,
    "e2f1q": 1039,
    "e2f1r": 1040,
    "e2f2": 1041,
    "e2f3": 1042,
    "e2f4": 1043,
    "e2g1": 1044,
    "e2g2": 1045,
    "e2g3": 1046,
    "e2g4": 1047,
    "e2h2": 1048,
    "e2h5": 1049,
    "e3a3": 1050,
    "e3a7": 1051,
    "e3b3": 1052,
    "e3b6": 1053,
    "e3c1": 1054,
    "e3c2": 1055,
    "e3c3": 1056,
    "e3c4": 1057,
    "e3c5": 1058,
    "e3d1": 1059,
    "e3d2": 1060,
    "e3d3": 1061,
    "e3d4": 1062,
    "e3d5": 1063,
    "e3e1": 1064,
    "e3e2": 1065,
    "e3e4": 1066,
    "e3e5": 1067,
    "e3e6": 1068,
    "e3e7": 1069,
    "e3e8": 1070,
    "e3f1": 1071,
    "e3f2": 1072,
    "e3f3": 1073,
    "e3f4": 1074,
    "e3f5": 1075,
    "e3g1": 1076,
    "e3g2": 1077,
    "e3g3": 1078,
    "e3g4": 1079,
    "e3g5": 1080,
    "e3h3": 1081,
    "e3h6": 1082,
    "e4a4": 1083,
    "e4a8": 1084,
    "e4b1": 1085,
    "e4b4": 1086,
    "e4b7": 1087,
    "e4c2": 1088,
    "e4c3": 1089,
    "e4c4": 1090,
    "e4c5": 1091,
    "e4c6": 1092,
    "e4d2": 1093,
    "e4d3": 1094,
    "e4d4": 1095,
    "e4d5": 1096,
    "e4d6": 1097,
    "e4e1": 1098,
    "e4e2": 1099,
    "e4e3": 1100,
    "e4e5": 1101,
    "e4e6": 1102,
    "e4e7": 1103,
    "e4e8": 1104,
    "e4f2": 1105,
    "e4f3": 1106,
    "e4f4": 1107,
    "e4f5": 1108,
    "e4f6": 1109,
    "e4g2": 1110,
    "e4g3": 1111,
    "e4g4": 1112,
    "e4g5": 1113,
    "e4g6": 1114,
    "e4h1": 1115,
    "e4h4": 1116,
    "e4h7": 1117,
    "e5a1": 1118,
    "e5a5": 1119,
    "e5b2": 1120,
    "e5b5": 1121,
    "e5b8": 1122,
    "e5c3": 1123,
    "e5c4": 1124,
    "e5c5": 1125,
    "e5c6": 1126,
    "e5c7": 1127,
    "e5d3": 1128,
    "e5d4": 1129,
    "e5d5": 1130,
    "e5d6": 1131,
    "e5d7": 1132,
    "e5e1": 1133,
    "e5e2": 1134,
    "e5e3": 1135,
    "e5e4": 1136,
    "e5e6": 1137,
    "e5e7": 1138,
    "e5e8": 1139,
    "e5f3": 1140,
    "e5f4": 1141,
    "e5f5": 1142,
    "e5f6": 1143,
    "e5f7": 1144,
    "e5g3": 1145,
    "e5g4": 1146,
    "e5g5": 1147,
    "e5g6": 1148,
    "e5g7": 1149,
    "e5h2": 1150,
    "e5h5": 1151,
    "e5h8": 1152,
    "e6a2": 1153,
    "e6a6": 1154,
    "e6b3": 1155,
    "e6b6": 1156,
    "e6c4": 1157,
    "e6c5": 1158,
    "e6c6": 1159,
    "e6c7": 1160,
    "e6c8": 1161,
    "e6d4": 1162,
    "e6d5": 1163,
    "e6d6": 1164,
    "e6d7": 1165,
    "e6d8": 1166,
    "e6e1": 1167,
    "e6e2": 1168,
    "e6e3": 1169,
    "e6e4": 1170,
    "e6e5": 1171,
    "e6e7": 1172,
    "e6e8": 1173,
    "e6f4": 1174,
    "e6f5": 1175,
    "e6f6": 1176,
    "e6f7": 1177,
    "e6f8": 1178,
    "e6g4": 1179,
    "e6g5": 1180,
    "e6g6": 1181,
    "e6g7": 1182,
    "e6g8": 1183,
    "e6h3": 1184,
    "e6h6": 1185,
    "e7a3": 1186,
    "e7a7": 1187,
    "e7b4": 1188,
    "e7b7": 1189,
    "e7c5": 1190,
    "e7c6": 1191,
    "e7c7": 1192,
    "e7c8": 1193,
    "e7d5": 1194,
    "e7d6": 1195,
    "e7d7": 1196,
    "e7d8": 1197,
    "e7d8b": 1198,
    "e7d8n": 1199,
    "e7d8q": 1200,
    "e7d8r": 1201,
    "e7e1": 1202,
    "e7e2": 1203,
    "e7e3": 1204,
    "e7e4": 1205,
    "e7e5": 1206,
    "e7e6": 1207,
    "e7e8": 1208,
    "e7e8b": 1209,
    "e7e8n": 1210,
    "e7e8q": 1211,
    "e7e8r": 1212,
    "e7f5": 1213,
    "e7f6": 1214,
    "e7f7": 1215,
    "e7f8": 1216,
    "e7f8b": 1217,
    "e7f8n": 1218,
    "e7f8q": 1219,
    "e7f8r": 1220,
    "e7g5": 1221,
    "e7g6": 1222,
    "e7g7": 1223,
    "e7g8": 1224,
    "e7h4": 1225,
    "e7h7": 1226,
    "e8a4": 1227,
    "e8a8": 1228,
    "e8b5": 1229,
    "e8b8": 1230,
    "e8c6": 1231,
    "e8c7": 1232,
    "e8c8": 1233,
    "e8d6": 1234,
    "e8d7": 1235,
    "e8d8": 1236,
    "e8e1": 1237,
    "e8e2": 1238,
    "e8e3": 1239,
    "e8e4": 1240,
    "e8e5": 1241,
    "e8e6": 1242,
    "e8e7": 1243,
    "e8f6": 1244,
    "e8f7": 1245,
    "e8f8": 1246,
    "e8g6": 1247,
    "e8g7": 1248,
    "e8g8": 1249,
    "e8h5": 1250,
    "e8h8": 1251,
    "f1a1": 1252,
    "f1a6": 1253,
    "f1b1": 1254,
    "f1b5": 1255,
    "f1c1": 1256,
    "f1c4": 1257,
    "f1d1": 1258,
    "f1d2": 1259,
    "f1d3": 1260,
    "f1e1": 1261,
    "f1e2": 1262,
    "f1e3": 1263,
    "f1f2": 1264,
    "f1f3": 1265,
    "f1f4": 1266,
    "f1f5": 1267,
    "f1f6": 1268,
    "f1f7": 1269,
    "f1f8": 1270,
    "f1g1": 1271,
    "f1g2": 1272,
    "f1g3": 1273,
    "f1h1": 1274,
    "f1h2": 1275,
    "f1h3": 1276,
    "f2a2": 1277,
    "f2a7": 1278,
    "f2b2": 1279,
    "f2b6": 1280,
    "f2c2": 1281,
    "f2c5": 1282,
    "f2d1": 1283,
    "f2d2": 1284,
    "f2d3": 1285,
    "f2d4": 1286,
    "f2e1": 1287,
    "f2e1b": 1288,
    "f2e1n": 1289,
    "f2e1q": 1290,
    "f2e1r": 1291,
    "f2e2": 1292,
    "f2e3": 1293,
    "f2e4": 1294,
    "f2f1": 1295,
    "f2f1b": 1296,
    "f2f1n": 1297,
    "f2f1q": 1298,
    "f2f1r": 1299,
    "f2f3": 1300,
    "f2f4": 1301,
    "f2f5": 1302,
    "f2f6": 1303,
    "f2f7": 1304,
    "f2f8": 1305,
    "f2g1": 1306,
    "f2g1b": 1307,
    "f2g1n": 1308,
    "f2g1q": 1309,
    "f2g1r": 1310,
    "f2g2": 1311,
    "f2g3": 1312,
    "f2g4": 1313,
    "f2h1": 1314,
    "f2h2": 1315,
    "f2h3": 1316,
    "f2h4": 1317,
    "f3a3": 1318,
    "f3a8": 1319,
    "f3b3": 1320,
    "f3b7": 1321,
    "f3c3": 1322,
    "f3c6": 1323,
    "f3d1": 1324,
    "f3d2": 1325,
    "f3d3": 1326,
    "f3d4": 1327,
    "f3d5": 1328,
    "f3e1": 1329,
    "f3e2": 1330,
    "f3e3": 1331,
    "f3e4": 1332,
    "f3e5": 1333,
    "f3f1": 1334,
    "f3f2": 1335,
    "f3f4": 1336,
    "f3f5": 1337,
    "f3f6": 1338,
    "f3f7": 1339,
    "f3f8": 1340,
    "f3g1": 1341,
    "f3g2": 1342,
    "f3g3": 1343,
    "f3g4": 1344,
    "f3g5": 1345,
    "f3h1": 1346,
    "f3h2": 1347,
    "f3h3": 1348,
    "f3h4": 1349,
    "f3h5": 1350,
    "f4a4": 1351,
    "f4b4": 1352,
    "f4b8": 1353,
    "f4c1": 1354,
    "f4c4": 1355,
    "f4c7": 1356,
    "f4d2": 1357,
    "f4d3": 1358,
    "f4d4": 1359,
    "f4d5": 1360,
    "f4d6": 1361,
    "f4e2": 1362,
    "f4e3": 1363,
    "f4e4": 1364,
    "f4e5": 1365,
    "f4e6": 1366,
    "f4f1": 1367,
    "f4f2": 1368,
    "f4f3": 1369,
    "f4f5": 1370,
    "f4f6": 1371,
    "f4f7": 1372,
    "f4f8": 1373,
    "f4g2": 1374,
    "f4g3": 1375,
    "f4g4": 1376,
    "f4g5": 1377,
    "f4g6": 1378,
    "f4h2": 1379,
    "f4h3": 1380,
    "f4h4": 1381,
    "f4h5": 1382,
    "f4h6": 1383,
    "f5a5": 1384,
    "f5b1": 1385,
    "f5b5": 1386,
    "f5c2": 1387,
    "f5c5": 1388,
    "f5c8": 1389,
    "f5d3": 1390,
    "f5d4": 1391,
    "f5d5": 1392,
    "f5d6": 1393,
    "f5d7": 1394,
    "f5e3": 1395,
    "f5e4": 1396,
    "f5e5": 1397,
    "f5e6": 1398,
    "f5e7": 1399,
    "f5f1": 1400,
    "f5f2": 1401,
    "f5f3": 1402,
    "f5f4": 1403,
    "f5f6": 1404,
    "f5f7": 1405,
    "f5f8": 1406,
    "f5g3": 1407,
    "f5g4": 1408,
    "f5g5": 1409,
    "f5g6": 1410,
    "f5g7": 1411,
    "f5h3": 1412,
    "f5h4": 1413,
    "f5h5": 1414,
    "f5h6": 1415,
    "f5h7": 1416,
    "f6a1": 1417,
    "f6a6": 1418,
    "f6b2": 1419,
    "f6b6": 1420,
    "f6c3": 1421,
    "f6c6": 1422,
    "f6d4": 1423,
    "f6d5": 1424,
    "f6d6": 1425,
    "f6d7": 1426,
    "f6d8": 1427,
    "f6e4": 1428,
    "f6e5": 1429,
    "f6e6": 1430,
    "f6e7": 1431,
    "f6e8": 1432,
    "f6f1": 1433,
    "f6f2": 1434,
    "f6f3": 1435,
    "f6f4": 1436,
    "f6f5": 1437,
    "f6f7": 1438,
    "f6f8": 1439,
    "f6g4": 1440,
    "f6g5": 1441,
    "f6g6": 1442,
    "f6g7": 1443,
    "f6g8": 1444,
    "f6h4": 1445,
    "f6h5": 1446,
    "f6h6": 1447,
    "f6h7": 1448,
    "f6h8": 1449,
    "f7a2": 1450,
    "f7a7": 1451,
    "f7b3": 1452,
    "f7b7": 1453,
    "f7c4": 1454,
    "f7c7": 1455,
    "f7d5": 1456,
    "f7d6": 1457,
    "f7d7": 1458,
    "f7d8": 1459,
    "f7e5": 1460,
    "f7e6": 1461,
    "f7e7": 1462,
    "f7e8": 1463,
    "f7e8b": 1464,
    "f7e8n": 1465,
    "f7e8q": 1466,
    "f7e8r": 1467,
    "f7f1": 1468,
    "f7f2": 1469,
    "f7f3": 1470,
    "f7f4": 1471,
    "f7f5": 1472,
    "f7f6": 1473,
    "f7f8": 1474,
    "f7f8b": 1475,
    "f7f8n": 1476,
    "f7f8q": 1477,
    "f7f8r": 1478,
    "f7g5": 1479,
    "f7g6": 1480,
    "f7g7": 1481,
    "f7g8": 1482,
    "f7g8b": 1483,
    "f7g8n": 1484,
    "f7g8q": 1485,
    "f7g8r": 1486,
    "f7h5": 1487,
    "f7h6": 1488,
    "f7h7": 1489,
    "f7h8": 1490,
    "f8a3": 1491,
    "f8a8": 1492,
    "f8b4": 1493,
    "f8b8": 1494,
    "f8c5": 1495,
    "f8c8": 1496,
    "f8d6": 1497,
    "f8d7": 1498,
    "f8d8": 1499,
    "f8e6": 1500,
    "f8e7": 1501,
    "f8e8": 1502,
    "f8f1": 1503,
    "f8f2": 1504,
    "f8f3": 1505,
    "f8f4": 1506,
    "f8f5": 1507,
    "f8f6": 1508,
    "f8f7": 1509,
    "f8g6": 1510,
    "f8g7": 1511,
    "f8g8": 1512,
    "f8h6": 1513,
    "f8h7": 1514,
    "f8h8": 1515,
    "g1a1": 1516,
    "g1a7": 1517,
    "g1b1": 1518,
    "g1b6": 1519,
    "g1c1": 1520,
    "g1c5": 1521,
    "g1d1": 1522,
    "g1d4": 1523,
    "g1e1": 1524,
    "g1e2": 1525,
    "g1e3": 1526,
    "g1f1": 1527,
    "g1f2": 1528,
    "g1f3": 1529,
    "g1g2": 1530,
    "g1g3": 1531,
    "g1g4": 1532,
    "g1g5": 1533,
    "g1g6": 1534,
    "g1g7": 1535,
    "g1g8": 1536,
    "g1h1": 1537,
    "g1h2": 1538,
    "g1h3": 1539,
    "g2a2": 1540,
    "g2a8": 1541,
    "g2b2": 1542,
    "g2b7": 1543,
    "g2c2": 1544,
    "g2c6": 1545,
    "g2d2": 1546,
    "g2d5": 1547,
    "g2e1": 1548,
    "g2e2": 1549,
    "g2e3": 1550,
    "g2e4": 1551,
    "g2f1": 1552,
    "g2f1b": 1553,
    "g2f1n": 1554,
    "g2f1q": 1555,
    "g2f1r": 1556,
    "g2f2": 1557,
    "g2f3": 1558,
    "g2f4": 1559,
    "g2g1": 1560,
    "g2g1b": 1561,
    "g2g1n": 1562,
    "g2g1q": 1563,
    "g2g1r": 1564,
    "g2g3": 1565,
    "g2g4": 1566,
    "g2g5": 1567,
    "g2g6": 1568,
    "g2g7": 1569,
    "g2g8": 1570,
    "g2h1": 1571,
    "g2h1b": 1572,
    "g2h1n": 1573,
    "g2h1q": 1574,
    "g2h1r": 1575,
    "g2h2": 1576,
    "g2h3": 1577,
    "g2h4": 1578,
    "g3a3": 1579,
    "g3b3": 1580,
    "g3b8": 1581,
    "g3c3": 1582,
    "g3c7": 1583,
    "g3d3": 1584,
    "g3d6": 1585,
    "g3e1": 1586,
    "g3e2": 1587,
    "g3e3": 1588,
    "g3e4": 1589,
    "g3e5": 1590,
    "g3f1": 1591,
    "g3f2": 1592,
    "g3f3": 1593,
    "g3f4": 1594,
    "g3f5": 1595,
    "g3g1": 1596,
    "g3g2": 1597,
    "g3g4": 1598,
    "g3g5": 1599,
    "g3g6": 1600,
    "g3g7": 1601,
    "g3g8": 1602,
    "g3h1": 1603,
    "g3h2": 1604,
    "g3h3": 1605,
    "g3h4": 1606,
    "g3h5": 1607,
    "g4a4": 1608,
    "g4b4": 1609,
    "g4c4": 1610,
    "g4c8": 1611,
    "g4d1": 1612,
    "g4d4": 1613,
    "g4d7": 1614,
    "g4e2": 1615,
    "g4e3": 1616,
    "g4e4": 1617,
    "g4e5": 1618,
    "g4e6": 1619,
    "g4f2": 1620,
    "g4f3": 1621,
    "g4f4": 1622,
    "g4f5": 1623,
    "g4f6": 1624,
    "g4g1": 1625,
    "g4g2": 1626,
    "g4g3": 1627,
    "g4g5": 1628,
    "g4g6": 1629,
    "g4g7": 1630,
    "g4g8": 1631,
    "g4h2": 1632,
    "g4h3": 1633,
    "g4h4": 1634,
    "g4h5": 1635,
    "g4h6": 1636,
    "g5a5": 1637,
    "g5b5": 1638,
    "g5c1": 1639,
    "g5c5": 1640,
    "g5d2": 1641,
    "g5d5": 1642,
    "g5d8": 1643,
    "g5e3": 1644,
    "g5e4": 1645,
    "g5e5": 1646,
    "g5e6": 1647,
    "g5e7": 1648,
    "g5f3": 1649,
    "g5f4": 1650,
    "g5f5": 1651,
    "g5f6": 1652,
    "g5f7": 1653,
    "g5g1": 1654,
    "g5g2": 1655,
    "g5g3": 1656,
    "g5g4": 1657,
    "g5g6": 1658,
    "g5g7": 1659,
    "g5g8": 1660,
    "g5h3": 1661,
    "g5h4": 1662,
    "g5h5": 1663,
    "g5h6": 1664,
    "g5h7": 1665,
    "g6a6": 1666,
    "g6b1": 1667,
    "g6b6": 1668,
    "g6c2": 1669,
    "g6c6": 1670,
    "g6d3": 1671,
    "g6d6": 1672,
    "g6e4": 1673,
    "g6e5": 1674,
    "g6e6": 1675,
    "g6e7": 1676,
    "g6e8": 1677,
    "g6f4": 1678,
    "g6f5": 1679,
    "g6f6": 1680,
    "g6f7": 1681,
    "g6f8": 1682,
    "g6g1": 1683,
    "g6g2": 1684,
    "g6g3": 1685,
    "g6g4": 1686,
    "g6g5": 1687,
    "g6g7": 1688,
    "g6g8": 1689,
    "g6h4": 1690,
    "g6h5": 1691,
    "g6h6": 1692,
    "g6h7": 1693,
    "g6h8": 1694,
    "g7a1": 1695,
    "g7a7": 1696,
    "g7b2": 1697,
    "g7b7": 1698,
    "g7c3": 1699,
    "g7c7": 1700,
    "g7d4": 1701,
    "g7d7": 1702,
    "g7e5": 1703,
    "g7e6": 1704,
    "g7e7": 1705,
    "g7e8": 1706,
    "g7f5": 1707,
    "g7f6": 1708,
    "g7f7": 1709,
    "g7f8": 1710,
    "g7f8b": 1711,
    "g7f8n": 1712,
    "g7f8q": 1713,
    "g7f8r": 1714,
    "g7g1": 1715,
    "g7g2": 1716,
    "g7g3": 1717,
    "g7g4": 1718,
    "g7g5": 1719,
    "g7g6": 1720,
    "g7g8": 1721,
    "g7g8b": 1722,
    "g7g8n": 1723,
    "g7g8q": 1724,
    "g7g8r": 1725,
    "g7h5": 1726,
    "g7h6": 1727,
    "g7h7": 1728,
    "g7h8": 1729,
    "g7h8b": 1730,
    "g7h8n": 1731,
    "g7h8q": 1732,
    "g7h8r": 1733,
    "g8a2": 1734,
    "g8a8": 1735,
    "g8b3": 1736,
    "g8b8": 1737,
    "g8c4": 1738,
    "g8c8": 1739,
    "g8d5": 1740,
    "g8d8": 1741,
    "g8e6": 1742,
    "g8e7": 1743,
    "g8e8": 1744,
    "g8f6": 1745,
    "g8f7": 1746,
    "g8f8": 1747,
    "g8g1": 1748,
    "g8g2": 1749,
    "g8g3": 1750,
    "g8g4": 1751,
    "g8g5": 1752,
    "g8g6": 1753,
    "g8g7": 1754,
    "g8h6": 1755,
    "g8h7": 1756,
    "g8h8": 1757,
    "h1a1": 1758,
    "h1a8": 1759,
    "h1b1": 1760,
    "h1b7": 1761,
    "h1c1": 1762,
    "h1c6": 1763,
    "h1d1": 1764,
    "h1d5": 1765,
    "h1e1": 1766,
    "h1e4": 1767,
    "h1f1": 1768,
    "h1f2": 1769,
    "h1f3": 1770,
    "h1g1": 1771,
    "h1g2": 1772,
    "h1g3": 1773,
    "h1h2": 1774,
    "h1h3": 1775,
    "h1h4": 1776,
    "h1h5": 1777,
    "h1h6": 1778,
    "h1h7": 1779,
    "h1h8": 1780,
    "h2a2": 1781,
    "h2b2": 1782,
    "h2b8": 1783,
    "h2c2": 1784,
    "h2c7": 1785,
    "h2d2": 1786,
    "h2d6": 1787,
    "h2e2": 1788,
    "h2e5": 1789,
    "h2f1": 1790,
    "h2f2": 1791,
    "h2f3": 1792,
    "h2f4": 1793,
    "h2g1": 1794,
    "h2g1b": 1795,
    "h2g1n": 1796,
    "h2g1q": 1797,
    "h2g1r": 1798,
    "h2g2": 1799,
    "h2g3": 1800,
    "h2g4": 1801,
    "h2h1": 1802,
    "h2h1b": 1803,
    "h2h1n": 1804,
    "h2h1q": 1805,
    "h2h1r": 1806,
    "h2h3": 1807,
    "h2h4": 1808,
    "h2h5": 1809,
    "h2h6": 1810,
    "h2h7": 1811,
    "h2h8": 1812,
    "h3a3": 1813,
    "h3b3": 1814,
    "h3c3": 1815,
    "h3c8": 1816,
    "h3d3": 1817,
    "h3d7": 1818,
    "h3e3": 1819,
    "h3e6": 1820,
    "h3f1": 1821,
    "h3f2": 1822,
    "h3f3": 1823,
    "h3f4": 1824,
    "h3f5": 1825,
    "h3g1": 1826,
    "h3g2": 1827,
    "h3g3": 1828,
    "h3g4": 1829,
    "h3g5": 1830,
    "h3h1": 1831,
    "h3h2": 1832,
    "h3h4": 1833,
    "h3h5": 1834,
    "h3h6": 1835,
    "h3h7": 1836,
    "h3h8": 1837,
    "h4a4": 1838,
    "h4b4": 1839,
    "h4c4": 1840,
    "h4d4": 1841,
    "h4d8": 1842,
    "h4e1": 1843,
    "h4e4": 1844,
    "h4e7": 1845,
    "h4f2": 1846,
    "h4f3": 1847,
    "h4f4": 1848,
    "h4f5": 1849,
    "h4f6": 1850,
    "h4g2": 1851,
    "h4g3": 1852,
    "h4g4": 1853,
    "h4g5": 1854,
    "h4g6": 1855,
    "h4h1": 1856,
    "h4h2": 1857,
    "h4h3": 1858,
    "h4h5": 1859,
    "h4h6": 1860,
    "h4h7": 1861,
    "h4h8": 1862,
    "h5a5": 1863,
    "h5b5": 1864,
    "h5c5": 1865,
    "h5d1": 1866,
    "h5d5": 1867,
    "h5e2": 1868,
    "h5e5": 1869,
    "h5e8": 1870,
    "h5f3": 1871,
    "h5f4": 1872,
    "h5f5": 1873,
    "h5f6": 1874,
    "h5f7": 1875,
    "h5g3": 1876,
    "h5g4": 1877,
    "h5g5": 1878,
    "h5g6": 1879,
    "h5g7": 1880,
    "h5h1": 1881,
    "h5h2": 1882,
    "h5h3": 1883,
    "h5h4": 1884,
    "h5h6": 1885,
    "h5h7": 1886,
    "h5h8": 1887,
    "h6a6": 1888,
    "h6b6": 1889,
    "h6c1": 1890,
    "h6c6": 1891,
    "h6d2": 1892,
    "h6d6": 1893,
    "h6e3": 1894,
    "h6e6": 1895,
    "h6f4": 1896,
    "h6f5": 1897,
    "h6f6": 1898,
    "h6f7": 1899,
    "h6f8": 1900,
    "h6g4": 1901,
    "h6g5": 1902,
    "h6g6": 1903,
    "h6g7": 1904,
    "h6g8": 1905,
    "h6h1": 1906,
    "h6h2": 1907,
    "h6h3": 1908,
    "h6h4": 1909,
    "h6h5": 1910,
    "h6h7": 1911,
    "h6h8": 1912,
    "h7a7": 1913,
    "h7b1": 1914,
    "h7b7": 1915,
    "h7c2": 1916,
    "h7c7": 1917,
    "h7d3": 1918,
    "h7d7": 1919,
    "h7e4": 1920,
    "h7e7": 1921,
    "h7f5": 1922,
    "h7f6": 1923,
    "h7f7": 1924,
    "h7f8": 1925,
    "h7g5": 1926,
    "h7g6": 1927,
    "h7g7": 1928,
    "h7g8": 1929,
    "h7g8b": 1930,
    "h7g8n": 1931,
    "h7g8q": 1932,
    "h7g8r": 1933,
    "h7h1": 1934,
    "h7h2": 1935,
    "h7h3": 1936,
    "h7h4": 1937,
    "h7h5": 1938,
    "h7h6": 1939,
    "h7h8": 1940,
    "h7h8b": 1941,
    "h7h8n": 1942,
    "h7h8q": 1943,
    "h7h8r": 1944,
    "h8a1": 1945,
    "h8a8": 1946,
    "h8b2": 1947,
    "h8b8": 1948,
    "h8c3": 1949,
    "h8c8": 1950,
    "h8d4": 1951,
    "h8d8": 1952,
    "h8e5": 1953,
    "h8e8": 1954,
    "h8f6": 1955,
    "h8f7": 1956,
    "h8f8": 1957,
    "h8g6": 1958,
    "h8g7": 1959,
    "h8g8": 1960,
    "h8h1": 1961,
    "h8h2": 1962,
    "h8h3": 1963,
    "h8h4": 1964,
    "h8h5": 1965,
    "h8h6": 1966,
    "h8h7": 1967,
}
