from tkinter import *
import random
import time

# Αρχικοποίηση διαφορετικής αλληλουχίας για να έχουμε κάθε φορά διαφορετικά αποτελέσματα
random.seed(time.time())

PLAYER_NAME = ""
player_table = [[] for i in range(11)]
enemy_table = [[] for i in range(11)]
battleships = {"aircraft_carrier": [0, 5],
               "battleship": [0, 4],
               "cruiser": [0, 3],
               "destroyer": [0, 2]}
# Μία λίστα η οποία περιέχει όλες τις δυνατές επιλογές που μπορεί να κάνει ο υπολογιστής
# κατά τη διάρκεια της βολής του
CPU_random_choice = []
for y in range(11):
    for x in range(10):
        CPU_random_choice.append([x, y])
# Μία λίστα με συνένωση συντεταγμένων σε περίπτωση επιτυχής βολής
CPU_random_choice_if_hit = ["",[]]
HIT = False
# Μία λίστα με τις συντεταγμένες των πλοίων του εχθρού
enemy_battleships = []
# Λίστα με τα κουμπιά που αλλάζουν ανάλογα με τις επιλογές του παίχτη
enemy_right_wrong_buttons = [[], []]
# Λίστα με τις ταμπέλες που αλλάζουν ανάλογα με τις επιλογές του Υπολογιστή
friendly_right_wrong_labels = [[], []]

# Score counter
PLAYER_SCORE = 0
PC_SCORE = 0


class Ship:
    """
    Μία κλάση η οποία περιέχει όλες τις απαραίτητες πληροφορίες για κάθε αντικείμενο Ship
    έτσι ώστε να μπορεί να το διαχειριστεί το παιχνίδι.

    Τα αντικείμενα χωρίζονται και αρχικοποιούνται με βάση το μέγεθός τους.
    """

    def __init__(self, size):
        self.coordinates = []
        self.adjacent_coordinates = []
        self.size = size
        self.labels = []
        self.buttons = []
        self.adjacent_buttons = []

    def create_ship_labels(self, frame_player):
        """Δημιουργεί όλες τις ετικέτες που δείχνουν τη θέση των φίλιων πλοίων."""

        for size in range(self.size+1):
            label = Label(frame_player, width=6, height=3, bg="blue")
            self.labels.append(label)

    def create_ship_buttons(self):
        """Δημιουργεί όλα τα κουμπιά που δείχνουν τη θέση των φίλιων πλοίων."""

        for size in range(self.size+1):
            button = Button(window, width=9, height=4, bg="blue", state=DISABLED)
            self.buttons.append(button)

    def create_ship_adjacent_buttons(self):
        """Δημιουργεί όλα τα κουμπιά που οριοθετούν τη θέση των φίλιων πλοίων μέσα στον χάρτη."""

        for size in range((self.size*5)):
            button = Button(window, width=9, height=4, state=DISABLED)
            self.adjacent_buttons.append(button)


