from lxml import etree
import argparse
import os

rejected_names = ["\"hot\"", "player's edge", "players edge", "mahjong", "casino", "virtual poker", "virtual blackjack",
                  "erotic", "roullette", "video poker", "poker", "video blackjack", "blackjack", "slots", "slot machine",
                  "gambling", "sex", "(notgame)"]
existing_count = {}


def name_desc_from_game(game_elem):
    gname = None
    gdesc = None
    for e in game_elem.getchildren():
        if e.tag == "name":
            gname = e.text
        elif e.tag == "desc":
            gdesc = e.text
        if gname and gdesc:
            return gname, gdesc
    return gname, gdesc


def is_name_rejected(gname, gdesc):
    for rn in rejected_names:
        if (gname is not None and rn in gname.lower()) or (gdesc is not None and rn in gdesc.lower()):
            print(f"tbr: {gname}: {gdesc}")
            return True
    return False


def has_no_description(gname, gdesc):
    if gdesc:
        gdesc = gdesc.strip()
    if not gdesc:
        print(f"rejecting {gname} due to no description")
        return True


def is_name_duplicate(gname):
    n = gname.strip().lower()
    count = existing_count.get(n)
    if not count:
        existing_count[gname] = True
        return False
    else:
        print(f'found duplicate game entry: {n}')
        return True


def remove_game(c_pointer):
    game_parent = c_pointer.getparent()
    game_parent.remove(c_pointer)


def check_games(gameslist_path, output_path):
    doc = etree.parse(gameslist_path)
    all_children = doc.findall(".//game")
    duplicate_count = 0
    rejected_name_count = 0
    missing_description_count = 0
    game_count = 0
    for c in all_children:
        game_count += 1
        name, desc = name_desc_from_game(c)
        if is_name_duplicate(name):
            duplicate_count += 1
            remove_game(c)
        elif is_name_rejected(name, desc):
            rejected_name_count += 1
            remove_game(c)
        elif has_no_description(name, desc):
            missing_description_count += 1
            remove_game(c)
    removal_count = duplicate_count + rejected_name_count + missing_description_count
    print("-----")
    print(f"total games: {game_count}")
    print(f"games removed due to duplicates: {duplicate_count}")
    print(f"games removed due to rejected name: {rejected_name_count}")
    print(f"games removed due to missing description: {missing_description_count}")
    print(f'total removals: {removal_count}')
    et = etree.ElementTree(doc.getroot())
    et.write(output_path, pretty_print=True)


def parse_args():
    parser = argparse.ArgumentParser(prog="sgsanitizer",
                                     description="Provide a gamelist.xml file and it will do its best to "
                                                 "sanitize and remove any vulgar, casino, mahjong, or other "
                                                 "known unusable games from the gamelist. Primarily for arcade games")
    parser.add_argument('gamelist_path', help="full path to gamelist.xml", type=argparse.FileType('r',
                                                                                                  encoding='latin1'))
    parser.add_argument('output_file', help="full path to output location")
    args = parser.parse_args()
    return args


def main():
    args = parse_args()
    check_games(args.gamelist_path, args.output_file)


if __name__ == "__main__":
    main()


