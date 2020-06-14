#!/usr/bin/env python
from Door import Door
import logging


def main():
    # Call getLogger with no args to set up the handler
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    fh = logging.FileHandler('/home/pi/doorLog.log', mode='a')
    fh.setLevel = logging.DEBUG
    formatter = logging.Formatter('%(asctime)s:%(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)

    door = Door(19. 26, 16, 20)
    try:
        result = door.openDoor()
        logger.info(result)
    except KeyboardInterrupt, e:
        pass
    finally:
        # logging.info(result)
        door.cleanup()
    return


if __name__ == '__main__':
    main()