def create_ship(ship):
    """
    Συνάρτηση τοποθέτησης Πλοίων

    Η συνάρτηση αυτή χρησιμοποιείται για την προσθήκη στο ταμπλό των πλοίων του χρήστη.
    Βοηθάει τον χρήστη να εισάγει ένα ένα τα πλοία του αποφεύγοντας collisions και ταυτόχρονα
    αποθηκεύοντας τις συντεταγμένες τους για μετέπειτα χρήση.
    """

    # Γίνεται η επιλογή Πλοίου, έπειτα στο αρχικό λεξικό σημειώνεται ότι δημιουργήθηκε
    # και επίσης προστίθεται.
    if ship == "aircraft_carrier":
        aircraft_carrier = Ship(battleships[ship][1])
        battleships[ship].append(aircraft_carrier)
    elif ship == "battleship":
        battleship = Ship(battleships[ship][1])
        battleships[ship].append(battleship)
    elif ship == "cruiser":
        cruiser = Ship(battleships[ship][1])
        battleships[ship].append(cruiser)
    else:
        destroyer = Ship(battleships[ship][1])
        battleships[ship].append(destroyer)

    for widget in window.winfo_children():
        widget.destroy()

    def starting_coords(x, y):
        """Συνάρτηση η οποία δημιουργεί συναρτήσεις για κάθε κουμπί του ταμπλό διαφορετικές για τα
        διάφορα x και y."""

        def ship_coords():
            """
            Συνάρτηση αρχικοποίησης συντεταγμένων για κάθε αντικείμενο πλοίου

            Η Συνάρτηση αυτή ανάλογα με το κουμπί που θα επιλέξει ο χρήστης δίνει στο μόλις δημιουργηθέν
            αντικείμενο πλοίου αρχικές συντεταγμένες κεφαλής.
            Έπειτα, ανάλογα με την κατεύθυνση που θα επιλέξει ο χρήστης, συμπληρώνει τις υπόλοιπες
            συντεταγμένες του αντικειμένου σύμφωνα με το μέγεθος του.
            Τέλος, δημιουργεί ένα χώρο γύρο απο το κάθε αντικείμενο στο οποίο ο χρήστης δεν μπορεί να
            τοποθετήσει άλλο αντικείμενο.
            """

            def fill_ship_coords(direction):
                """Ανάλογα με τη δοθείσα κατεύθυνση συμπληρώνει τις συντεταγμένες του αντικειμένου."""

                if direction == "up":
                    for size in range(1, battleships[ship][2].size):
                        battleships[ship][2].coordinates.append([x, y-size])
                    for size in range(battleships[ship][2].size):
                        if x-1 >= 0:
                            battleships[ship][2].adjacent_coordinates.append([x-1, y-size])
                        if x+1 < 10:
                            battleships[ship][2].adjacent_coordinates.append([x+1, y-size])
                    for i in range(3):
                        if y+1 < 11 and 0 <= x - 1 + i < 10:
                            battleships[ship][2].adjacent_coordinates.append([x-1+i, y+1])
                    for i in range(3):
                        if y-battleships[ship][2].size and 0 <= x - 1 + i < 10:
                            battleships[ship][2].adjacent_coordinates.append([x-1+i, y-battleships[ship][2].size])
                elif direction == "down":
                    for size in range(1, battleships[ship][2].size):
                        battleships[ship][2].coordinates.append([x, y+size])
                    for size in range(battleships[ship][2].size):
                        if x - 1 >= 0:
                            battleships[ship][2].adjacent_coordinates.append([x-1, y+size])
                        if x + 1 < 10:
                            battleships[ship][2].adjacent_coordinates.append([x+1, y+size])
                    for i in range(3):
                        if y-1 >= 0 and 0 <= x - 1 + i < 10:
                            battleships[ship][2].adjacent_coordinates.append([x-1+i, y-1])
                    for i in range(3):
                        if y+battleships[ship][2].size < 11 and 0 <= x - 1 + i < 10:
                            battleships[ship][2].adjacent_coordinates.append([x-1+i, y+battleships[ship][2].size])
                elif direction == "right":
                    for size in range(1, battleships[ship][2].size):
                        battleships[ship][2].coordinates.append([x+size, y])
                    for size in range(battleships[ship][2].size):
                        if y-1 >= 0:
                            battleships[ship][2].adjacent_coordinates.append([x+size, y-1])
                        if y+1 < 11:
                            battleships[ship][2].adjacent_coordinates.append([x+size, y+1])
                    for i in range(3):
                        if x-1 >= 0 and 0 <= y-1+i < 11:
                            battleships[ship][2].adjacent_coordinates.append([x-1, y-1+i])
                    for i in range(3):
                        if x+battleships[ship][2].size < 10 and 0 <= y-1+i < 11:
                            battleships[ship][2].adjacent_coordinates.append([x+battleships[ship][2].size, y-1+i])
                else:
                    for size in range(1, battleships[ship][2].size):
                        battleships[ship][2].coordinates.append([x-size, y])
                    for size in range(battleships[ship][2].size):
                        if y-1 >= 0:
                            battleships[ship][2].adjacent_coordinates.append([x-size, y-1])
                        if y+1 < 11:
                            battleships[ship][2].adjacent_coordinates.append([x-size, y+1])
                    for i in range(3):
                        if x+1 < 10 and 0 <= y-1+i < 11:
                            battleships[ship][2].adjacent_coordinates.append([x+1, y-1+i])
                    for i in range(3):
                        if x-battleships[ship][2].size >= 0 and 0 <= y-1+i < 11:
                            battleships[ship][2].adjacent_coordinates.append([x-battleships[ship][2].size, y-1+i])

                new_game(window, False, True)

            # Αρχικοποίηση συντεταγμένων κεφαλής αντικειμένου.
            battleships[ship][2].coordinates.append([x, y])

            for widget in window.winfo_children():
                widget.destroy()

            # Κουμπιά για επιλογή κατεύθυνσης πλοίου
            up = Button(window, text="Up", command=lambda: fill_ship_coords("up"))
            down = Button(window, text="Down", command=lambda: fill_ship_coords("down"))
            left = Button(window, text="Left", command=lambda: fill_ship_coords("left"))
            right = Button(window, text="Right", command=lambda: fill_ship_coords("right"))

            # Τοποθέτηση στου πλέγμα
            up.grid(column=1, row=0)
            down.grid(column=1, row=2)
            left.grid(column=0, row=1)
            right.grid(column=2, row=1)

            # Έλεγχος για έξοδο πλοίου εκτός ορίων.
            if battleships[ship][2].coordinates[0][0] - battleships[ship][2].size + 1 < 0:
                left.config(state=DISABLED)
            if battleships[ship][2].coordinates[0][0] + battleships[ship][2].size - 1 > 9:
                right.config(state=DISABLED)
            if battleships[ship][2].coordinates[0][1] - battleships[ship][2].size + 1 < 0:
                up.config(state=DISABLED)
            if battleships[ship][2].coordinates[0][1] + battleships[ship][2].size - 1 > 10:
                down.config(state=DISABLED)

            # Έλεγχος για σύγκρουση μεταξύ ήδη προϋπάρχων πλοίων προς κάθε κατεύθυνση.

            for someship in battleships.keys():
                if battleships[someship][0] == 1 and someship != ship:
                    for i in range(battleships[ship][2].size):
                        for x_someship in battleships[someship][2].adjacent_coordinates:
                            if (battleships[ship][2].coordinates[0][0] + i == x_someship[0] and
                                    battleships[ship][2].coordinates[0][1] == x_someship[1]):
                                right.config(state=DISABLED)
                                break

            for someship in battleships.keys():
                if battleships[someship][0] == 1 and someship != ship:
                    for i in range(battleships[ship][2].size):
                        for x_someship in battleships[someship][2].adjacent_coordinates:
                            if (battleships[ship][2].coordinates[0][0] - i == x_someship[0] and
                                    battleships[ship][2].coordinates[0][1] == x_someship[1]):
                                left.config(state=DISABLED)
                                break

            for someship in battleships.keys():
                if battleships[someship][0] == 1 and someship != ship:
                    for i in range(battleships[ship][2].size):
                        for x_someship in battleships[someship][2].adjacent_coordinates:
                            if (battleships[ship][2].coordinates[0][1] + i == x_someship[1] and
                                    battleships[ship][2].coordinates[0][0] == x_someship[0]):
                                down.config(state=DISABLED)
                                break

            for someship in battleships.keys():
                if battleships[someship][0] == 1 and someship != ship:
                    for i in range(battleships[ship][2].size):
                        for x_someship in battleships[someship][2].adjacent_coordinates:
                            if (battleships[ship][2].coordinates[0][1] - i == x_someship[1] and
                                    battleships[ship][2].coordinates[0][0] == x_someship[0]):
                                up.config(state=DISABLED)
                                break

            # Κουμπί για έξοδο σε περίπτωση επιθυμίας του χρήστη.
            Button(window, text="Back", command=lambda: cancel(ship)).grid(row=4, column=1)

            center_window(window)

            # Επισήμανση δημιουργίας του αντικειμένου στο αρχικό λεξικό μας.
            battleships[ship][0] = 1

        return ship_coords

    # Αρχικοποίηση Κουμπιών στο ταμπλό προσθήκης πλοίων του χρήστη.
    for y in range(11):
        for x in range(10):
            ship_coords = starting_coords(x, y)  # Ορίζεται στην αρχή της συνάρτησης
            button = Button(window, text=f"{x+1}, {y+1}",
                            width=9, height=4, command=ship_coords)
            button.grid(row=y, column=x)

    # Αρχικοποίηση των λιστών με τα κουμπιά των αντικειμένων θα πρέπει να ξανά δημιουργηθούν και να ξανά
    # μπουν στο πλέγμα.
    for someship in battleships.keys():
        if battleships[someship][0] == 1:
            battleships[someship][2].buttons = []
            battleships[someship][2].adjacent_buttons = []

    # Αντικατάσταση των κουμπιών του πλέγματος με κουμπιά τα οποία υποδηλώνουν τη θέση των πλοίων
    # καθώς και τον περιορισμό τοποθέτησης άλλων πλοίων δίπλα σε αυτά
    for someship in battleships.keys():
        if battleships[someship][0] == 1:
            battleships[someship][2].create_ship_buttons()
            battleships[someship][2].create_ship_adjacent_buttons()
            for i in range(len(battleships[someship][2].buttons)-1):
                battleships[someship][2].buttons[i].grid(row=battleships[someship][2].coordinates[i][1],
                                                         column=battleships[someship][2].coordinates[i][0])
            for i in range(len(battleships[someship][2].adjacent_coordinates)):
                battleships[someship][2].adjacent_buttons[i].grid(row=battleships[someship][2].adjacent_coordinates[i][1],
                                                                  column=battleships[someship][2].adjacent_coordinates[i][0])

    center_window(window)


