import json
import clingo
import logging

class Scheduler:
    _input_data: dict

    def __init__(self):
        pass

    def run(self) -> dict:
        # Configure logging (Options: DEBUG, INFO, WARNING, ERROR, CRITICAL)
        logging.basicConfig(level=logging.INFO)  # Minimum level to show

        # map of names to ids
        id_name = {f"p{i+1}" : name for i, name in enumerate(self._input_data)}

        # Define a Clingo control object
        ctl = clingo.Control()

        # Add all of our input and logic to clingo
        self._prepare_ctl(ctl, id_name)

        # Ground the logic (prepare it for solving)
        ctl.ground([("base", [])])

        # Get the raw answer sets from ctl
        raw_outputs = self._get_raw_outputs(ctl)

        # Get the formatted version, and only the best answer set, along with the sum
        person_to_day, ranking_sum = self._get_format_outputs(raw_outputs, id_name)

        logging.info(f"Assigned schedule: {person_to_day}")
        logging.info(f"Sum of rankings (lower is better): {ranking_sum}")
        return person_to_day

    def _get_raw_outputs(self, ctl) -> list:
        """
        Gets the solutions for a Clingo Control Object
        Must be already grounded
        :param ctl: Clingo Control Object
        :return: List of outputs
        """
        outputs = [] # List to return
        with ctl.solve(yield_=True) as handle:
            # For every answer set
            for model in handle:
                # Log output and append to our list
                logging.info(model.symbols(shown=True))
                outputs.append([str(atom) for atom in model.symbols(shown=True)])

        return outputs

    def _get_format_outputs(self, raw_outputs: list, id_name: dict) -> tuple[dict,int]:
        """
        Gets a formatted version of the output
        Only returns the best option (last one) and the sum of the rankings
        :param raw_outputs: List of answer sets
        :param id_name: Dictionary mapping ids (internally used) to names
        :return: Dictionary of Name to Day mappings (the schedule), and sum of rankings
        """
        person_to_day = {}
        ranking_sum = 0
        for atom in raw_outputs[-1]:
            if "total_sum" in atom:
                ranking_sum = int(atom[len("total_sum("):-1])
                continue
            content = atom[len("assigned("):-1]
            pid, day = content.split(",")
            person_to_day[id_name[pid]] = day
        return person_to_day, ranking_sum

    def _prepare_ctl(self, ctl, id_name) -> None:
        """
        Prepares the Clingo Control Object with our input data
        :param ctl: Clingo Control Object to prepare
        :param id_name: Dictionary mapping ids (internally used) to names
        :param input_data: Dictionary of input data (from json file)
        :return: Nothing
        """
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
            for i, day in enumerate(self._input_data[f"{(id_name.get(person_key))}"], start=1):
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

    def load_file(self) -> None:
        """
        Opens and reads the input json file
        :return: Nothing
        """
        json_file = open('input.json', 'r')
        self._input_data = json.load(json_file)

    def load_dict(self, dict:dict) -> None:
        """
        Loads input data from a dict
        :param dict: Dictionary of input data
        :return: Nothing
        """
        self._input_data = dict

if __name__ == '__main__':
    scheduler = Scheduler()
    scheduler.load_file()
    scheduler.run()
