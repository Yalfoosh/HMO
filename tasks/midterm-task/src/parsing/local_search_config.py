class LocalSearchConfig:
    def __init__(self, args):
        self.instance_path = args.instance_path
        self.solution_path = args.solution_path
        self.dump_path = args.dump_path
        self.solution_dump_path = args.solution_dump_path

        self.price_budget = args.price_budget
        self.max_players_in_main_team = args.max_players_in_main_team
        self.max_players_per_club = args.max_players_per_club
        self.position_budget = {
            "GK": args.gk_count,
            "DEF": args.def_count,
            "MID": args.mid_count,
            "FW": args.fw_count,
        }
        self.main_team_ranges = {
            "GK": args.gk_range,
            "DEF": args.def_range,
            "MID": args.mid_range,
            "FW": args.fw_range,
        }

        self.verbosity = args.verbosity

        # Adjust main_team_ranges to be full pairs.
        for key, value in self.main_team_ranges.items():
            if value is None:
                value = (0, self.position_budget[key])
            elif len(value) == 1:
                value = (
                    0 if value[0] is None else value[0],
                    self.position_budget[key],
                )

            self.main_team_ranges[key] = value