def cancel(ship):
    """Συνάρτηση η οποία επιτρέπει επιστροφή στην επιλογή πλοίου στην περίπτωση που θελήσει ο Χρήστης"""

    battleships[ship][0] = 0
    del battleships[ship][2]
    add_ship()


def add_ship():
    """
        Συνάρτηση ελεγχόμενης προσθήκης πλοίου.

        Η συνάρτηση αυτή εμφανίζει ένα παράθυρο το οποίο περιέχει ΜΟΝΟ πλοία τα οποία δεν έχει
        τοποθετήσει ο Χρήστης και εισάγει σε αυτά ως command μία συνάρτηση η οποία δημιουργεί
        το συγκεκριμένο αντικείμενο πλοίου που θα επιλέξει ο χρήστης.
        """

    for widget in window.winfo_children():
        widget.destroy()

    # Κουμπί για δημιουργία πλοίου τύπου Aircraft Carrier.
    aircraft_carrier_add = Button(window, text="aircraft_carrier",
                                  command=lambda: create_ship("aircraft_carrier"))
    # Κουμπί για δημιουργία πλοίου τύπου BattleShip.
    battleship_add = Button(window, text="battleship",
                            command=lambda: create_ship("battleship"))
    # Κουμπί για δημιουργία πλοίου τύπου Cruiser.
    cruiser_add = Button(window, text="cruiser",
                         command=lambda: create_ship("cruiser"))
    # Κουμπί για δημιουργία πλοίου τύπου Destroyer.
    destroyer_add = Button(window, text="destroyer",
                           command=lambda: create_ship("destroyer"))

    battleships_buttons = {"aircraft_carrier": aircraft_carrier_add,
                           "battleship": battleship_add,
                           "cruiser": cruiser_add,
                           "destroyer": destroyer_add}

    # Γίνεται έλεγχος για το αν δεν υπάρχει αντικείμενο πλοίου και εισάγεται το ανάλογο
    # κουμπί στο παράθυρο
    for ship in battleships.keys():
        if battleships[ship][0] == 0:
            battleships_buttons[ship].pack()

    center_window(window)


