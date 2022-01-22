import abc

class BaseInput(abc.ABC):
    @abc.abstractmethod
    def get_left_speed(self) -> float:
        ...
    
    @abc.abstractmethod
    def get_right_speed(self) -> float:
        ...

