import datetime

class printing():

    def print(image):

        now = datetime.datetime.now()

        withSecond = now.strftime("%Y-%m-%d_%H-%M-%S")
        withmilisecond = now.strftime("%Y-%m-%d_%H-%M-%S-%f")

        