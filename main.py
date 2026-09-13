import controller
from cli import choose_file, choose_parameter_set, select_runs

def main() -> None:
    while True:
        print("\n==============================")
        print("Job Shop Scheduling Problem")
        print("==============================")

        
        selected_file = choose_file()
        parameters = choose_parameter_set()
        runs = select_runs()

        controller.controller(
            filepath=selected_file,
            parameters=parameters,
            runs = runs
        )

if __name__ == "__main__":
    main()