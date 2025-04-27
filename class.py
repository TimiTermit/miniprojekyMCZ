class Car:
    def __init__(self):
        self.engine_status = "Zatrzymany"
        self.wheels_status = "Nie obracają się"

    def start(self):
        self.engine_status = "Uruchomiony"
        self.wheels_status = "Obracają się"
        return f"Silnik {self.engine_status}, Koła {self.wheels_status}"

    def stop(self):
        self.engine_status = "Zatrzymany"
        self.wheels_status = "Nie obracają się"
        return f"Silnik {self.engine_status}"


class Driver:
    def drive(self, car):
        print(car.start())
        print("Jedziemy!")
        print(car.stop())


# Główna część programu
if __name__ == "__main__":
    my_car = Car()
    driver = Driver()
    driver.drive(my_car)

    # Dodatkowe operacje
    for _ in range(5):
        print("Zmieniam bieg...")
    print("Zatrzymujemy się na światłach.")