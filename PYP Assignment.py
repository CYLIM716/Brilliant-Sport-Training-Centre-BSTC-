
def login():
    attempts = 0
    max_attempts = 3
    while attempts < max_attempts:
        username = input("Username: ")
        password = input("Password: ")
        with open("users.txt", "r") as file:
            for line in file:
                role, user, pwd = line.strip().split(",")
                if user == username and pwd == password:
                    print(f"Login successful! Welcome {username} ({role})")
                    return role, username
        attempts += 1
        print(f"Invalid credentials. {max_attempts - attempts} attempts left.")
    print("Too many failed login attempts.")
    return None, None


def admin_menu(username):
    while True: #This creates an infinite loop, ensuring the menu keeps showing until the user chooses to log out.
        print(f"\n[Admin Menu - Logged in as {username}]")
        print("1. Register Coach") 
        print("2. Delete Coach")
        print("3. Register Receptionist")
        print("4. Delete Receptionist")
        print("5. Assign Coach to Training")
        print("6. View Monthly Income Report")
        print("7. Update Own Profile")
        print("0. Logout")

        choice = input("Enter your choice: ")#Each if or elif block handles one specific menu choice:

        if choice == "1":
            register_user("coach")
        elif choice == "2":
            delete_user("coach")
        elif choice == "3":
            register_user("receptionist")
        elif choice == "4":
            delete_user("receptionist")
        elif choice == "5":
            assign_coach()
        elif choice == "6":
            view_income_report()
        elif choice == "7":
            update_profile(username)
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")#If the input doesn't match any expected option, a warning is shown.



def register_user(role):
    print(f"\n--- Register New {role.title()} ---")
    username = input("Username: ")

    with open("users.txt", "r") as file:
        for line in file:
            _, existing_user, _ = line.strip().split(",")
            if existing_user == username:
                print("Username already exists. Registration aborted.")
                return  

    password = input("Password: ")
    with open("users.txt", "a") as file:
        file.write(f"{role},{username},{password}\n")
    print(f"{role.title()} registered.")

def delete_user(role):
    print(f"\n--- Delete {role.title()} ---")
    username = input("Username to delete: ")
    lines = []
    deleted = False
    with open("users.txt", "r") as file:
        for line in file:
            r, user, pwd = line.strip().split(",")
            if r == role and user == username:
                deleted = True
                continue
            lines.append(line.strip())
    if deleted: # Updated
        with open("users.txt", "w") as file:
            for l in lines:
                file.write(l + "\n")
        print(f"{role.title()} deleted.")
    else:
        print(f"{role.title()} not found.")


def assign_coach():
    print("\n--- Assign Coach to Training ---")
    training_name = input("Training name: ")
    coach_username = input("Coach username: ")
    updated = False
    lines = []
    with open("trainings.txt", "r") as file:
        for line in file:
            name, fee, schedule, coach = line.strip().split(",")
            if name == training_name:
                lines.append(f"{name},{fee},{schedule},{coach_username}")
                updated = True
            else:
                lines.append(line.strip())
    if updated:
        with open("trainings.txt", "w") as file:
            for l in lines:
                file.write(l + "\n")
        print("Coach assigned.")
    else:
        print("Training not found.")

def view_income_report():
    print("\n--- Monthly Income Report ---")
    training_income = {}
    training_fees = {}
    with open("trainings.txt", "r") as file:
        for line in file:
            name, fee, _, _ = line.strip().split(",")
            training_fees[name] = float(fee)


    with open("trainees.txt", "r") as file: #Read Training Fees
        for line in file:
            parts = line.strip().split(",")
            if len(parts) >= 7: #Process Trainee Enrollments
                trainings = parts[6].split(";")
                for t in trainings:
                    t = t.strip()
                    if t in training_fees:
                        training_income[t] = training_income.get(t, 0) + training_fees[t] #handle first-time additions

    if training_income: #print final income
        print(f"{'Training Name':<20} {'Total Income (RM)':>20}")
        print("-" * 40)
        for name, total in training_income.items():
            print(f"{name:<20} {total:>20.2f}")
    else:
        print("No income data available.")


def update_profile(username):
    print("\n--- Update Password ---")
    new_password = input("Enter new password: ")
    lines = []
    with open("users.txt", "r") as file: #Read and Modify User Data
        for line in file:
            role, user, pwd = line.strip().split(",")
            if user == username: #If the username matches,replaces the old password with the new one.
                lines.append(f"{role},{user},{new_password}")
            else:
                lines.append(line.strip())
    with open("users.txt", "w") as file:# updated data
        for l in lines:
            file.write(l + "\n")
    print("Password updated.")


import os

def receptionist_menu(username):
    while True:
        print(f"\n[Receptionist Menu - Logged in as {username}]")
        print("1. Register Trainee")
        print("2. Enroll Trainee in Trainings")
        print("3. Update Trainee's Training")
        print("4. Accept Payment")
        print("5. Delete Completed Trainee")
        print("6. Update Own Profile")
        print("0. Logout")
        choice = input("Enter choice: ")

        if choice == "1":
            register_trainee()
        elif choice == "2":
            enroll_trainee()
        elif choice == "3":
            update_trainee_training()
        elif choice == "4":
            accept_payment()
        elif choice == "5":
            delete_trainee()
        elif choice == "6":
            update_profile(username)
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")


