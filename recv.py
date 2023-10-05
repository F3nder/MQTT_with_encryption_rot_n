import paho.mqtt.client as mqtt

alphabet = "abcdefghijklmnopqrstuvwxyzåäö"
run_once = 0

def encryption_number():
    print("Choose your encryption(0-28): ", end="")
    encryption_number_ = int(input())
    if encryption_number_ > 0 and encryption_number_ < 29:
        return encryption_number_
    else:
        raise ValueError
    
def decrypt(text):
      # Transform the string to lower-case chars
    text = text.lower()
    # the decrypted message
    result = ''
    # Replace each letter in the string with a letter which is 13 positions backwards
    for char in text:
        if char.isalpha():
            # the new position
            position = alphabet.index(char) - shift
            if position < 0:
                result += alphabet[29 + position]
            else:
                result += alphabet[position]
        else:
            result += char
    return result

# The callback for when the client connects to the server
def on_connect(client, userdata, flags, rc):
    # Subscribing in on_connect() means that
    # reconnect will renew then subscriptions
    client.subscribe("ela/superchat/#", qos=1)


# The callback for receiving message
def on_message(client, userdata, msg):
    message_str = msg.payload.decode("utf-8")
    decrypted_msg = decrypt(message_str)
    print(f"message: {decrypted_msg}")


# Create a MQTT client with callbacks
client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("broker.hivemq.com", port=1883, keepalive=60)
# Blocking call that processes network traffic, dispatches
# callbacks and handles reconnecting.
if run_once == 0:
    while True:
        try:
            shift = encryption_number()
            break
        except ValueError:
            print("Wrong encryption!")
        run_once = 1

client.loop_forever()