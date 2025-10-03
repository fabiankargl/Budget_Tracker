import readchar

KEY_UP = readchar.key.UP
KEY_DOWN = readchar.key.DOWN
KEY_ENTER = readchar.key.ENTER

def select_category(categories) -> int:
    index = 0

    print("Kategorie mit Pfeiltasten auswählen und Enter drücken:")
    while True:
        for i, cat in enumerate(categories):
            prefix = "-> " if i == index else "  "
            print(f"{prefix}{cat}")
        key = readchar.readkey()
        if key == KEY_UP:
            index = (index - 1) % len(categories)
        elif key == KEY_DOWN:
            index = (index + 1) % len(categories)
        elif key == KEY_ENTER:
            break

        print("\033c", end="")
    
    return index