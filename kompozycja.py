class Engine:
    def start(self):
        return "Silnik uruchomiony"

    def stop(self):
        return "Silnik zatrzymany"


class Wheels:
    def rotate(self):
        return "Koła się obracają"


class Car:
    def __init__(self):
        self.engine = Engine()
        self.wheels = Wheels()

    def start(self):
        engine_status = self.engine.start()
        wheels_status = self.wheels.rotate()
        return f"{engine_status}, {wheels_status}"

    def stop(self):
        return self.engine.stop()


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
