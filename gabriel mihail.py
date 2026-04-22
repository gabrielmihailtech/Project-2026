# gabriel mihail

def read_file(filename):
    ids = []
    gdpr = []
    days = []
    status = []

    with open(filename, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            ids.append(parts[0])
            gdpr.append(parts[1])
            days.append(int(parts[2]))
            status.append(parts[3])

    return ids, gdpr, days, status

def view_all(ids, gdpr, days, status):
    print("\n=== All Gamer Accounts ===\n")

    for i in range(len(ids)):
        player_id = ids[i]
        paid = gdpr[i]
        day_count = days[i]
        acc_status = status[i]

        # Determine type
        if player_id.startswith("CAS"):
            acc_type = "Casual"
        else:
            acc_type = "Pro"

        # Paid icon
        paid_icon = "✅" if paid == "Yes" else "❎"

        # Alert for > 90 days
        alert = " 🚨" if day_count > 90 else ""

        # Print formatted row
        print(f"{player_id:<10} {acc_type:<7} {paid_icon:<3} {acc_status:<8}{alert}")

    print()

def delete_player(ids, gdpr, days, status):
    print("\n=== Delete a Player ===")
    search_id = input("Enter the Player ID to delete: ")

    if search_id not in ids:
        print("Player ID not found.")
        return

    # Find the index of the ID
    index = ids.index(search_id)

    # Delete from all lists
    del ids[index]
    del gdpr[index]
    del days[index]
    del status[index]

    print(f"Player {search_id} has been successfully deleted.")

def add_player(ids, gdpr, days, status):
    print("\n=== Register New Player ===")
    new_id = input("Enter new Player ID: ")

    # Check if ID already exists
    if new_id in ids:
        print("Error: That Player ID already exists.")
        return

    # Add new record with default values
    ids.append(new_id)
    gdpr.append("No")
    days.append(0)
    status.append("Active")

    print(f"Player {new_id} has been successfully added.")

def update_status(ids, status):
    print("\n=== Update Player Status ===")
    search_id = input("Enter the Player ID to update: ")

    # Check if ID exists
    if search_id not in ids:
        print("Player ID not found.")
        return

    # Find index
    index = ids.index(search_id)

    # Ask for new status
    new_status = input("Enter new status (Active/Locked/Disabled): ")

    # Update the status list
    status[index] = new_status

    print(f"Status for player {search_id} has been updated to {new_status}.")

def save_data(filename, ids, gdpr, days, status):
    print("\nSaving data to file...")

    with open(filename, "w") as file:
        for i in range(len(ids)):
            line = f"{ids[i]},{gdpr[i]},{days[i]},{status[i]}\n"
            file.write(line)

    print("Data saved successfully.")


def percentage_types(ids):
 
    """
    Calculates and prints the percentage of Casual and Professional gamers
    based on the list of player IDs.
    A player is considered Casual if the ID starts with 'CAS'.
    Otherwise, the player is considered Professional.
    """

    print("\n=== Gamer Type Percentages ===")

    total = len(ids)  # Total number of players in the system

    # Safety check: avoid division by zero
    if total == 0:
        print("No players found.")
        return

    casual_count = 0
    pro_count = 0

     # Loop through all IDs and classify each player
    for player_id in ids:
        if player_id.startswith("CAS"):
            casual_count += 1
        else:
            pro_count += 1

    # Calculate percentages
    casual_percentage = (casual_count / total) * 100
    pro_percentage = (pro_count / total) * 100

    # Print the results
    print(f"Total gamers: {total}")
    print(f"Casual gamers: {casual_percentage:.2f}%")
    print(f"Professional gamers: {pro_percentage:.2f}%")


def write_status_files(ids, status):
    """
    Writes gamer IDs into separate files based on their account status.
    - Locked players → locked.txt
    - Active players → active.txt
    - Disabled players → disabled.txt

    Parameters:
        ids (list): List of gamer IDs
        status (list): List of gamer statuses (Active / Locked / Disabled)

    Returns:
        None
    """

    # Open all three files in write mode (this clears old content)
    locked_file = open("locked.txt", "w")
    active_file = open("active.txt", "w")
    disabled_file = open("disabled.txt", "w")

    # Loop through all gamers and write their IDs to the appropriate file
    for i in range(len(ids)):
        player_id = ids[i]
        player_status = status[i]

        # Write each ID to the correct file based on status
        if player_status == "Locked":
            locked_file.write(player_id + "\n")
        elif player_status == "Active":
            active_file.write(player_id + "\n")
        elif player_status == "Disabled":
            disabled_file.write(player_id + "\n")

    # Close all files
    locked_file.close()
    active_file.close()
    disabled_file.close()       

    print("Player IDs have been written to locked.txt, active.txt, and disabled.txt.")


def disable_unpaid_accounts(gdpr, status):
    """
    Disables accounts that have not paid the membership fee.
    A player is disabled ONLY if:
        - Their GDPR/paid value is "No"
        - Their current status is "Active"

    Locked or Disabled accounts are NOT changed.

    Parameters:
        gdpr (list): List containing "Yes" or "No" for payment status
        status (list): List containing account statuses (Active / Locked / Disabled)

    Returns:
        int: Number of accounts that were updated (set to Disabled)
    """

    updated_count = 0  # Counter for how many accounts were changed

    # Loop through all players
    for i in range(len(status)):
        # Check if the player has not paid and is currently Active
        if gdpr[i] == "No" and status[i] == "Active":
            status[i] = "Disabled"  # Update status to Disabled
            updated_count += 1  # Increment the counter

    return updated_count

def menu():
    filename = "gamers.txt"
    ids, gdpr, days, status = read_file(filename)
    choice = ""
    while choice != "8":
        print("\nMenu")
        print("1. View all players")
        print("2. Delete a player")
        print("3. Register new player")
        print("4. Update player status")
        print("5. Percentage of Casual vs Professional gamers")
        print("6. Write status files")
        print("7. Update unpaid accounts to Disabled")
        print("8. Quit and save")
        choice = input("Enter choice: ")

        if choice == "1":
            view_all(ids, gdpr, days, status)
        elif choice == "2":
            delete_player(ids, gdpr, days, status)
        elif choice == "3":
            add_player(ids, gdpr, days, status)
        elif choice == "4":
            update_status(ids, status)
        elif choice == "5":
            percentage_types(ids)
        elif choice == "6":
            write_status_files(ids, status)
        elif choice == '7':
            updated_count = disable_unpaid_accounts(gdpr, status)
            print(f"{updated_count} accounts have been updated to Disabled.")
        elif choice == "8":
            save_data(filename, ids, gdpr, days, status)
            print("Data saved. Goodbye.")
        else:
            print("Invalid choice.")


if __name__ == '__main__':
    menu()