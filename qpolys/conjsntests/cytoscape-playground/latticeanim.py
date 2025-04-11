# Save this code as a Python file (e.g., lattice_scene_fixed.py)
# Run it using: manim -pql lattice_scene_fixed.py LatticeScene

from manim import *
import json
import collections

# Provided JSON data as a Python dictionary
graph_data_json = """
{
    "nodes": [
        { "data": { "id": "0: -5*t^2 - 13*t - 9", "label": "0: -5*t^2 - 13*t - 9", "color": "#DFDF00" } },
        { "data": { "id": "1: 5*t + 6", "label": "1: 5*t + 6", "color": "#00F0F0" } },
        { "data": { "id": "2: 4", "label": "2: 4", "color": "#00F0F0" } },
        { "data": { "id": "3: -2", "label": "3: -2", "color": "#FFFF00" } },
        { "data": { "id": "4: 5*t + 6", "label": "4: 5*t + 6", "color": "#00F0F0" } },
        { "data": { "id": "5: -2*t - 3", "label": "5: -2*t - 3", "color": "#FFFF00" } },
        { "data": { "id": "6: -2", "label": "6: -2", "color": "#FFFF00" } },
        { "data": { "id": "7: 5*t + 6", "label": "7: 5*t + 6", "color": "#00F0F0" } },
        { "data": { "id": "8: -t - 4", "label": "8: -t - 4", "color": "#FFFF00" } },
        { "data": { "id": "9: -2", "label": "9: -2", "color": "#FFFF00" } },
        { "data": { "id": "10: 1", "label": "10: 1", "color": "#FFD0DF" } },
        { "data": { "id": "11: -t - 4", "label": "11: -t - 4", "color": "#FFFF00" } },
        { "data": { "id": "12: 1", "label": "12: 1", "color": "#FFD0DF" } },
        { "data": { "id": "13: 2", "label": "13: 2", "color": "#FFD0DF" } },
        { "data": { "id": "14: 5*t + 6", "label": "14: 5*t + 6", "color": "#00F0F0" } },
        { "data": { "id": "15: -t - 4", "label": "15: -t - 4", "color": "#FFFF00" } },
        { "data": { "id": "16: -2", "label": "16: -2", "color": "#FFFF00" } },
        { "data": { "id": "17: 1", "label": "17: 1", "color": "#FFD0DF" } },
        { "data": { "id": "18: -2*t - 3", "label": "18: -2*t - 3", "color": "#FFFF00" } },
        { "data": { "id": "19: 2", "label": "19: 2", "color": "#FFD0DF" } },
        { "data": { "id": "20: -t - 4", "label": "20: -t - 4", "color": "#FFFF00" } },
        { "data": { "id": "21: 2", "label": "21: 2", "color": "#FFD0DF" } },
        { "data": { "id": "22: 2", "label": "22: 2", "color": "#FFD0DF" } },
        { "data": { "id": "23: -1", "label": "23: -1", "color": "#DFDF00" } },
        { "data": { "id": "24: 1", "label": "24: 1", "color": "#FFD0DF" } },
        { "data": { "id": "25: 5*t + 6", "label": "25: 5*t + 6", "color": "#00F0F0" } },
        { "data": { "id": "26: -t - 4", "label": "26: -t - 4", "color": "#FFFF00" } },
        { "data": { "id": "27: -2", "label": "27: -2", "color": "#FFFF00" } },
        { "data": { "id": "28: 1", "label": "28: 1", "color": "#FFD0DF" } },
        { "data": { "id": "29: -2*t - 3", "label": "29: -2*t - 3", "color": "#FFFF00" } },
        { "data": { "id": "30: 2", "label": "30: 2", "color": "#FFD0DF" } },
        { "data": { "id": "31: -t - 4", "label": "31: -t - 4", "color": "#FFFF00" } },
        { "data": { "id": "32: 2", "label": "32: 2", "color": "#FFD0DF" } },
        { "data": { "id": "33: 1", "label": "33: 1", "color": "#FFD0DF" } },
        { "data": { "id": "34: 2", "label": "34: 2", "color": "#FFD0DF" } },
        { "data": { "id": "35: -1", "label": "35: -1", "color": "#DFDF00" } },
        { "data": { "id": "36: -2*t - 3", "label": "36: -2*t - 3", "color": "#FFFF00" } },
        { "data": { "id": "37: 4*t + 2", "label": "37: 4*t + 2", "color": "#FFD0DF" } },
        { "data": { "id": "38: 2", "label": "38: 2", "color": "#FFD0DF" } },
        { "data": { "id": "39: -2*t - 1", "label": "39: -2*t - 1", "color": "#DFDF00" } },
        { "data": { "id": "40: 2", "label": "40: 2", "color": "#FFD0DF" } },
        { "data": { "id": "41: -2*t - 1", "label": "41: -2*t - 1", "color": "#DFDF00" } },
        { "data": { "id": "42: -1", "label": "42: -1", "color": "#DFDF00" } },
        { "data": { "id": "43: 5*t + 6", "label": "43: 5*t + 6", "color": "#00F0F0" } },
        { "data": { "id": "44: -2*t - 3", "label": "44: -2*t - 3", "color": "#FFFF00" } },
        { "data": { "id": "45: -2", "label": "45: -2", "color": "#FFFF00" } },
        { "data": { "id": "46: -t - 4", "label": "46: -t - 4", "color": "#FFFF00" } },
        { "data": { "id": "47: 1", "label": "47: 1", "color": "#FFD0DF" } },
        { "data": { "id": "48: 2", "label": "48: 2", "color": "#FFD0DF" } },
        { "data": { "id": "49: -2*t - 3", "label": "49: -2*t - 3", "color": "#FFFF00" } },
        { "data": { "id": "50: 2", "label": "50: 2", "color": "#FFD0DF" } },
        { "data": { "id": "51: 4*t + 2", "label": "51: 4*t + 2", "color": "#FFD0DF" } },
        { "data": { "id": "52: -2*t - 1", "label": "52: -2*t - 1", "color": "#DFDF00" } },
        { "data": { "id": "53: -t - 4", "label": "53: -t - 4", "color": "#FFFF00" } },
        { "data": { "id": "54: 1", "label": "54: 1", "color": "#FFD0DF" } },
        { "data": { "id": "55: 2", "label": "55: 2", "color": "#FFD0DF" } },
        { "data": { "id": "56: 2", "label": "56: 2", "color": "#FFD0DF" } },
        { "data": { "id": "57: -1", "label": "57: -1", "color": "#DFDF00" } },
        { "data": { "id": "58: 2", "label": "58: 2", "color": "#FFD0DF" } },
        { "data": { "id": "59: -1", "label": "59: -1", "color": "#DFDF00" } },
        { "data": { "id": "60: -2*t - 1", "label": "60: -2*t - 1", "color": "#DFDF00" } },
        { "data": { "id": "61: -t - 4", "label": "61: -t - 4", "color": "#FFFF00" } },
        { "data": { "id": "62: 1", "label": "62: 1", "color": "#FFD0DF" } },
        { "data": { "id": "63: 2", "label": "63: 2", "color": "#FFD0DF" } },
        { "data": { "id": "64: 2", "label": "64: 2", "color": "#FFD0DF" } },
        { "data": { "id": "65: -1", "label": "65: -1", "color": "#DFDF00" } },
        { "data": { "id": "66: 2", "label": "66: 2", "color": "#FFD0DF" } },
        { "data": { "id": "67: -2*t - 1", "label": "67: -2*t - 1", "color": "#DFDF00" } },
        { "data": { "id": "68: -1", "label": "68: -1", "color": "#DFDF00" } },
        { "data": { "id": "69: 2", "label": "69: 2", "color": "#FFD0DF" } },
        { "data": { "id": "70: -1", "label": "70: -1", "color": "#DFDF00" } },
        { "data": { "id": "71: -2*t - 1", "label": "71: -2*t - 1", "color": "#DFDF00" } },
        { "data": { "id": "72: -1", "label": "72: -1", "color": "#DFDF00" } },
        { "data": { "id": "73: 5*t^2 + 8*t + 1", "label": "73: 5*t^2 + 8*t + 1", "color": "#00F0F0" } }
    ],
    "edges": [
        { "data": { "source": "1: 5*t + 6", "target": "0: -5*t^2 - 13*t - 9" } }, { "data": { "source": "2: 4", "target": "0: -5*t^2 - 13*t - 9" } },
        { "data": { "source": "3: -2", "target": "1: 5*t + 6" } }, { "data": { "source": "3: -2", "target": "2: 4" } },
        { "data": { "source": "4: 5*t + 6", "target": "0: -5*t^2 - 13*t - 9" } }, { "data": { "source": "5: -2*t - 3", "target": "1: 5*t + 6" } },
        { "data": { "source": "5: -2*t - 3", "target": "4: 5*t + 6" } }, { "data": { "source": "6: -2", "target": "2: 4" } },
        { "data": { "source": "6: -2", "target": "4: 5*t + 6" } }, { "data": { "source": "7: 5*t + 6", "target": "0: -5*t^2 - 13*t - 9" } },
        { "data": { "source": "8: -t - 4", "target": "1: 5*t + 6" } }, { "data": { "source": "8: -t - 4", "target": "7: 5*t + 6" } },
        { "data": { "source": "9: -2", "target": "2: 4" } }, { "data": { "source": "9: -2", "target": "7: 5*t + 6" } },
        { "data": { "source": "10: 1", "target": "3: -2" } }, { "data": { "source": "10: 1", "target": "8: -t - 4" } },
        { "data": { "source": "10: 1", "target": "9: -2" } }, { "data": { "source": "11: -t - 4", "target": "4: 5*t + 6" } },
        { "data": { "source": "11: -t - 4", "target": "7: 5*t + 6" } }, { "data": { "source": "12: 1", "target": "6: -2" } },
        { "data": { "source": "12: 1", "target": "9: -2" } }, { "data": { "source": "12: 1", "target": "11: -t - 4" } },
        { "data": { "source": "13: 2", "target": "5: -2*t - 3" } }, { "data": { "source": "13: 2", "target": "8: -t - 4" } },
        { "data": { "source": "13: 2", "target": "11: -t - 4" } }, { "data": { "source": "14: 5*t + 6", "target": "0: -5*t^2 - 13*t - 9" } },
        { "data": { "source": "15: -t - 4", "target": "1: 5*t + 6" } }, { "data": { "source": "15: -t - 4", "target": "14: 5*t + 6" } },
        { "data": { "source": "16: -2", "target": "2: 4" } }, { "data": { "source": "16: -2", "target": "14: 5*t + 6" } },
        { "data": { "source": "17: 1", "target": "3: -2" } }, { "data": { "source": "17: 1", "target": "15: -t - 4" } },
        { "data": { "source": "17: 1", "target": "16: -2" } }, { "data": { "source": "18: -2*t - 3", "target": "7: 5*t + 6" } },
        { "data": { "source": "18: -2*t - 3", "target": "14: 5*t + 6" } }, { "data": { "source": "19: 2", "target": "8: -t - 4" } },
        { "data": { "source": "19: 2", "target": "15: -t - 4" } }, { "data": { "source": "19: 2", "target": "18: -2*t - 3" } },
        { "data": { "source": "20: -t - 4", "target": "4: 5*t + 6" } }, { "data": { "source": "20: -t - 4", "target": "14: 5*t + 6" } },
        { "data": { "source": "21: 2", "target": "11: -t - 4" } }, { "data": { "source": "21: 2", "target": "18: -2*t - 3" } },
        { "data": { "source": "21: 2", "target": "20: -t - 4" } }, { "data": { "source": "22: 2", "target": "5: -2*t - 3" } },
        { "data": { "source": "22: 2", "target": "15: -t - 4" } }, { "data": { "source": "22: 2", "target": "20: -t - 4" } },
        { "data": { "source": "23: -1", "target": "13: 2" } }, { "data": { "source": "23: -1", "target": "19: 2" } },
        { "data": { "source": "23: -1", "target": "21: 2" } }, { "data": { "source": "23: -1", "target": "22: 2" } },
        { "data": { "source": "24: 1", "target": "6: -2" } }, { "data": { "source": "24: 1", "target": "16: -2" } },
        { "data": { "source": "24: 1", "target": "20: -t - 4" } }, { "data": { "source": "25: 5*t + 6", "target": "0: -5*t^2 - 13*t - 9" } },
        { "data": { "source": "26: -t - 4", "target": "1: 5*t + 6" } }, { "data": { "source": "26: -t - 4", "target": "25: 5*t + 6" } },
        { "data": { "source": "27: -2", "target": "2: 4" } }, { "data": { "source": "27: -2", "target": "25: 5*t + 6" } },
        { "data": { "source": "28: 1", "target": "3: -2" } }, { "data": { "source": "28: 1", "target": "26: -t - 4" } },
        { "data": { "source": "28: 1", "target": "27: -2" } }, { "data": { "source": "29: -2*t - 3", "target": "14: 5*t + 6" } },
        { "data": { "source": "29: -2*t - 3", "target": "25: 5*t + 6" } }, { "data": { "source": "30: 2", "target": "15: -t - 4" } },
        { "data": { "source": "30: 2", "target": "26: -t - 4" } }, { "data": { "source": "30: 2", "target": "29: -2*t - 3" } },
        { "data": { "source": "31: -t - 4", "target": "4: 5*t + 6" } }, { "data": { "source": "31: -t - 4", "target": "25: 5*t + 6" } },
        { "data": { "source": "32: 2", "target": "20: -t - 4" } }, { "data": { "source": "32: 2", "target": "29: -2*t - 3" } },
        { "data": { "source": "32: 2", "target": "31: -t - 4" } }, { "data": { "source": "33: 1", "target": "6: -2" } },
        { "data": { "source": "33: 1", "target": "27: -2" } }, { "data": { "source": "33: 1", "target": "31: -t - 4" } },
        { "data": { "source": "34: 2", "target": "5: -2*t - 3" } }, { "data": { "source": "34: 2", "target": "26: -t - 4" } },
        { "data": { "source": "34: 2", "target": "31: -t - 4" } }, { "data": { "source": "35: -1", "target": "22: 2" } },
        { "data": { "source": "35: -1", "target": "30: 2" } }, { "data": { "source": "35: -1", "target": "32: 2" } },
        { "data": { "source": "35: -1", "target": "34: 2" } }, { "data": { "source": "36: -2*t - 3", "target": "7: 5*t + 6" } },
        { "data": { "source": "36: -2*t - 3", "target": "25: 5*t + 6" } }, { "data": { "source": "37: 4*t + 2", "target": "9: -2" } },
        { "data": { "source": "37: 4*t + 2", "target": "16: -2" } }, { "data": { "source": "37: 4*t + 2", "target": "18: -2*t - 3" } },
        { "data": { "source": "37: 4*t + 2", "target": "27: -2" } }, { "data": { "source": "37: 4*t + 2", "target": "29: -2*t - 3" } },
        { "data": { "source": "37: 4*t + 2", "target": "36: -2*t - 3" } }, { "data": { "source": "38: 2", "target": "11: -t - 4" } },
        { "data": { "source": "38: 2", "target": "31: -t - 4" } }, { "data": { "source": "38: 2", "target": "36: -2*t - 3" } },
        { "data": { "source": "39: -2*t - 1", "target": "12: 1" } }, { "data": { "source": "39: -2*t - 1", "target": "21: 2" } },
        { "data": { "source": "39: -2*t - 1", "target": "24: 1" } }, { "data": { "source": "39: -2*t - 1", "target": "32: 2" } },
        { "data": { "source": "39: -2*t - 1", "target": "33: 1" } }, { "data": { "source": "39: -2*t - 1", "target": "37: 4*t + 2" } },
        { "data": { "source": "39: -2*t - 1", "target": "38: 2" } }, { "data": { "source": "40: 2", "target": "8: -t - 4" } },
        { "data": { "source": "40: 2", "target": "26: -t - 4" } }, { "data": { "source": "40: 2", "target": "36: -2*t - 3" } },
        { "data": { "source": "41: -2*t - 1", "target": "10: 1" } }, { "data": { "source": "41: -2*t - 1", "target": "17: 1" } },
        { "data": { "source": "41: -2*t - 1", "target": "19: 2" } }, { "data": { "source": "41: -2*t - 1", "target": "28: 1" } },
        { "data": { "source": "41: -2*t - 1", "target": "30: 2" } }, { "data": { "source": "41: -2*t - 1", "target": "37: 4*t + 2" } },
        { "data": { "source": "41: -2*t - 1", "target": "40: 2" } }, { "data": { "source": "42: -1", "target": "13: 2" } },
        { "data": { "source": "42: -1", "target": "34: 2" } }, { "data": { "source": "42: -1", "target": "38: 2" } },
        { "data": { "source": "42: -1", "target": "40: 2" } }, { "data": { "source": "43: 5*t + 6", "target": "0: -5*t^2 - 13*t - 9" } },
        { "data": { "source": "44: -2*t - 3", "target": "1: 5*t + 6" } }, { "data": { "source": "44: -2*t - 3", "target": "43: 5*t + 6" } },
        { "data": { "source": "45: -2", "target": "2: 4" } }, { "data": { "source": "45: -2", "target": "43: 5*t + 6" } },
        { "data": { "source": "46: -t - 4", "target": "14: 5*t + 6" } }, { "data": { "source": "46: -t - 4", "target": "43: 5*t + 6" } },
        { "data": { "source": "47: 1", "target": "16: -2" } }, { "data": { "source": "47: 1", "target": "45: -2" } },
        { "data": { "source": "47: 1", "target": "46: -t - 4" } }, { "data": { "source": "48: 2", "target": "15: -t - 4" } },
        { "data": { "source": "48: 2", "target": "44: -2*t - 3" } }, { "data": { "source": "48: 2", "target": "46: -t - 4" } },
        { "data": { "source": "49: -2*t - 3", "target": "4: 5*t + 6" } }, { "data": { "source": "49: -2*t - 3", "target": "43: 5*t + 6" } },
        { "data": { "source": "50: 2", "target": "20: -t - 4" } }, { "data": { "source": "50: 2", "target": "46: -t - 4" } },
        { "data": { "source": "50: 2", "target": "49: -2*t - 3" } }, { "data": { "source": "51: 4*t + 2", "target": "3: -2" } },
        { "data": { "source": "51: 4*t + 2", "target": "5: -2*t - 3" } }, { "data": { "source": "51: 4*t + 2", "target": "6: -2" } },
        { "data": { "source": "51: 4*t + 2", "target": "44: -2*t - 3" } }, { "data": { "source": "51: 4*t + 2", "target": "45: -2" } },
        { "data": { "source": "51: 4*t + 2", "target": "49: -2*t - 3" } }, { "data": { "source": "52: -2*t - 1", "target": "17: 1" } },
        { "data": { "source": "52: -2*t - 1", "target": "22: 2" } }, { "data": { "source": "52: -2*t - 1", "target": "24: 1" } },
        { "data": { "source": "52: -2*t - 1", "target": "47: 1" } }, { "data": { "source": "52: -2*t - 1", "target": "48: 2" } },
        { "data": { "source": "52: -2*t - 1", "target": "50: 2" } }, { "data": { "source": "52: -2*t - 1", "target": "51: 4*t + 2" } },
        { "data": { "source": "53: -t - 4", "target": "7: 5*t + 6" } }, { "data": { "source": "53: -t - 4", "target": "43: 5*t + 6" } },
        { "data": { "source": "54: 1", "target": "9: -2" } }, { "data": { "source": "54: 1", "target": "45: -2" } },
        { "data": { "source": "54: 1", "target": "53: -t - 4" } }, { "data": { "source": "55: 2", "target": "18: -2*t - 3" } },
        { "data": { "source": "55: 2", "target": "46: -t - 4" } }, { "data": { "source": "55: 2", "target": "53: -t - 4" } },
        { "data": { "source": "56: 2", "target": "11: -t - 4" } }, { "data": { "source": "56: 2", "target": "49: -2*t - 3" } },
        { "data": { "source": "56: 2", "target": "53: -t - 4" } }, { "data": { "source": "57: -1", "target": "21: 2" } },
        { "data": { "source": "57: -1", "target": "50: 2" } }, { "data": { "source": "57: -1", "target": "55: 2" } },
        { "data": { "source": "57: -1", "target": "56: 2" } }, { "data": { "source": "58: 2", "target": "8: -t - 4" } },
        { "data": { "source": "58: 2", "target": "44: -2*t - 3" } }, { "data": { "source": "58: 2", "target": "53: -t - 4" } },
        { "data": { "source": "59: -1", "target": "19: 2" } }, { "data": { "source": "59: -1", "target": "48: 2" } },
        { "data": { "source": "59: -1", "target": "55: 2" } }, { "data": { "source": "59: -1", "target": "58: 2" } },
        { "data": { "source": "60: -2*t - 1", "target": "10: 1" } }, { "data": { "source": "60: -2*t - 1", "target": "12: 1" } },
        { "data": { "source": "60: -2*t - 1", "target": "13: 2" } }, { "data": { "source": "60: -2*t - 1", "target": "51: 4*t + 2" } },
        { "data": { "source": "60: -2*t - 1", "target": "54: 1" } }, { "data": { "source": "60: -2*t - 1", "target": "56: 2" } },
        { "data": { "source": "60: -2*t - 1", "target": "58: 2" } }, { "data": { "source": "61: -t - 4", "target": "25: 5*t + 6" } },
        { "data": { "source": "61: -t - 4", "target": "43: 5*t + 6" } }, { "data": { "source": "62: 1", "target": "27: -2" } },
        { "data": { "source": "62: 1", "target": "45: -2" } }, { "data": { "source": "62: 1", "target": "61: -t - 4" } },
        { "data": { "source": "63: 2", "target": "29: -2*t - 3" } }, { "data": { "source": "63: 2", "target": "46: -t - 4" } },
        { "data": { "source": "63: 2", "target": "61: -t - 4" } }, { "data": { "source": "64: 2", "target": "31: -t - 4" } },
        { "data": { "source": "64: 2", "target": "49: -2*t - 3" } }, { "data": { "source": "64: 2", "target": "61: -t - 4" } },
        { "data": { "source": "65: -1", "target": "32: 2" } }, { "data": { "source": "65: -1", "target": "50: 2" } },
        { "data": { "source": "65: -1", "target": "63: 2" } }, { "data": { "source": "65: -1", "target": "64: 2" } },
        { "data": { "source": "66: 2", "target": "36: -2*t - 3" } }, { "data": { "source": "66: 2", "target": "53: -t - 4" } },
        { "data": { "source": "66: 2", "target": "61: -t - 4" } }, { "data": { "source": "67: -2*t - 1", "target": "37: 4*t + 2" } },
        { "data": { "source": "67: -2*t - 1", "target": "47: 1" } }, { "data": { "source": "67: -2*t - 1", "target": "54: 1" } },
        { "data": { "source": "67: -2*t - 1", "target": "55: 2" } }, { "data": { "source": "67: -2*t - 1", "target": "62: 1" } },
        { "data": { "source": "67: -2*t - 1", "target": "63: 2" } }, { "data": { "source": "67: -2*t - 1", "target": "66: 2" } },
        { "data": { "source": "68: -1", "target": "38: 2" } }, { "data": { "source": "68: -1", "target": "56: 2" } },
        { "data": { "source": "68: -1", "target": "64: 2" } }, { "data": { "source": "68: -1", "target": "66: 2" } },
        { "data": { "source": "69: 2", "target": "26: -t - 4" } }, { "data": { "source": "69: 2", "target": "44: -2*t - 3" } },
        { "data": { "source": "69: 2", "target": "61: -t - 4" } }, { "data": { "source": "70: -1", "target": "30: 2" } },
        { "data": { "source": "70: -1", "target": "48: 2" } }, { "data": { "source": "70: -1", "target": "63: 2" } },
        { "data": { "source": "70: -1", "target": "69: 2" } }, { "data": { "source": "71: -2*t - 1", "target": "28: 1" } },
        { "data": { "source": "71: -2*t - 1", "target": "33: 1" } }, { "data": { "source": "71: -2*t - 1", "target": "34: 2" } },
        { "data": { "source": "71: -2*t - 1", "target": "51: 4*t + 2" } }, { "data": { "source": "71: -2*t - 1", "target": "62: 1" } },
        { "data": { "source": "71: -2*t - 1", "target": "64: 2" } }, { "data": { "source": "71: -2*t - 1", "target": "69: 2" } },
        { "data": { "source": "72: -1", "target": "40: 2" } }, { "data": { "source": "72: -1", "target": "58: 2" } },
        { "data": { "source": "72: -1", "target": "66: 2" } }, { "data": { "source": "72: -1", "target": "69: 2" } },
        { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "23: -1" } }, { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "35: -1" } },
        { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "39: -2*t - 1" } }, { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "41: -2*t - 1" } },
        { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "42: -1" } }, { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "52: -2*t - 1" } },
        { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "57: -1" } }, { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "59: -1" } },
        { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "60: -2*t - 1" } }, { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "65: -1" } },
        { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "67: -2*t - 1" } }, { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "68: -1" } },
        { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "70: -1" } }, { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "71: -2*t - 1" } },
        { "data": { "source": "73: 5*t^2 + 8*t + 1", "target": "72: -1" } }
    ]
}
"""

