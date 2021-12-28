from csv import reader
from argparse import ArgumentParser
from collections import defaultdict


def determine_payouts(name_and_profits):
    l = 0
    r = len(name_and_profits) - 1

    owed = defaultdict(lambda: defaultdict(int))
    while l < r:
        up = name_and_profits[l][1]
        down = name_and_profits[r][1]

        if up > abs(down):
            name_and_profits[l][1] += down
            owed[name_and_profits[l][0]][name_and_profits[r][0]] += abs(down)
            r -= 1
        elif up < abs(down):
            name_and_profits[r][1] += up
            owed[name_and_profits[l][0]][name_and_profits[r][0]] += up
            l += 1
        else:
            owed[name_and_profits[l][0]][name_and_profits[r][0]] += abs(down)
            l += 1
            r -= 1

    return owed


def main():
    parser = ArgumentParser()
    parser.add_argument("--csv_file", required=True, help="CSV file containing ledger information.")

    args = parser.parse_args()

    csv_file = args.csv_file

    with open(csv_file, newline="") as f:
        ledger_reader = reader(f)
        next(ledger_reader)

        name_and_net_profit = []
        for row in ledger_reader:
            name_and_net_profit.append([row[0], int(row[7]) / 100])

        name_and_net_profit.sort(key=lambda x: x[1], reverse=True)

    payout = determine_payouts(name_and_net_profit)

    results_file = "results.txt"
    with open(results_file, "a") as f:
        for key, val in payout.items():
            losers = [[loser_key, round(loser_val, 2)] for loser_key, loser_val in val.items()]
            f.write(f"Pay to: {key}\n")
            f.write(f"From:  {losers[0][0]}: {losers[0][1]}\n")
            for loser in losers[1:]:
                f.write(f"       {loser[0]}: {loser[1]}\n")
            f.write("\n")

if __name__ == "__main__":
    main()



