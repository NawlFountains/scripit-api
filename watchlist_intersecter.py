import os
import argparse
import letterboxd_scraper as scraper

def intersect_watchlists(watchlists):
    print("Intersecting watchlists...")
    intersected_watchlist = watchlists[0]
    for i in range(1, len(watchlists)):
        intersected_watchlist = intersected_watchlist.merge(watchlists[i], how='inner', on=['Name','Year'])
    print("Intersected watchlists:")
    return intersected_watchlist

def print_watchlist(watchlist):
    print('\nWatchlist:\n')
    if watchlist.empty:
        print('Watchlist is empty')
        return
    for index, row in watchlist.iterrows():
        print(row['Name'], row['Year'])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Intersect the watchlist from letterboxd users")
    parser.add_argument('users', help='Username of one or more users', nargs='+')
    args = parser.parse_args()
    watchlists = []

    output_dir = f"intersected_watchlist"
    os.makedirs(output_dir, exist_ok=True)

    for user in args.users:
        watchlists.append(scraper.retrive_watchlist_from_user(user))
    
    nameToStore = f"{output_dir}/intersected_watchlist{args.users}.csv"
    df = intersect_watchlists(watchlists)
    df.to_csv(nameToStore, index=False)
    print_watchlist(df)
    print(f'Saved to {nameToStore}')

