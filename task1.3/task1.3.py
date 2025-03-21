import os
import networkx as nx
import pandas as pd
import colorama
from colorama import Fore, Style
from difflib import get_close_matches

colorama.init(autoreset=True)

# 📂 Load Data File Dynamically
current_directory = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(current_directory, "task1_3_data.csv")

# 🛠 Load CSV File
df = pd.read_csv(file_path)

# ✅ Define Graph (Railway Network)
G_new = nx.Graph()

# 🚆 Add Train Stations & Routes from CSV (Normalize Names)
for _, row in df.iterrows():
    station1 = row.iloc[0].strip().lower()
    station2 = row.iloc[1].strip().lower()
    cost, time = int(row.iloc[2]), int(row.iloc[3])

    G_new.add_edge(station1, station2, cost=cost, time=time)

# ✅ Modified Output Line
print(Fore.CYAN + f"\n✅ Railway network loaded with {len(G_new.nodes)} stations and {len(G_new.edges)} routes.\n")

# 🛠 Convert Minutes to HH:MM Format
def format_time(minutes):
    if minutes >= 60:
        hours = minutes // 60
        mins = minutes % 60
        return f"{hours}h {mins}m" if mins else f"{hours}h"
    return f"{minutes} min"

# 🔍 Find Closest Matching Stations
def find_closest_stations(user_input, station_list):
    """Finds the closest matching station names using fuzzy matching."""
    return get_close_matches(user_input, station_list, n=4, cutoff=0.6)

# 🚆 Find Route with Error Handling
def find_route(graph, start, end, criterion="cost"):
    """Finds the optimal route and retrieves both cost & time for comparison."""
    start, end = start.strip().lower(), end.strip().lower()
    station_map = {station.lower(): station for station in graph.nodes}

    if start not in station_map or end not in station_map:
        return None, None, None  # If station not found, return None

    start, end = station_map[start], station_map[end]

    try:
        path = nx.shortest_path(graph, source=start, target=end, weight=criterion)
        total_time = sum(graph[path[i]][path[i+1]]['time'] for i in range(len(path) - 1))
        total_cost = sum(graph[path[i]][path[i+1]]['cost'] for i in range(len(path) - 1))

        return path, total_cost, total_time
    except nx.NetworkXNoPath:
        print(Fore.RED + f"❌ No route found between {start.capitalize()} and {end.capitalize()}.")
        return None, None, None

# 🚆 Main Ticket Search Function
def search_train_tickets():
    while True:
        print(Fore.CYAN + "\n🚆 Train Ticket Search System 🚆")
        print(Fore.YELLOW + "=" * 50)

        station_map = {station.lower(): station for station in G_new.nodes}

        # ✅ Get Departure Station with Correction
        while True:
            departure = input(Fore.GREEN + "📍 Enter departure station: ").strip().lower()
            if departure in station_map:
                departure = station_map[departure]  # Use correct station name
                break
            corrected = find_closest_stations(departure, station_map.keys())
            if corrected:
                print(Fore.YELLOW + f"\n🚨 '{departure}' not found. Did you mean:")
                for i, suggestion in enumerate(corrected, start=1):
                    print(f"{i}. {suggestion.capitalize()}")
                choice = input(Fore.GREEN + "🔍 Enter the number of your choice (or press Enter to retry): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(corrected):
                    departure = station_map[corrected[int(choice) - 1]]
                    break

        # ✅ Get Destination Station with Correction
        while True:
            destination = input(Fore.GREEN + "🎯 Enter destination station: ").strip().lower()
            if destination in station_map:
                destination = station_map[destination]  # Use correct station name
                break
            corrected = find_closest_stations(destination, station_map.keys())
            if corrected:
                print(Fore.YELLOW + f"\n🚨 '{destination}' not found. Did you mean:")
                for i, suggestion in enumerate(corrected, start=1):
                    print(f"{i}. {suggestion.capitalize()}")
                choice = input(Fore.GREEN + "🔍 Enter the number of your choice (or press Enter to retry): ").strip()
                if choice.isdigit() and 1 <= int(choice) <= len(corrected):
                    destination = station_map[corrected[int(choice) - 1]]
                    break

        print(Fore.YELLOW + "=" * 50)

        # Find cheapest and fastest routes
        cheapest_route = find_route(G_new, departure, destination, "cost")
        fastest_route = find_route(G_new, departure, destination, "time")

        # Display Cheapest Route (Total Cost + Travel Time)
        if cheapest_route[1] is not None:
            print(Fore.BLUE + "\n📌 Cheapest Route:")
            print(Fore.LIGHTMAGENTA_EX + " → ".join(cheapest_route[0]))
            print(Fore.GREEN + f"💰 Total Cost: £{cheapest_route[1]}")
            print(Fore.GREEN + f"⏳ Travel Time: {format_time(cheapest_route[2])}")
        else:
            print(Fore.RED + "❌ No cheapest route found.")

        print(Fore.YELLOW + "-" * 50)

        # Display Fastest Route (Total Time + Travel Cost)
        if fastest_route[1] is not None:
            print(Fore.BLUE + "\n⚡ Fastest Route:")
            print(Fore.LIGHTCYAN_EX + " → ".join(fastest_route[0]))
            print(Fore.GREEN + f"⏳ Total Time: {format_time(fastest_route[2])}")
            print(Fore.GREEN + f"💰 Travel Cost: £{fastest_route[1]}")
        else:
            print(Fore.RED + "❌ No fastest route found.")

        print(Fore.YELLOW + "=" * 50)

        # ✅ Fix: Proper Input Validation for Exit Prompt with Closest Station Suggestions
        while True:
            again = input(Fore.CYAN + "🔄 Do you want to search another route? (yes/no): ").strip().lower()
            
            if again in ["yes", "no"]:
                break  # ✅ Accept only "yes" or "no"
            
            # 🚨 If the user enters a station name instead, suggest closest stations
            closest_matches = find_closest_stations(again, station_map.keys())
            if closest_matches:
                print(Fore.YELLOW + f"\n🚨 '{again}' looks like a station name! Did you mean:")
                for i, suggestion in enumerate(closest_matches, start=1):
                    print(f"{i}. {suggestion.capitalize()}")
                print(Fore.RED + "⚠️ Please enter 'yes' or 'no' to continue.")

        if again == "no":
            print(Fore.YELLOW + "👋 Exiting Train Ticket Search System. Have a nice day!\n")
            break

# 🚆 Run System
if __name__ == "__main__":
    search_train_tickets()