import json
import clingo
import logging


def main():
    # Configure logging (Options: DEBUG, INFO, WARNING, ERROR, CRITICAL)
    logging.basicConfig(level=logging.INFO)  # Minimum level to show

    # Get our input data
    input_data = take_input()

    # map of names to ids
    id_name = {f"p{i+1}" : name for i, name in enumerate(input_data)}

    # Define a Clingo control object
    ctl = clingo.Control()

    # Add structure of days
    day_fact = "day(sunday; monday; tuesday; wednesday; thursday; ). \n"
    logging.debug(day_fact)
    ctl.add("base", [], day_fact)

    # Add person-day relations
    for person_key in id_name.keys():
        # Add structure of individual persons
        person_fact = f"person({person_key})."
        logging.debug(person_fact)
        ctl.add("base", [], person_fact)

        # For each person, add their rankings of each day
        for i, day in enumerate(input_data[f"{id_name.get(person_key)}"], start=1):
            ranking_fact = f"ranks_day({person_key},{i},{day.lower()})."
            logging.debug(ranking_fact)
            ctl.add("base", [], ranking_fact)


    # A day for every person
    assigned_fact = "1 {assigned(P, D) : day(D) } 1 :- person(P)."
    logging.debug(assigned_fact)
    ctl.add("base", [], assigned_fact)

    # Two occurrences of each day
    unique_day_condition = "2 {assigned(P, D) : person(P)} 2 :- day(D)."
    logging.debug(unique_day_condition)
    ctl.add("base", [], unique_day_condition)

    # Minimize rankings (smaller number, higher ranking)
    ranking_directive = "#minimize { I,P,D : assigned(P,D), ranks_day(P,I,D) }."
    logging.debug(ranking_directive)
    ctl.add("base", [], ranking_directive)

    # Show sum of rankings
    sum_directive = "total_sum(S) :- S = #sum { I,P,D : assigned(P,D), ranks_day(P,I,D) }.\n#show total_sum/1."
    logging.debug(sum_directive)
    ctl.add("base", [], sum_directive)

    # Output format
    show_directive = "#show assigned/2."
    logging.debug(show_directive)
    ctl.add("base", [], show_directive)

    # Ground the logic (prepare it for solving)
    ctl.ground([("base", [])])

    # Show every answer set
    with ctl.solve(yield_=True) as handle:
        for model in handle:
            on_model(model)
    # Show one answer set
    #ctl.solve(on_model=on_model)

# Print model
def on_model(model):
    logging.info(f"Answer:{model.symbols(shown=True)}")


def take_input() -> dict:
    json_file = open('input.json', 'r')
    schedule = json.load(json_file)
    return schedule

if __name__ == '__main__':
    main()