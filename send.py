import paho.mqtt.client as mqtt

# Create a MQTT client and register a callback for connect events
client = mqtt.Client()
# Connect to a broker
client.connect("broker.hivemq.com", port=1883, keepalive=60)
# Start a background loop that handles all broker communicationU
client.loop_start()

alphabet = "abcdefghijklmnopqrstuvwxyzåäö"
new_username = 0
encryption_number_ = 0
run_once = 0

def username():
    print("Username: ", end="")
    new_username = input()
    if len(new_username) > 0:
        return new_username
    else:
        raise ValueError

def encryption_number():
    print("Choose your encryption(0-28): ", end="")
    encryption_number_ = int(input())
    if encryption_number_ > 0 and encryption_number_ < 29:
        return encryption_number_
    else:
        raise ValueError

def encrypt(text):
    
    # The function receives a string as input, and encrypts it using the Rot-13 method
    
    # Transform the string to lower-case chars
    text = text.lower()
    
    # the encrypted message
    result = ''
    
    # Replace each letter in the string with a letter which is N positions further
    for char in text:
        if char.isalpha():
             result += alphabet[(alphabet.index(char) + shift) % 29]
        else:
            result += char
    return(result)

while True:
    if run_once == 0:
        while True:
            try:
                user = username()
                break
            except ValueError:
                print("No username!")

        while True:
            try:
                shift = encryption_number()
                break
            except ValueError:
                print("Wrong encryption!")

            run_once = 1

    print("Message: ", end="")
    message = input()
    if len(message) == 0:
        break

    encrypted_message = encrypt(message)
    print(encrypted_message)
    
    # Send the message
    msg = client.publish(f"ela/superchat/{user}", payload=encrypted_message, qos=1)
    # If python exits immediately it does not have the time to send
    # the message
    msg.wait_for_publish()
client.disconnect()
