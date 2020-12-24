#!/usr/bin/python3

import os
import sys
import time
import datetime





def main():

    last_time_something_playing = datetime.datetime.now()
    print()
    first_device_found = False
    services_found = False
    devices_arr = []
    mac_address_arr = []
    blacklisted_devices = []
    time_threshold = 30
    need_to_disconnect = False

    bluetooth_data_gathered = False
   
    #Recover data from the saved file
    lines = open("devices_storage.txt", "r").readlines()
    for l in lines:
        l = l.replace('\n', '')
        blacklisted_devices.append(l)


    while True:
        
        okay = True
        print("Menu\n")
        print("1. Gather data and show")
        print("2. Show previously paired devices ")
        print("3. Devices added to the list")
        print("4. Add device to the list")
        print("5. Launch the service")
        print("6. Clean screen")
        print("7. Test")
        print("0. Exit")
        
        input_sel = input("Select one option: ")
        os.system('clear')

        try:

            input_sel = int(input_sel)

        except:
            okay = False
            print("\n\033[1;31mInvalid selection, not number\033[0m\n\n")

        
        

        if okay:
            if input_sel == 1 :
                print("\n\n\033[0;32mGathering data\033[0m")
                time.sleep(1.0)

                # Reading command line
                stream = os.popen("system_profiler SPBluetoothDataType")
                bluetooth_devices = stream.read()
                splited_bluetooth_devices = bluetooth_devices.splitlines(True)

                for line in splited_bluetooth_devices:
                    aux_split = line.split()
                    if str(line).find("Devices") != -1:
                        first_device_found = True

                    if str(line).find("Services:\n") != -1:
                        services_found = True

                    if first_device_found and not services_found :
                        #print(line)
                        if str(line).find(":\n") != -1:
                            devices_arr.append(line)
                        if str(line).find("Address:") != -1:
                            mac_address_arr.append(line)

                devices_arr.pop(0)
                i = 1
                for element in devices_arr:
                    mac_address_arr[i-1] = str(mac_address_arr[i-1]).replace("Address: ", '')
                    mac_address_arr[i-1] = str(mac_address_arr[i-1]).replace('    ','')
                    element = str(element).translate({ord(':'): None})
                    element = str(element).replace('\n','')
                    element = str(element).replace('    ','')
                    devices_arr[i-1] = element
                    print(" " + str(i) + "." + element)
                    print(str(mac_address_arr[i-1]))
                    i += 1

                
                bluetooth_data_gathered = True
                time.sleep(1.0)

            elif input_sel == 2 :
                print("\n\n\033[0;32mShowing devices previously paired\033[0m\n")
                if bluetooth_data_gathered:
                    i = 1
                    for element in devices_arr:
                        print(str(i) + ". " + element)
                        i += 1

                else:
                    print("\t\033[1;31mData not gathered yet, gather data first(option 1)\033[0m\n\n\n")

            elif input_sel == 3 :
                print("\n\n\033[0;32mShowing devices that are in the list\033[0m")
                if blacklisted_devices != []:
                    i = 1
                    for element in blacklisted_devices:
                        print(str(i) + ". " + element)
                        i += 1
                elif blacklisted_devices == []:
                    print("\tNothing here yet\n\n\n")
                else:
                    print("Error retrieving the data\n\n\n")

            elif input_sel == 4 :
                if bluetooth_data_gathered:
                    print("Select device of the list to add")
                    i = 1
                    for element in devices_arr:
                        print(str(i) + ". " + element)
                        i += 1
                    entrada_incorrecta = True
                    input_is_number = True
                    while entrada_incorrecta:
                        input_sel_device = input("Select a device: ")
                        try:

                            input_sel_device = int(input_sel_device)

                        except:
                            input_is_number = False
                            print("\n\033[1;31mInvalid selection, not number\033[0m\n\n")

                        if input_is_number:
                            if input_sel_device > 0 and input_sel_device < len(devices_arr) + 1:
                                blacklisted_devices.append(mac_address_arr[input_sel_device - 1])
                                entrada_incorrecta = False

                                # Write the devices mac addreses in the output
                                outF = open("devices_storage.txt", "w")
                                outF.writelines(blacklisted_devices)
                                outF.close()
                            else:
                                print("\t\033[1;31mThe device you have selected is not in the list\033[0m")

                else:
                    print("\nData not gathered yet, gather data first(option 1)\n\n\n")

                
            elif input_sel == 5 :
                print("Service started")
                while True:
                    # Check if there's audio playing
                    stream = os.popen("./check_audio_playing.sh")
                    audio_playing_string = stream.read()
                    
                    if str(audio_playing_string).find("not_playing") != -1:
                        #print("Nothing is playing")
                        time_difference = datetime.datetime.now() - last_time_something_playing
                        time_difference = time_difference.total_seconds()
                        
                        #print(int(time_difference))
                        
                        if(int(time_difference) > time_threshold*60) and (need_to_disconnect or int(time_difference)%300 == 0 ):
                            print("Disconnecting devices")
                            for device in blacklisted_devices:
                                command = 'BluetoothConnector --disconnect ' + str(device)
                                os.system(command)
                            
                            need_to_disconnect = False


                    elif str(audio_playing_string).find("playing") != -1:
                        # print("Something is playing")
                        last_time_something_playing = datetime.datetime.now()
                        need_to_disconnect = True

                    else: 
                        print("Something went wrong")
                        print("Finishing this script")
                        sys.exit()
                    
                    time.sleep(1)

            elif input_sel == 0 :
                print("Exiting")
                sys.exit()

            elif input_sel == 6 :
                os.system('clear')

            elif input_sel == 7:
                data_file = open("devices_storage.txt", "r")
                data = data_file.read()
                all_lines = "pollas"
                outF = open("devices_storage.txt", "w")
                outF.writelines(all_lines)
                outF.close()
                print(str(data))
                print("\n\n\n")

            else:
                print("\n\n\033[1;31mInvalid selection, number not in selection menu\033[0m\n\n")





if __name__ == "__main__":
    main()