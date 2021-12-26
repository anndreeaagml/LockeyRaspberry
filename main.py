from RPi import GPIO
import requests
import time
import uuid
import re 


API_URL = 'https://lockeysuperserverdeluxe.azurewebsites.net/Sensor'
MAC_ADDRESS = ':'.join(re.findall('..', '%012x' % uuid.getnode()))
DELAY = 0.1  # seconds


def get_input() -> None:
    return GPIO.input(4)


def send_api_message(locked: bool) -> None:
    global API_URL, MAC_ADDRESS

    data = {
        "ID": MAC_ADDRESS,
        "IsLocked": locked
    }

    response = requests.post(API_URL, data=data)
    print(response)
    print("Unocked" if not locked else 'Locked')


def main() -> None:
    global API_URL, DELAY

    response = requests.get(API_URL)
    print(response._content.decode("utf-8"))

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.IN)

    prev_input = get_input()

    if prev_input == 0:
        send_api_message(locked=False)
    else:
        send_api_message(locked=True)

    time.sleep(DELAY)

    try:
        while True:
            # take a reading
            input = get_input()
            print(input)

            # if the last reading was low and this one high, alert us
            if prev_input < input:
                send_api_message(locked=True)

            if prev_input > input:
                send_api_message(locked=False)

            # update previous input
            prev_input = input

            # slight pause
            time.sleep(DELAY)

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == '__main__':
    main()