def del_ship(ship):
    """Συνάρτηση η οποία διαγράφει ένα αντικείμενο πλοίου"""

    del battleships[ship][2]
    battleships[ship][0] = 0
    new_game(window, False, True)


def remove_ship():
    """
    Συνάρτηση ελεγχόμενης αφαίρεσης πλοίου.

    Η συνάρτηση αυτή εμφανίζει ένα παράθυρο το οποίο περιέχει ΜΟΝΟ πλοία τα οποία έχει τοποθετήσει
    ο Χρήστης και εισάγει σε αυτά ως command μία συνάρτηση η οποία διαγράφει το συγκεκριμένο
    αντικείμενο πλοίου που θα επιλέξει ο χρήστης.
    """

    for widget in window.winfo_children():
        widget.destroy()

    aircraft_carrier_remove = Button(window, text="aircraft_carrier",
                                     command=lambda: del_ship("aircraft_carrier"))
    battleship_remove = Button(window, text="battleship",
                               command=lambda: del_ship("battleship"))
    cruiser_remove = Button(window, text="cruiser",
                            command=lambda: del_ship("cruiser"))
    destroyer_remove = Button(window, text="destroyer",
                              command=lambda: del_ship("destroyer"))

    battleships_buttons_remove = {"aircraft_carrier": aircraft_carrier_remove,
                                  "battleship": battleship_remove,
                                  "cruiser": cruiser_remove,
                                  "destroyer": destroyer_remove}

    for ship in battleships.keys():
        if battleships[ship][0] == 1:
            battleships_buttons_remove[ship].pack()

    center_window(window)


