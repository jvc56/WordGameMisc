import re
import os
import argparse

def main(srcdir, destdir, tourney_name):
    onlyfiles = [f for f in os.listdir(srcdir) if os.path.isfile(os.path.join(srcdir, f))]

    for filename in onlyfiles:
        mround = re.search(r"(\d)+", filename)
        if mround.group() is None:
            print("malformed filename: ", filename)
            exit(0)
        round_num = mround.group()
        title_comment = "{}, Round {}.".format(tourney_name, round_num)
        newfilestring = ""
        with open(os.path.join(srcdir, filename)) as gcg:
            notenext = False
            player1 = ""
            done = False
            for line in gcg:
                newfileline = line
                if done:
                    newfilestring += newfileline
                    continue

                mplayer1 = re.search("^.player1 (\w+)", line)
                if mplayer1 is not None and mplayer1.group(1) is not None:
                    player1 = mplayer1.group(1)
                    newfilestring += newfileline
                    continue

                if player1 != "":
                    mfirstplay = re.search(">{}:".format(player1), line)
                    if mfirstplay is not None:
                        notenext = True
                        newfilestring += newfileline
                        continue

                if notenext:
                    if line.startswith("#note"):
                        newfileline = "#note {} {}".format(title_comment, line[5:])
                    else:
                        newfileline = "#note {}".format(title_comment) + "\n" + line
                    done = True

                newfilestring += newfileline

        with open(os.path.join(destdir, filename), "w") as text_file:
            text_file.write(newfilestring)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Annotate game files")
    parser.add_argument("--srcdir", required=True, help="Source directory for game files")
    parser.add_argument("--destdir", required=True, help="Destination directory for annotated game files")
    parser.add_argument("--tourney_name", required=True, help="Name of the tournament")

    args = parser.parse_args()
    main(args.srcdir, args.destdir, args.tourney_name)

