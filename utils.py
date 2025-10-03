import readchar

def select_category(categories) -> int:
    index = 0

    print("Kategorie mit Pfeiltasten auswählen und Enter drücken:")
    while True:
        for i, cat in enumerate(categories):
            prefix = "-> " if i == index else "  "
            print(f"{prefix}{cat}")
        key = readchar.readkey()
        if key == readchar.key.UP:
            index = (index - 1) % len(categories)
        elif key == readchar.key.DOWN:
            index = (index + 1) % len(categories)
        elif key == readchar.key.ENTER:
            break

        print("\033c", end="")
    
    return index