def start_game():
    """
    Συνάρτηση έναρξης παιχνιδιού.

    Με τη συνάρτηση αυτή ο Υπολογιστής τοποθετεί τα πλοία του και ξεκινάει το παιχνίδι
    """

    global CPU_random_choice

    ship = 2
    while ship != 6:
        # Συντεταγμένες για να επιλέξει ο υπολογιστής κατεύθυνση
        x = [-1, 1]
        y = [-1, 1]
        # Διαλέξει ένα τυχαίο σημείο στο πλαίσιο
        coords = random.choice(CPU_random_choice)
        CPU_random_choice.remove(coords)
        direction = random.choice(["x", "y"])
        # Περιορισμοί σε περίπτωση σύγκρουσης
        if direction == "x":
            y = [0]
            if coords[0]-ship+1 < 0:
                x.remove(-1)
            if coords[0]+ship > 9:
                x.remove(1)
            if not x:
                break
        if direction == "y":
            x = [0]
            if coords[1]-ship+1 < 0:
                y.remove(-1)
            if coords[1]+ship > 10:
                y.remove(1)
            if not y:
                break
        enemy_ship = [coords]
        random_x = random.choice(x)
        random_y = random.choice(y)
        for i in range(ship-1):
            enemy_ship += [[coords[0]+(1+i)*random_x, coords[1]+(1+i)*random_y]]
        # Περιορισμοί σε περίπτωση επαφής με άλλο πλοίο
        if enemy_battleships:
            for enemy_battleship_coords in enemy_battleships:
                for enemy_ship_coords in enemy_ship:
                    if enemy_ship_coords == enemy_battleship_coords:
                        break
        for i in enemy_ship:
            enemy_battleships.append(i)

        ship += 1

    # Ανακατασκευή της λίστας CPU_random_choice
    CPU_random_choice = []
    for y in range(11):
        for x in range(10):
            CPU_random_choice.append([x, y])

    new_game(window, False, False)


