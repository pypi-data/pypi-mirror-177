from marta import TrainLine


def train_line_code_to_line(train_line_code: str) -> TrainLine:
    """
    Convert train line code to TrainLine enum

    :param train_line_code: train line code
    :return: TrainLine enum
    """
    if train_line_code == '1':
        return TrainLine.BLUE
    elif train_line_code == '2':
        return TrainLine.GREEN
    if train_line_code == '3':
        return TrainLine.GOLD
    elif train_line_code == '4':
        return TrainLine.RED
    else:
        raise ValueError(f"Invalid train line code: {train_line_code}")


