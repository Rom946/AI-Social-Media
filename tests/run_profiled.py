import cProfile
import pstats
from app import create_app

def main():
    # Create the Flask app
    app = create_app()
    
    # Run the Flask app
    app.run(debug=True)

def process_profiling_data(profiler):
    # Create a Stats object
    stats = pstats.Stats(profiler)
    
    # Sort the statistics by cumulative time
    stats.sort_stats('cumulative')
    
    # Extract the top 10 functions by cumulative time
    top_stats = stats.stats.items()
    top_stats = sorted(top_stats, key=lambda x: x[1][3], reverse=True)[:10]
    
    # Classify and format the profiling data
    classified_data = {
        "Module Loading": [],
        "Built-in Execution": [],
        "Script Execution": [],
        "Text Generation Initialization": [],
        "Pipeline Initialization": [],
        "Model Loading": []
    }
    
    for func, (cc, nc, tt, ct, callers) in top_stats:
        func_name = f"{func[0]}:{func[1]}({func[2]})"
        entry = {
            "Function": func_name,
            "Calls": f"{cc}/{nc}",
            "Total Time": f"{tt:.3f}s",
            "Cumulative Time": f"{ct:.3f}s"
        }
        
        if "importlib" in func_name:
            classified_data["Module Loading"].append(entry)
        elif "builtins.exec" in func_name:
            classified_data["Built-in Execution"].append(entry)
        elif "routes.py" in func_name:
            classified_data["Script Execution"].append(entry)
        elif "text_generation.py" in func_name:
            classified_data["Text Generation Initialization"].append(entry)
        elif "pipelines/__init__.py" in func_name:
            classified_data["Pipeline Initialization"].append(entry)
        elif "pipelines/base.py" in func_name:
            classified_data["Model Loading"].append(entry)
    
    return classified_data

def log_classified_data(classified_data):
    for category, entries in classified_data.items():
        print(f"\n{category}:")
        for entry in entries:
            print(f"  Function: {entry['Function']}")
            print(f"    Calls: {entry['Calls']}")
            print(f"    Total Time: {entry['Total Time']}")
            print(f"    Cumulative Time: {entry['Cumulative Time']}")

if __name__ == '__main__':
    # Enable the profiler
    profiler = cProfile.Profile()
    profiler.enable()
    
    # Run the main function
    main()
    
    # Disable the profiler
    profiler.disable()
    
    # Process and log the profiling data
    classified_data = process_profiling_data(profiler)
    log_classified_data(classified_data)