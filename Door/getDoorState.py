#!/usr/bin/env python
from Door import Door


def main():
    door = Door(19, 26, 16, 20)

    try:
        doorStatus = door.getDoorStatus()
        print doorStatus
    except KeyboardInterrupt, e:
        pass
    finally:
        door.cleanup()
    return


if __name__ == '__main__':
    main()
