from typing import Dict


class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self, training_type,
                 duration,
                 distance,
                 speed,
                 calories):  # здесь выполняю "Свойства класса InfoMessage"
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        return (f'Тип тренировки: {self.training_type}; '
                f'Длительность: {self.duration:.3f} ч.; '
                f'Дистанция: {self.distance:.3f} км; '
                f'Ср. скорость: {self.speed:.3f} км/ч; '
                f'Потрачено ккал: {self.calories:.3f}.')
# здесь выполняю "у класса InfoMessage должен быть
# метод get_message(), который возвращает сообщение"


class Training:
    """Базовый класс тренировки."""

    MIN_IN_HOUR = 60
    LEN_STEP = 0.65
    M_IN_KM = 1000

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight
        self.training_type = 'Training'

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM
#  Т.к. метод get_distance не принимает внешних данных,
#  то мы используем внутреннее св-во класса
# Пример: внешние данные принимает функция __init__,
# в классе list - функция append

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        return NotImplementedError

    def show_training_info(self) -> InfoMessage:

        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.training_type,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
# выполняю "вынести все неименованные значения
# в константы на уровне класса"

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        super().__init__(action, duration, weight)
        self.training_type = 'Running'  # "нужно добавить атрибуты класса"

    def get_spent_calories(self) -> float:
        return ((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 + self.CALORIES_MEAN_SPEED_SHIFT)
                * self.weight / self.M_IN_KM
                * (self.duration * self.MIN_IN_HOUR))


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    KMpH_IN_MPpS = 0.278
    WEIGHT_MULTIPLIER = 0.035
    SM_IN_MET = 100
    AVERAGE_SPEED_MULTIPLIER = 0.029

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float,  # "дополнительный параметр height"
                 ) -> None:

        super().__init__(action, duration, weight)
        self.height = height
        self.training_type = 'SportsWalking'

    def get_spent_calories(self) -> float:
        return ((self.WEIGHT_MULTIPLIER * self.weight
                 + ((self.get_mean_speed() * self.KMpH_IN_MPpS)
                    ** 2 / (self.height / self.SM_IN_MET))
                 * self.AVERAGE_SPEED_MULTIPLIER
                 * self.weight) * self.duration * self.MIN_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP = 1.38
    SHIFT_IN_SPEED = 1.1
    SWM_SPEED_MULTIPLIER = 2

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: float,
                 count_pool: int
                 ) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.training_type = 'Swimming'

    def get_mean_speed(self) -> float:  # Со 107 по 114 - копипаст из Running
        return (self.length_pool
                * self.count_pool
                / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed()
                + self.SHIFT_IN_SPEED)
                * self.SWM_SPEED_MULTIPLIER
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    trainings: Dict[str, Training] = {'SWM': Swimming,
                                      'RUN': Running,
                                      'WLK': SportsWalking}
    return trainings[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
