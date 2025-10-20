import json
import clingo


def main():
    # Get our input data
    input_data = take_input()

    # Define a Clingo control object
    ctl = clingo.Control()

    # Add structure of days
    ctl.add("base", [], """
    days("Monday",  "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday")
    """)

    # Add person-day relations
    for person, days in input_data.items():
        for i, day in enumerate(days, start=1):
            # Encode each fact
            ctl.add("base", [], f"ranks_day({person},{i},{day}).")

    ctl.add("base", [], """
    // actual code
    """)

    # Ground the logic (prepare it for solving)
    ctl.ground([("base", [])])
    ctl.solve(on_model=on_model)

# Solve and print each model
def on_model(model):
    print("Answer:", model.symbols(shown=True))


def take_input() -> list:
    json_file = open('input.json', 'r')
    schedule = json.load(json_file)
    return schedule

if __name__ == '__main__':
    main()