# Parse the JSON string
graph_data = json.loads(graph_data_json)

class LatticeScene(Scene):
    def construct(self):
        # Configurable parameters
        scale_factor = 0.8 # Scale the overall layout
        rank_sep = 1.5 * scale_factor    # Vertical distance between ranks
        intra_rank_sep = 1.0 * scale_factor # Horizontal distance within a rank
        node_radius = 0.25 * scale_factor
        label_font_size = 14 * scale_factor
        edge_config = {"stroke_width": 2 * scale_factor, "color": GRAY}
        # Removed arrow_config as it might not be used directly here

        # --- 1. Parse Data ---
        node_info = {}
        vertices = []
        adj = collections.defaultdict(list)
        edge_list = []

        for node in graph_data["nodes"]:
            node_id = node["data"]["id"]
            vertices.append(node_id)
            label_full = node["data"]["label"]
            # Extract math part of label, handling potential errors
            label_parts = label_full.split(":", 1)
            math_label = label_parts[1].strip() if len(label_parts) > 1 else label_full
            # Replace '*' with '\cdot' for better LaTeX rendering if needed
            math_label = math_label.replace('*', r'\cdot ')

            node_info[node_id] = {
                "label": math_label,
                "color": node["data"]["color"]
            }

        for edge in graph_data["edges"]:
            source = edge["data"]["source"]
            target = edge["data"]["target"]
            # Check if source and target exist before adding edge
            if source in node_info and target in node_info:
                 edge_list.append((source, target))
                 adj[source].append(target)
            else:
                 print(f"Warning: Skipping edge with missing node: {source} -> {target}")


        # --- 2. Determine Ranks using BFS ---
        root_node = "73: 5*t^2 + 8*t + 1"
        ranks = {node_id: -1 for node_id in vertices} # Initialize ranks as -1 (unvisited)
        nodes_by_rank = collections.defaultdict(list)
        max_rank = 0

        if root_node not in vertices:
             all_targets = {edge[1] for edge in edge_list}
             potential_roots = [v for v in vertices if v not in all_targets]
             if not potential_roots:
                  print("Error: Could not determine root node(s). Aborting rank calculation.")
                  return
             root_node = potential_roots[0]
             print(f"Warning: Assumed root not found. Using fallback root: '{root_node}'")

        queue = collections.deque([(root_node, 0)]) # (node, rank)
        if root_node in ranks: # Ensure root exists before assigning rank
            ranks[root_node] = 0
            nodes_by_rank[0].append(root_node)
        else:
            print(f"Error: Root node '{root_node}' not found in parsed vertices.")
            return # Cannot proceed

        processed_nodes_in_bfs = {root_node} # Keep track of nodes added to queue

        while queue:
            current_node, current_rank = queue.popleft()
            max_rank = max(max_rank, current_rank)

            for neighbor in adj[current_node]:
                # Check if neighbor exists and hasn't been processed in BFS yet
                if neighbor in ranks and neighbor not in processed_nodes_in_bfs:
                    ranks[neighbor] = current_rank + 1
                    nodes_by_rank[current_rank + 1].append(neighbor)
                    queue.append((neighbor, current_rank + 1))
                    processed_nodes_in_bfs.add(neighbor)
                # Handle cases where a node might be reached via multiple paths (potentially different ranks)
                elif neighbor in ranks and ranks[neighbor] == -1: # Visited but maybe not ranked from shortest path
                     ranks[neighbor] = current_rank + 1
                     nodes_by_rank[current_rank + 1].append(neighbor)
                     # Don't add back to queue if already processed via another path

        # Check for unranked nodes
        unranked = [node_id for node_id, rank in ranks.items() if rank == -1]
        if unranked:
            print(f"Warning: Some nodes were not reached by BFS: {unranked}")


        # --- 3. Calculate Layout Positions ---
        layout = {}
        y_scale = rank_sep
        total_height = max_rank * y_scale

        for rank, nodes_in_rank in sorted(nodes_by_rank.items()):
            num_nodes = len(nodes_in_rank)
            rank_width = (num_nodes - 1) * intra_rank_sep if num_nodes > 1 else 0
            start_x = -rank_width / 2
            # Adjust y_pos calculation to place rank 0 at the bottom
            y_pos = (-max_rank + rank) * y_scale + total_height / 2

            # Sort nodes within rank for consistent ordering
            nodes_in_rank.sort(key=lambda node_id: int(node_id.split(":", 1)[0]))

            for i, node_id in enumerate(nodes_in_rank):
                x_pos = start_x + i * intra_rank_sep if num_nodes > 1 else 0
                layout[node_id] = [x_pos, y_pos, 0]

        # Handle unranked nodes
        for i, node_id in enumerate(unranked):
             layout[node_id] = [-10 -i*0.5 , -total_height/2 - 2, 0]


        # --- 4. Create Manim Vertex Config ---
        vert_config = {}
        label_dict = {}
        for node_id, info in node_info.items():
            label_obj = MathTex(info["label"], font_size=label_font_size).scale(0.8) # Scale label here
            label_dict[node_id] = label_obj # Store generated label mobject

            vert_config[node_id] = {
                "radius": node_radius,
                "fill_color": info["color"],
                "fill_opacity": 0.9,
                "color": DARK_GRAY,
                "stroke_width": 1 * scale_factor,
            }

        # --- 5. Create Manim Graph ---
        valid_vertices = [v for v in vertices if ranks[v] != -1]
        # Filter edge_list to only include edges between valid vertices
        valid_edge_list = [(u, v) for u, v in edge_list if u in valid_vertices and v in valid_vertices]

        # Filter layout to only include valid vertices
        valid_layout = {v: pos for v, pos in layout.items() if v in valid_vertices}

        graph = Graph(
            valid_vertices,
            valid_edge_list, # Use filtered edges
            layout=valid_layout, # Use filtered layout
            layout_scale=3,
            vertex_config=vert_config,
            edge_config=edge_config,
            # Pass the pre-generated labels dictionary
            labels=label_dict,
            # labels = True # Alternative: use default label positioning, may overlap
        )

        # Position the graph
        graph.move_to(ORIGIN)

        # --- 6. Add to Scene ---
        self.play(Create(graph), run_time=5) # Increased run_time for complex graph

        # Optional: Add rank labels
        rank_texts = VGroup()
        if max_rank >= 0: # Only add rank labels if ranks were calculated
            for r in range(max_rank + 1):
                 y_pos = (-max_rank + r) * y_scale + total_height / 2
                 rank_nodes = nodes_by_rank[r]
                 if rank_nodes:
                      num_nodes = len(rank_nodes)
                      rank_width = (num_nodes - 1) * intra_rank_sep if num_nodes > 1 else 0
                      label_x_pos = -rank_width / 2 - intra_rank_sep * 1.5
                      rank_label = Text(f"Rank {r}", font_size=18 * scale_factor, color=GRAY)
                      rank_label.move_to([label_x_pos, y_pos, 0])
                      rank_texts.add(rank_label)

            self.play(Write(rank_texts), run_time=1)

        self.wait(5) # Increased wait time