def register_trainee():
    print("\n--- Register New Trainee ---")
    username = input("Trainee Username: ")
    with open("users.txt", "r") as file:
        for line in file:
            _, existing_user, _ = line.strip().split(",")
            if existing_user == username:
                print("Username already exists.")
                return
    name = input("Full Name: ")
    ic = input("IC/Passport: ")
    email = input("Email: ")
    contact = input("Contact Number: ")
    address = input("Address: ")
    line = f"{username},{name},{ic},{email},{contact},{address},\n"
    with open("trainees.txt", "a") as file:
        file.write(line)
    print("Trainee registered. Default password is 'train123'")
    default_password = "train123"
    with open("users.txt", "a") as file:
        file.write(f"trainee,{username},{default_password}\n")


def enroll_trainee():
    print("\n--- Enroll Trainee ---")
    username = input("Trainee Username: ")
    trainings = input("Enter trainings (comma separated): ")
    lines = []
    found = False
    with open("trainees.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if parts[0] == username:
                found = True
                parts[-1] = ";".join([t.strip() for t in trainings.split(",")])
                lines.append(",".join(parts))
            else:
                lines.append(line.strip())
    if found:
        with open("trainees.txt", "w") as file:
            for l in lines:
                file.write(l + "\n")
        print("Trainee enrolled.")
    else:
        print("Trainee not found.")


def update_trainee_training():
    print("\n--- Update Training ---")
    username = input("Trainee Username: ")
    new_trainings = input("New trainings (comma separated): ")
    updated = False
    lines = []
    with open("trainees.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if parts[0] == username:
                parts[-1] = ";".join([t.strip() for t in new_trainings.split(",")])
                updated = True
            lines.append(",".join(parts))
    if updated:
        with open("trainees.txt", "w") as file:
            for l in lines:
                file.write(l + "\n")
        print("Training updated.")
    else:
        print("Trainee not found.")


def accept_payment():
    print("\n--- Accept Payment ---")
    username = input("Trainee Username: ")
    amount = float(input("Amount Paid: "))
    updated = False
    lines = []
    if not os.path.exists("payments.txt"):
        open("payments.txt", "w").close()
    with open("payments.txt", "r") as file:
        for line in file:
            u, total = line.strip().split(",")
            if u == username:
                new_total = float(total) + amount
                lines.append(f"{u},{new_total}")
                updated = True
            else:
                lines.append(line.strip())
    if not updated:
        lines.append(f"{username},{amount}")
    with open("payments.txt", "w") as file:
        for l in lines:
            file.write(l + "\n")
    print("Payment recorded.")


def delete_trainee():
    print("\n--- Delete Trainee ---")
    username = input("Trainee Username to delete: ")
    new_lines = []
    deleted = False

    with open("trainees.txt", "r") as file:
        for line in file:
            if not line.startswith(username + ","):
                new_lines.append(line.strip())
            else:
                deleted = True

    if deleted:
        with open("trainees.txt", "w") as file:
            for l in new_lines:
                file.write(l + "\n")
        updated_users = []
        with open("users.txt", "r") as file:
            for line in file:
                role, user, pwd = line.strip().split(",")
                if not (role == "trainee" and user == username):
                    updated_users.append(line.strip())
        with open("users.txt", "w") as file:
            for l in updated_users:
                file.write(l + "\n")
        print("Trainee deleted.")
    else:
        print("Trainee not found.")

def coach_menu(username):
    while True:
        print(f"\n[Coach Menu - Logged in as {username}]")
        print("1. Add Training Program")
        print("2. Update Training Program")
        print("3. Delete Training Program")
        print("4. View Enrolled Trainees")
        print("5. Update Own Profile")
        print("0. Logout")
        choice = input("Enter your choice: ")

        if choice == "1":
            add_training(username)
        elif choice == "2":
            update_training(username)
        elif choice == "3":
            delete_training(username)
        elif choice == "4":
            view_enrolled_trainees(username)
        elif choice == "5":
            update_profile(username)
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid choice. Try again.")


def add_training(coach_username):
    print("\n--- Add Training ---")
    name = input("Training name: ")
    fee = input("Fee (RM): ")
    schedule = input("Schedule (e.g. Mon 9AM): ")
    line = f"{name},{fee},{schedule},{coach_username}"
    with open("trainings.txt", "a") as file:
        file.write(line + "\n")
    print("Training added.")


def update_training(coach_username):
    print("\n--- Update Training ---")
    name = input("Training name to update: ")
    updated = False
    new_lines = []
    with open("trainings.txt", "r") as file:
        for line in file:
            t_name, fee, sched, coach = line.strip().split(",")
            if t_name == name and coach == coach_username:
                print("Leave field blank to keep current value.")
                new_fee = input(f"New fee (was {fee}): ") or fee
                new_sched = input(f"New schedule (was {sched}): ") or sched
                new_lines.append(f"{name},{new_fee},{new_sched},{coach_username}")
                updated = True
            else:
                new_lines.append(line.strip())
    if updated:
        with open("trainings.txt", "w") as file:
            for l in new_lines:
                file.write(l + "\n")
        print("Training updated.")
    else:
        print("Training not found or not owned by you.")


def delete_training(coach_username):
    print("\n--- Delete Training ---")
    name = input("Training name to delete: ")
    new_lines = []
    deleted = False
    with open("trainings.txt", "r") as file:
        for line in file:
            t_name, _, _, coach = line.strip().split(",")
            if t_name == name and coach == coach_username:
                deleted = True
                continue
            new_lines.append(line.strip())
    if deleted:
        with open("trainings.txt", "w") as file:
            for l in new_lines:
                file.write(l + "\n")
        print("Training deleted.")
    else:
        print("Training not found or not owned by you.")


def view_enrolled_trainees(coach_username):
    print("\n--- Enrolled Trainees ---")
    coach_trainings = []
    with open("trainings.txt", "r") as file:
        for line in file:
            t_name, _, _, coach = line.strip().split(",")
            if coach == coach_username:
                coach_trainings.append(t_name)
    if not coach_trainings:
        print("You have no trainings.")
        return

    with open("trainees.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if len(parts) < 7 or parts[6] == "":
                continue
            username, name, _, email, contact, _, trainings = parts
            enrolled = trainings.split(";")
            for t in enrolled:
                if t.strip() in coach_trainings:
                    print(f"Trainee: {name} ({username}) - Training: {t.strip()}")


def trainee_menu(username):
    while True:
        print(f"\n[Trainee Menu - Logged in as {username}]")
        print("1. View My Training Schedule")
        print("2. Send Request to Change Training")
        print("3. Delete Pending Change Request")
        print("4. View Payment Status")
        print("5. Update My Profile")
        print("0. Logout")

        choice = input("Enter your choice: ")

        if choice == "1":
            view_schedule(username)
        elif choice == "2":
            send_change_request(username)
        elif choice == "3":
            delete_change_request(username)
        elif choice == "4":
            view_payment_status(username)
        elif choice == "5":
            update_profile(username)
        elif choice == "0":
            print("Logging out...")
            break
        else:
            print("Invalid choice.")


def view_schedule(username):
    print("\n--- My Training Schedule ---")
    trainings = []
    with open("trainees.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if parts[0] == username and len(parts) >= 7:
                trainings = parts[6].split(";")
                break
    if not trainings:
        print("No trainings enrolled.")
        return

    with open("trainings.txt", "r") as file:
        for line in file:
            name, fee, schedule, _ = line.strip().split(",")
            if name in trainings:
                print(f"{name}: {schedule} (RM {fee})")


def send_change_request(username):
    print("\n--- Request Training Change ---")
    new_training = input("Enter training name to request: ")
    with open("requests.txt", "a") as file:
        file.write(f"{username},{new_training}\n")
    print("Change request sent.")


def delete_change_request(username):
    print("\n--- Delete Pending Request ---")
    lines = []
    removed = False
    with open("requests.txt", "r") as file:
        for line in file:
            user, training = line.strip().split(",")
            if user == username:
                removed = True
                continue
            lines.append(line.strip())
    if removed:
        with open("requests.txt", "w") as file:
            for l in lines:
                file.write(l + "\n")
        print("Request deleted.")
    else:
        print("No pending request found.")

def view_payment_status(username):
    print("\n--- Payment Status ---")
    total_fee = 0
    total_paid = 0

    trainings = []
    with open("trainees.txt", "r") as file:
        for line in file:
            parts = line.strip().split(",")
            if parts[0] == username:
                trainings = parts[6].split(";") if len(parts) >= 7 else []
                break

    with open("trainings.txt", "r") as file:
        for line in file:
            name, fee, _, _ = line.strip().split(",")
            if name in trainings:
                total_fee += float(fee)

    try:
        with open("payments.txt", "r") as file:
            for line in file:
                user, paid = line.strip().split(",")
                if user == username:
                    total_paid = float(paid)
                    break
    except FileNotFoundError:
        pass

    balance = total_fee - total_paid
    print(f"Total Fee: RM {total_fee:.2f}")
    print(f"Total Paid: RM {total_paid:.2f}")
    print(f"Outstanding Balance: RM {balance:.2f}")




def main():
    print("=== Welcome to Brilliant Sport-Training Centre (BSTC) System ===")
    role, username = login()
    if role == "admin":
        admin_menu(username)
    elif role == "receptionist":
        receptionist_menu(username)
    elif role == "coach":
        coach_menu(username)
    elif role == "trainee":
        trainee_menu(username)
    else:
        print("Invalid role.")
    
while True:
    main()
    ans = input("Do you want to continue? (y/n): ").lower()
    if ans != "y":
        break