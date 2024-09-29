import time
import logging
import cProfile
import pstats

class Tracker:
    def __init__(self):
        # Initialize dictionaries to store start and end times
        self.start_times = {}
        self.end_times = {}
        
        # Set up logging
        self.logger = logging.getLogger('Tracker')
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
        
        # Initialize the profiler
        self.profiler = cProfile.Profile()

    def start(self, name):
        # Record the start time for a given name
        self.start_times[name] = time.time()
        self.logger.debug(f"Started tracking {name}")
        self.profiler.enable()  # Enable the profiler

    def stop(self, name):
        # Record the end time for a given name and log the elapsed time
        self.end_times[name] = time.time()
        elapsed_time = self.end_times[name] - self.start_times[name]
        self.logger.debug(f"Stopped tracking {name}. Time taken: {elapsed_time:.4f} seconds")
        self.profiler.disable()  # Disable the profiler

    def report(self):
        # Report the elapsed time for all tracked names
        for name in self.start_times:
            if name in self.end_times:
                elapsed_time = self.end_times[name] - self.start_times[name]
                self.logger.info(f"{name}: {elapsed_time:.4f} seconds")
            else:
                self.logger.warning(f"{name} has not been stopped")
        
        # Create a Stats object and print the profiling results
        stats = pstats.Stats(self.profiler)
        stats.sort_stats('cumulative').print_stats(10)