def center_window(window):
    """
    Μία Συνάρτηση κεντραρίσματος.

    Κεντράρει το παράθυρο αφού λάβει υπόψη τα νέα δεδομένα για το μέγεθός του!
    """

    window.geometry("")
    window.update()
    x = int(window.winfo_screenwidth()/2 - window.winfo_width()/2)
    y = int(window.winfo_screenheight() / 2 - window.winfo_height() / 2)
    window.geometry(f"{window.winfo_width()}x{window.winfo_height()}+{x}+{y}")


def new_game(window, entry_box, start_frame):
    """
    Έναρξη νέου παιχνιδιού.

    Αυτή η συνάρτηση αποθηκεύει στην καθολική μεταβλητή το όνομα που θα δηλώσει ο
    παίχτης και έπειτα διαγράφει τα αντικείμενα του προηγούμενου παραθύρου
    προσθέτοντας τα νέα!
    """

    player_table = [[] for i in range(11)]
    enemy_table = [[] for i in range(11)]

    global PLAYER_NAME, PLAYER_SCORE, PC_SCORE
    if entry_box:
        PLAYER_NAME = ""
        PLAYER_NAME = player_name_box.get()

    # Συνάρτηση η οποία δέχεται τη θέση του κάθε κουμπιού και επιστρέφει διαφορετική εντολή για κάθε κουμπί
    def enemy_buttons(x, y):
        # Συνάρτηση διαφορετική για κάθε κουμπί
        def enemy():
            global PLAYER_SCORE
            global PC_SCORE
            global HIT
            global CPU_random_choice_if_hit

            label_1 = Label(window, text=f"Κάνατε πυρά στο σημείο ({x-1}, {y-1})")
            label_2 = Label(window, text="Παρακαλώ περιμένετε")
            if [x, y] in enemy_battleships:
                enemy_right_wrong_buttons[0].append([x, y])
                PLAYER_SCORE += 1
                label_2.config(text="Πετύχατε κάποιο εχθρικό πλοίο!!")
            else:
                enemy_right_wrong_buttons[1].append([x, y])
                label_2.config(text="Τα πυρά σας ήταν εκτός στόχου!!")

            if not HIT:
                enemy_choice = random.choice(CPU_random_choice)
            else:
                if CPU_random_choice_if_hit[1]:
                    enemy_choice = random.choice(CPU_random_choice_if_hit[1])
                else:
                    HIT = False
                    del battleships[CPU_random_choice_if_hit[0]]
                    enemy_choice = random.choice(CPU_random_choice)

            if not HIT:
                for ship in battleships.keys():
                    for ship_coords in battleships[ship][2].coordinates:
                        if enemy_choice == ship_coords:
                            friendly_right_wrong_labels[0].append(enemy_choice)
                            CPU_random_choice_if_hit[1] = battleships[ship][2].coordinates + battleships[ship][2].adjacent_coordinates
                            i = 0
                            while i < len(CPU_random_choice_if_hit[1]):
                                if CPU_random_choice_if_hit[1][i] not in CPU_random_choice:
                                    CPU_random_choice_if_hit[1].remove(CPU_random_choice_if_hit[1][i])
                                else:
                                    i += 1
                            CPU_random_choice_if_hit[0] = ship
                            CPU_random_choice_if_hit[1].remove(enemy_choice)
                            HIT = True
                            CPU_random_choice.remove(enemy_choice)
                            PC_SCORE += 1
                            break
            else:
                if enemy_choice in battleships[CPU_random_choice_if_hit[0]][2].coordinates:
                    friendly_right_wrong_labels[0].append(enemy_choice)
                    CPU_random_choice.remove(enemy_choice)
                    CPU_random_choice_if_hit[1].remove(enemy_choice)
                    PC_SCORE += 1
                else:
                    friendly_right_wrong_labels[1].append(enemy_choice)
                    CPU_random_choice.remove(enemy_choice)
                    CPU_random_choice_if_hit[1].remove(enemy_choice)

            if not HIT:
                CPU_random_choice.remove(enemy_choice)
                friendly_right_wrong_labels[1].append(enemy_choice)

            new_game(window, False, False)

        return enemy

    # Αφαιρεί τη δυνατότητα χρήσης του Enter
    window.unbind("<Return>")

    for widget in window.winfo_children():
        widget.destroy()

    # All widgets for the game
    # Ετικέτα που εμφανίζει στο παράθυρο το όνομα παίχτη
    active_player = Label(window,
                          text=f"{PLAYER_NAME}",
                          font=("Comic Sans MS", 20))
    active_player.grid(row=0, column=1, columnspan=2)
    # Ετικέτα που εμφανίζει στο παράθυρο το Score
    score = Label(window,
                  text=f"{PLAYER_NAME}: {PLAYER_SCORE}\tCPU: {PC_SCORE}",
                  font=("Comic Sans MS", 15))
    score.grid(row=1, column=1, columnspan=2)

    # Μία δομή για αποθήκευση όλων των ετικετών που απαρτίζουν το Ταμπλό του Παίχτη
    frame_player = Frame(window)
    # Μία δομή για αποθήκευση όλων των κουμπιών που απαρτίζουν το Ταμπλό του Εχθρού
    frame_enemy = Frame(window, padx=15, pady=15)
    # Μία δομή για αποθήκευση των κουμπιών για τοποθέτηση πλοίων
    frame_ship_input = Frame(window, padx=15, pady=15, name="frame_ship_input")
    # Μία δομή για αποθήκευση των κουμπιών "Νέο Παιχνίδι" και "Έξοδος"
    frame_start_stop = Frame(window)

    # Τοποθέτηση κουμπιών στη δομή start_stop
    # Κουμπί για πιθανή έναρξη νέου παιχνιδιού
    Button(frame_start_stop, text="Νέο Παιχνίδι",
           font=("Comic Sans MS", 15)).grid(row=0, column=0, padx=15)
    # Κουμπί για πιθανή έξοδος απο το Παιχνίδι
    Button(frame_start_stop, text="Έξοδος",
           font=("Comic Sans MS", 15)).grid(row=0, column=1, padx=15)

    # Τοποθέτηση κουμπιών στη δομή ship_input
    # Κουμπί για προσθήκη Πλοίου
    ship_add = Button(frame_ship_input, text="Πρόσθεσε Πλοίο", command=add_ship,
                      font=("Comic Sans MS", 15), state=DISABLED)
    # Κουμπί για αφαίρεση Πλοίου
    ship_remove = Button(frame_ship_input, text="Διέγραψε Πλοίο", command=remove_ship,
                         font=("Comic Sans MS", 15), state=DISABLED)
    # Κουμπί για Έναρξη Παιχνιδιού
    start = Button(frame_ship_input, text="Έναρξη παιχνιδιού",
                   font=("Comic Sans MS", 15),
                   command=start_game)
    start.grid(row=1, column=0, columnspan=2, padx=10)
    ship_add.grid(row=0, column=0, padx=10)
    ship_remove.grid(row=0, column=1, padx=10)

    # Στοίχιση δομών στο παράθυρο
    frame_player.grid(row=3, column=1, columnspan=2)
    frame_enemy.grid(row=0, column=0, rowspan=5)
    if start_frame:
        frame_ship_input.grid(row=6, column=0, rowspan=2)
    frame_start_stop.grid(row=4, column=1, columnspan=2)

    # Δημιουργία και εισαγωγή των κουμπιών στο ταμπλό του εχθρού
    for y in range(11):
        for x in range(10):
            enemy = enemy_buttons(x, y)  # Ορίζεται στην αρχή της συνάρτησης
            button = Button(frame_enemy, text=f"{x+1}, {y+1}",
                            width=9, height=4, state=DISABLED, command=enemy)
            # Τα κουμπιά θα είναι ενεργά μόνο όταν ξεκινήσει το παιχνίδι
            if not start_frame:
                button.config(state=NORMAL)
            enemy_table[y].append(button)
            enemy_table[y][x].grid(row=y, column=x)

    # Δημιουργία και εισαγωγή των ετικετών στο ταμπλό του Παίχτη
    for y in range(11):
        for x in range(10):
            label = Label(frame_player, text=f"{x+1}, {y+1}",
                          width=6, height=3)
            player_table[x].append(label)
            player_table[x][y].grid(column=x, row=y)

    # Έλεγχος αν έχει εισάγει ο χρήστης Πλοίο
    # Αν ναι τότε καθαρίζει για κάθε πλοίο που υπάρχει τις ετικέτες
    for ship in battleships.keys():
        if battleships[ship][0] == 1:
            battleships[ship][2].labels = []

    # Δημιουργία για κάθε πλοίο ετικέτες που αντιστοιχούν στη θέση του πλοίου στο ταμπλό
    for ship in battleships.keys():
        if battleships[ship][0] == 1:
            battleships[ship][2].create_ship_labels(frame_player)
            for i in range(len(battleships[ship][2].labels)-1):
                battleships[ship][2].labels[i].grid(row=battleships[ship][2].coordinates[i][1],
                                                    column=battleships[ship][2].coordinates[i][0])

    # Ενεργοποίηση ή Απενεργοποίηση κουμπιών όπου χρειάζεται
    for ship in battleships.keys():
        if battleships[ship][0] == 0:
            start.config(state=DISABLED)
            ship_add.config(state=NORMAL)
            break

    for ship in battleships.keys():
        if battleships[ship][0] == 1:
            ship_remove.config(state=NORMAL)
            break

    if enemy_right_wrong_buttons[0]:
        for button in enemy_right_wrong_buttons[0]:
            enemy_table[button[1]][button[0]].config(state=DISABLED, bg="red")

    if enemy_right_wrong_buttons[1]:
        for button in enemy_right_wrong_buttons[1]:
            enemy_table[button[1]][button[0]].config(state=DISABLED, bg="white")

    if friendly_right_wrong_labels[0]:
        for label_coords in friendly_right_wrong_labels[0]:
            Label(frame_player, text=f"{label_coords[0] + 1}, {label_coords[1] + 1}",
                  width=6, height=3, bg="red").grid(row=label_coords[1], column=label_coords[0])

    if friendly_right_wrong_labels[1]:
        for label_coords in friendly_right_wrong_labels[1]:
            Label(frame_player, text=f"{label_coords[0] + 1}, {label_coords[1] + 1}",
                  width=6, height=3, bg="white").grid(row=label_coords[1], column=label_coords[0])

    center_window(window)


window = Tk()
window.title("Ναυμαχία The E-Game")
image = PhotoImage(file="Battleship_icon.png")
window.iconphoto(True, image)
window.resizable(False, False)

# All widgets for the give player Name
player_name_label = Label(window,
                          text="Παρακαλώ δώστε το όνομά σας:",
                          font=("Comic Sans MS", 20, "bold"))
player_name_box = Entry(window,
                        width=20,
                        font=("Comic Sans MS", 20),
                        justify=CENTER)
player_name_button = Button(window,
                            text="Νέο Παιχνίδι",
                            font=("Comic Sans MS", 14, "bold"),
                            command=lambda: new_game(window, True, True))

player_name_label.pack()
player_name_box.pack()
player_name_button.pack()
center_window(window)

# Προσθέτει τη δυνατότητα καταχώρησης ονόματος με το Enter
window.bind("<Return>", lambda event: new_game(window, True, True))


window.mainloop()
