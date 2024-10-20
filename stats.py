class Statistics:
    def __init__(self):
        self.time_played = 0
        self.kills = 0
        self.shields_used = 0
        self.powerup_count = 0 
        self.shots_fired = 0
    def update(self, *args, **kwargs):
        # Handle positional arguments
        for arg in args:
            if isinstance(arg, dict):
                # If the argument is a dictionary, update multiple stats
                for key, value in arg.items():
                    self._update_stat(key, value)
            elif hasattr(self, arg):
                # If it's a string matching an attribute, increment by 1
                self._update_stat(arg, 1)
            else:
                print(f"Warning: '{arg}' is not a valid stat attribute.")

        # Handle keyword arguments
        for key, value in kwargs.items():
            self._update_stat(key, value)

    def _update_stat(self, key, value):
        if hasattr(self, key):
            current_value = getattr(self, key)
            setattr(self, key, current_value + value)
        else:
            print(f"Warning: '{key}' is not a valid stat attribute.")