import os

if __name__ == "__main__":
    print("Starting full project execution pipeline...")
    
    scripts = [
        "src/data_preparation.py",
        "src/analysis_script.py",
        "src/trader_clustering.py"
    ]
    
    for script in scripts:
        print(f"\n--- Running {script} ---")
        exit_code = os.system(f"python {script}")
        if exit_code != 0:
            print(f"Error running {script}. Pipeline stopped.")
            break
            
    print("\nPipeline execution complete. Run 'streamlit run dashboard.py' to view results.")