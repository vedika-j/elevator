import tkinter as tk
import random


class ElevatorSimulation:
    def __init__(self, floors, elevators_count=5):
        self.floors = floors
        self.elevators_count = elevators_count
        self.elevators = [random.randint(0, floors) for _ in range(elevators_count)]
        self.positions = [self.elevators.copy()]  # Store initial positions
        self.current_position_index = 0

    def move_elevator(self, elevator_index, target_floor):
        current_floor = self.elevators[elevator_index]
        while current_floor != target_floor:
            direction = 1 if target_floor > current_floor else -1
            current_floor += direction
            self.elevators[elevator_index] = current_floor
            self.positions.append(self.elevators.copy())  # Save each position step

    def handle_calls(self, calls):
        for call in calls:
            distances = [(abs(elevator - call), i) for i, elevator in enumerate(self.elevators)]
            distances.sort()  # Find the closest elevator
            nearest_elevator = distances[0][1]
            self.move_elevator(nearest_elevator, call)


class ElevatorApp:
    def __init__(self, root, simulation):
        self.simulation = simulation

        # Create two windows
        self.main_window = root
        self.main_window.title("Elevator Simulation Controls")
        self.output_window = tk.Toplevel(root)
        self.output_window.title("Elevator Positions")

        # Setup output canvas
        self.canvas = tk.Canvas(self.output_window, width=400, height=600, bg="white")
        self.canvas.pack()
        self.label = tk.Label(self.output_window, text="Initial Elevator Positions", font=("Arial", 14))
        self.label.pack()

        # Setup control buttons
        self.forward_button = tk.Button(
            self.main_window, text="Next", command=self.next_position, state="disabled", font=("Arial", 12)
        )
        self.forward_button.pack(side=tk.LEFT, padx=20)
        self.backward_button = tk.Button(
            self.main_window, text="Previous", command=self.previous_position, state="disabled", font=("Arial", 12)
        )
        self.backward_button.pack(side=tk.LEFT, padx=20)

        # Draw initial positions
        self.draw_position()

    def draw_position(self):
        """
        Draw the current position of the elevators on the canvas.
        """
        self.canvas.delete("all")  # Clear the canvas for updates

        # Draw floors
        for floor in range(self.simulation.floors + 1):
            y = 550 - (floor * 50)
            self.canvas.create_line(50, y, 350, y, fill="black")
            self.canvas.create_text(30, y, text=f"{floor}", font=("Arial", 12))

        # Draw elevators at their current positions
        current_positions = self.simulation.positions[self.simulation.current_position_index]
        for i, position in enumerate(current_positions):
            x = 70 + (i * 60)
            y = 550 - (position * 50)
            self.canvas.create_rectangle(x, y, x + 40, y - 40, fill="blue", outline="black", width=3)
            self.canvas.create_text(x + 20, y - 50, text=f"{position}", font=("Arial", 12), fill="black")

        # Update label
        if self.simulation.current_position_index == 0:
            self.label.config(text="Initial Elevator Positions")
        else:
            self.label.config(
                text=f"Position {self.simulation.current_position_index + 1} of {len(self.simulation.positions)}"
            )

    def next_position(self):
        """
        Move to the next position in the stored simulation.
        """
        if self.simulation.current_position_index < len(self.simulation.positions) - 1:
            self.simulation.current_position_index += 1
            self.draw_position()
        self.update_buttons()

    def previous_position(self):
        """
        Move to the previous position in the stored simulation.
        """
        if self.simulation.current_position_index > 0:
            self.simulation.current_position_index -= 1
            self.draw_position()
        self.update_buttons()

    def update_buttons(self):
        """
        Enable or disable buttons based on the current position index.
        """
        if self.simulation.current_position_index == 0:
            self.backward_button.config(state="disabled")
        else:
            self.backward_button.config(state="normal")

        if self.simulation.current_position_index == len(self.simulation.positions) - 1:
            self.forward_button.config(state="disabled")
        else:
            self.forward_button.config(state="normal")

    def enable_navigation_buttons(self):
        """
        Enable forward navigation once simulation steps are available.
        """
        self.forward_button.config(state="normal")


def main():
    root = tk.Tk()
    floors = int(input("Enter the number of floors in the building (0 to n): "))
    simulation = ElevatorSimulation(floors)

    # Launch the GUI application
    app = ElevatorApp(root, simulation)

    # Show the initial position before proceeding
    root.update()
    input("Press Enter to continue after observing the initial elevator positions...")

    num_calls = int(input("How many floors do you want to call the lift for? "))
    calls = []
    for i in range(num_calls):
        while True:
            call = int(input(f"Enter the floor number for call {i + 1}: "))
            if 0 <= call <= floors:
                calls.append(call)
                break
            else:
                print(f"Invalid floor! Please enter a floor between 0 and {floors}.")

    # Process elevator calls
    simulation.handle_calls(calls)

    # Enable navigation buttons
    app.enable_navigation_buttons()

    root.mainloop()


if __name__ == "__main__":
    main()
