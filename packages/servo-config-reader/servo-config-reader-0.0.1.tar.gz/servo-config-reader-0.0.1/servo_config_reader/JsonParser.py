import json
from typing import List, Dict

from servo_config_reader.Models.Joint import Joint
from servo_config_reader.Models.Motor import Motor


class JsonParser:

    @staticmethod
    def _ReadConfig(path: str):
        # TODO check path exist
        f = open(f'{path}')
        data = json.load(f)
        f.close()

        return data

    @staticmethod
    def _ParseConfig(path: str) -> List[Motor]:
        config = JsonParser._ReadConfig(f'{path}')
        motors = []
        for element in config:
            motors.append(Motor(name=element['name'],
                                joint=Joint(element['joint']['lover_limit'],
                                            element['joint']['upper_limit'],
                                            element['joint']['speed'],
                                            element['joint']['id'])))
        return motors

    @staticmethod
    def GetParam(path: str) -> Dict[str, Motor]:
        motors = JsonParser._ParseConfig(f'{path}')
        name2Motor = {}

        for motor in motors:
            name2Motor[motor.name] = motor

        return name2Motor
