class RecursiveDescentParser:
    def __init__(self):
        self.grammar = {}            
        self.non_terminals = []      
        self.stack = []              
        self.input_string = []       
        self.accepted = False        

    def input_grammar(self):
        print("\n--- Define Your Grammar ---")
        self.grammar.clear()
        self.non_terminals = []

        num_non_terminals = int(input("Enter the number of non-terminals: ").strip())

        for i in range(num_non_terminals):
            non_terminal = input(f"Enter non-terminal {i + 1}: ").strip()
            self.non_terminals.append(non_terminal)
            
            rules = []
            print(f"Define rules for '{non_terminal}' (type 'end' to finish):")
            while True:
                rule = input(">> ").strip()
                if rule.lower() == 'end':
                    break
                rules.append(rule)
            
            self.grammar[non_terminal] = rules

    def is_simple_grammar(self):
        """
        Checks if the grammar is simple.
        A simple grammar ensures that no rule starts with a non-terminal.
        """
        for non_terminal, rules in self.grammar.items():
            for rule in rules:
                if rule.startswith(tuple(self.non_terminals)):
                    return False
        return True

    def parse(self, current, position):
        if position == len(self.input_string) and current == "":
            return True
        
        if current == "" or position == len(self.input_string):
            return False

        next_symbol = current[0]

        if next_symbol in self.grammar:
            for rule in self.grammar[next_symbol]:
                if self.parse(rule + current[1:], position):
                    self.stack.append((next_symbol, rule))
                    return True

        elif position < len(self.input_string) and next_symbol == self.input_string[position]:
            return self.parse(current[1:], position + 1)

        return False

    def check_string(self, input_str):
        self.input_string = list(input_str)  # Convert string to list of characters
        self.stack.clear()
        self.accepted = self.parse(self.non_terminals[0], 0)  # Start from the first non-terminal
        return self.accepted

    def print_tree(self):
        print("\n--- Derivation Tree ---")
        for non_terminal, rule in reversed(self.stack):
            print(f"{non_terminal} -> {rule}")
        print()

    def menu(self):
        while True:
            print("\n===== MENU =====")
            print("1. Input New Grammar")
            print("2. Check a String")
            print("3. Exit")
            choice = input("Select an option (1/2/3): ").strip()

            if choice == '1':
                self.input_grammar()
                if self.is_simple_grammar():
                    print("\n The grammar is simple.")
                else:
                    print("\n The grammar is not simple. Please redefine it carefully.")
                    continue

            elif choice == '2':
                input_str = input("Enter the string to be checked: ").strip()
                print(f"Input String: {list(input_str)}")
                if self.check_string(input_str):
                    print("\n The input string is accepted.")
                    self.print_tree()
                else:
                    print("\n The input string is rejected.")

            elif choice == '3':
                print("Exiting the parser. Goodbye!")
                break

            else:
                print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    print("Welcome to the Recursive Descent Parser!")
    parser = RecursiveDescentParser()
    parser.input_grammar()

    while not parser.is_simple_grammar():
        print("\n The grammar is not simple. Please redefine it.")
        parser.input_grammar()

    print("\n The grammar is simple. You may now check strings.\n")
    parser.menu()
