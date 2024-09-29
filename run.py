import sys
from app import create_app

def main(profile=True):
    # Create the Flask app
    app = create_app()
    
    if profile:
        import cProfile
        import pstats
        
        # Create a profiler object
        profiler = cProfile.Profile()
        
        # Enable the profiler
        profiler.enable()
        
        # Run the Flask app
        app.run(debug=True)
        
        # Disable the profiler
        profiler.disable()
        
        # Create a Stats object
        stats = pstats.Stats(profiler)
        
        # Sort the statistics by cumulative time and print the top 10 functions
        stats.sort_stats('cumulative').print_stats(10)
    else:
        # Run the Flask app without profiling
        app.run(debug=True)

if __name__ == '__main__':
    # Check if the script should run with profiling enabled
    profile = '--no-profile' not in sys.argv
    main(profile)
