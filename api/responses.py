from api.db import get_sector_data
from api.db import get_dip_array
from enum import Enum
import json

class Surveillance(Enum):
    SURV3_LOOT3 = 4
    SURV3_LOOT2 = 5
    SURV3_LOOT1 = 6
    SURV2_LOOT2 = 7
    SURV2_LOOT1 = 8
    SURV1_LOOT1 = 9

class Favor(Enum):
    DOUBLE_DIP = 18
    FAILED_DIP = 19
    CANT_DIP = 20

class Tier(Enum):
    TIER3 = 3
    TIER2 = 2
    TIER1 = 1

class Retrieval(Enum):
    TIER3 = 14
    TIER2 = 15
    TIER1 = 16

def get_loot_tier(s: int):
    if s == 4:
        return Tier.TIER3
    elif s == 5 or s == 7:
        return Tier.TIER2
    else:
        return Tier.TIER1

def load_itemlist():
    with open('./api/data/items.json', 'r', errors='ignore') as file:
        json_data = file.read()
    return json.loads(json_data)

def get_sector_data_response(sector_id: int):

    sector_rows = get_sector_data(sector_id)

    dip_rows = get_dip_array([
        sector.dip_1 for sector in sector_rows] + [
        sector.dip_2 for sector in sector_rows if sector.dip_2 is not None
        ])
    
    double_dips = [
        sum(1 for sector in sector_rows if sector.favor_result == 19),
        sum(1 for sector in sector_rows if sector.dip_2 is not None)
    ]

    ddr = 0 if sum(double_dips) == 0 else (double_dips[0] / sum(double_dips)) * 100

    tiers = {
        Tier.TIER1.name: {"data": {}, "hits": [0,0,0]},
        Tier.TIER2.name: {"data": {}, "hits": [0,0]},
        Tier.TIER3.name: {"data": {}, "hits": [0]}
    }

    itemlist = load_itemlist()

    for dip in dip_rows:
        loot_tier = get_loot_tier(dip.surveillance_result)
        if loot_tier.name in tiers:
            tier = tiers[loot_tier.name]
            if (dip.surveillance_result == 4) or (dip.surveillance_result == 5) or (dip.surveillance_result == 6):
                tier["hits"][0] += 1
            elif (dip.surveillance_result == 7) or (dip.surveillance_result == 8):
                tier["hits"][1] += 1
            else:
                tier["hits"][2] += 1
            item_id = str(dip.item_id)
            if item_id not in tier["data"]:
                tier["data"][item_id] = {
                    "Hits": 0,
                    "R1": {"Min": 0, "Max": 0},
                    "R2": {"Min": 0, "Max": 0},
                    "R3": {"Min": 0, "Max": 0},
                }
            tier["data"][item_id]["Hits"] += 1
            key = "R1"
            if dip.retrieval_result == 14:
                key = "R3"
            elif dip.retrieval_result == 15:
                key = "R2"
            if dip.quantity < tier["data"][item_id][key]["Min"] or tier["data"][item_id][key]["Min"] == 0:
                tier["data"][item_id][key]["Min"] = dip.quantity
            if dip.quantity > tier["data"][item_id][key]["Max"]:
                tier["data"][item_id][key]["Max"] = dip.quantity
    response = {
        Tier.TIER1.name: {"Items":[], "DDRate":ddr, "Procs":tiers[Tier.TIER1.name]["hits"]},
        Tier.TIER2.name: {"Items":[], "DDRate":ddr, "Procs":tiers[Tier.TIER2.name]["hits"]},
        Tier.TIER3.name: {"Items":[], "DDRate":ddr, "Procs":tiers[Tier.TIER3.name]["hits"]}
    }
    for t, tier in tiers.items():
        for id, data in tier["data"].items():
            response[t]["Items"].append({
                "ItemId":id,
                "Name":itemlist[f"{id}"],
                "Rate": (data["Hits"]/sum(tier["hits"]))*100,
                "R1": data["R1"],
                "R2": data["R2"],
                "R3": data["R3"]
            })
    return response