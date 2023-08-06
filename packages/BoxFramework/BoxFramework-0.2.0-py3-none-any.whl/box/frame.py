import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("out.log"),
        logging.StreamHandler()
    ]
)
class Numbers:
    def addone(num: int): # Base function  
        """Adds 1 to a given number

        Args:
            num (int): Enter a int to add 1 to get a sum

        Returns:
            int: The sum of given num plus 1
        """
        try:
            return num + 1
        except TypeError:
            logging.error(f"The given value wasn't a int when asked for a int.")

    def minusone(num: int):
        """Subtracts 1 to a given number

        Args:
            num (int): Enter a int to subtract 1 to get a total

        Returns:
            int: The total of given num minus 1
        """
        try:
            return num - 1
        except TypeError:
            logging.error(f"The given value wasn't a int when asked for a int.")
