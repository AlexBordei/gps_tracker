import serial
import pynmea2
import sys
import http.client



def port_setup(port):
    print(sys.argv)
    ser = serial.Serial(port, baudrate=int(sys.argv[1]), timeout=2)
    return ser

def parseGPSdata(ser):
    keywords = ["$GPRMC", "$GPGGA"]
    gps_data = ser.readline()
    gps_data = gps_data.decode("utf-8")  # transform data into plain string
    # parsing via manually

    if len(gps_data) > 5:  # Check to see if the GPS gave any useful data
        if gps_data[0:6] in keywords:  # Check t see if the message code
            gps_msg = pynmea2.parse(gps_data)
            lat = gps_msg.latitude
            lng = gps_msg.longitude
            return (lat, lng)
        else:
            return None
    else:
        return None

if __name__ == '__main__':
    # access serial port
    gps_port = "/dev/serial0"
    ser = port_setup(gps_port)

    # Print out GPS cordinates
    print("GPS coordinate Stream:")
    conn = http.client.HTTPSConnection("alexbordei.dev")

    headers = {
        'Content-Type': "application/json",
        'Authorization': "Basic QWxleCBCb3JkZWk6TU9rUDRtZ0RUNU1LcEZROXhmTmRyRG4w"
    }

    while True:
        try:
            gps_coords = parseGPSdata(ser)
            if gps_coords is not None:  # if no valid data was received
                if gps_coords[0] > 0 and gps_coords[1] > 0:
                    print(f"latitude: {gps_coords[0]}, longitude: {gps_coords[1]}")

                    payload = "{\n\t\t\"acf\": {\n\t\t\"lat\": \"" + str(gps_coords[0]) + "\",\n\t\t\"lng\": \"" + str(gps_coords[1]) + "\"\n\t}\n}"
                    try:
                        conn.request("POST", "/wp-json/wp/v2/location/671", payload, headers)
                        res = conn.getresponse()
                        data = res.read()
                        print('location sent')
                    except:
                        print('there was an error sending the data')


        except serial.SerialException as e:  # catch any serial communication errors
            print(f"\nERROR: {e}")
            print("... reconnecting to serial\n")
            ser = port_setup()

        except KeyboardInterrupt as e:  # Catch when user hits Ctrl-C and end program
            print("--- Program shutting down ---")
            break
