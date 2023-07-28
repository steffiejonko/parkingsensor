# Programmeur: Stef Jonker
# Datum begonnen: 9 Maart 2022
# Datum gestopt: 20 Maart 2022

# Dit programma is gebaseerd op de Ble-beacon-scanner "https://github.com/bowdentheo/BLE-Beacon-Scanner"

# Dit programma scanned voor bluetooth ibeacons. Dit programma simuleert een pakkeer systeem voor een garage.
# Wanneer er een iBeacon is gevonden en de auto verderweg is dan 75 Centimeter, brandt er een groene lamp.
# Wanneer de auto dichterbij dan 75 Centimeter is, brandt er een rode en een witte lamp, deze lampen blijven aan voor 5 minuten
# Indien de auto na de 5 minuten nog steeds op de oprit staat, blijven de rode en witte lampen uit.
# Wanneer de auto weer weg is gaat de groene lamp aan.

# Het programma gebruikt de bluetooth._bluetooth library om te communiceren met de blutooth-chip op de raspberry pi.
# De ScanUtility library word gebruikt om voor een iBeacons te scannen en dan de juiste iBeacon uit de lijst te halen.
# De RPi.GPIO library word gebruikt om de Afstands-sensor aan te sturen op de rpi.

# Dit programma scanned voor iBeacons via de ScanUtility library. Wanneer het programma de iBeacon heeft gevonden met een uuid van:
# "12345678-0000-0000-0000-000000000000", gaat het programma de afstand berekenen tussen het voertuig en de afstands-sensor.
# Als deze afstand groter is dan 75 cm gaat er een groen ledje branden, en er word een variabele (car_near) gezet met de inhoud "False"
# Deze variabele is nodig om te zien of het voertuig gedetecteerd word door de sensor
# Wanneer het voertuig dichter bij is dan 75 cm, dan word er een while loop geactiveerd die zegt dat de rode en groene
# Ledjes moeten gaan branden. De variabele (car_near) word dan op True gezet. Nu weten we dat de auto dichtbij is.
# Na 300 seconden (5 minuten) gaan de rode en witte ledjes uit. Het programma herhaalt zich daarna, deze keer weten we dat de variabele True is
# Door deze variabele weten we dat de auto er nog steeds is. We hoeven dan dus niet nog een keer de lampen aan te doen.
# Als deze variabele False is dan gaan de rode en witte lampen weer voor 5 minuten aan en herhaald het programma zich.

# Hier importeren we de benodigde Libraries ofwel "bibliotheek mappen"
# Deze Mappen zijn de basis van het programma. Meestal zijn deze mappen geimporteerd van een bekende website maar je kan ze ook zelf schrijven.

import time # De time library zorgt ervoor dat we een vertraging "Delay" kunnen implementeren. Deze vertraging is nodig om somige onderdelen
# Niet door elkaar te laten lopen
import RPi.GPIO as GPIO # Deze library is nodig voor het te kunnen besturen van de RPi input/output pinnen
import ScanUtility # Deze Module zorgt ervoor dat we een scan kunnen maken van de iBeacons in de buurt.
import bluetooth._bluetooth as bluez # Deze module is nodig zodat de ScanUtility kan communiceren met de bluetooth-chip

# Hier zetten we de input/output pinnen van de rpi in de BCM mode. dit zorgt ervoor dat we de pinnen kunnen benoemen bij de virtuele rpi pinout
# In plaats van de fysieke pinout van de rpi
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Hier defineren we de input/output pinnen die we willen gebruiken van de rpi
GPIO_TRIGGER = 18 # Dit is pin nummer 18. Deze pin gebruiken we voor de afstand sensor om een signaal te sturen.
GPIO_ECHO = 23 # Dit is pin nummer 23. Deze pin gebruiken we voor de afstand sensor om het gestuurde signaal te ontvangen.
GPIO_GreenLED = 17 # Pin nummer 17 word gebruikt voor de groene LED
GPIO_RedLED = 27 # Pin nummer 27 word gebruikt voor de rode LED
GPIO_YellowLED = 22 # Pin nummer 22 word gebruikt voor de witte LED

# Hier zetten we het nummer van ons bluetooth apparaat.
dev_id = 0
car_still_near = False

# Hier proberen we een variabele "sock" te defineren. Dit variabele heeft de inhoud van "bluez.hci_open_dev(dev_id)" dit zorgt ervoor dat we
# Het eerste bluetooth apparaat gebruiken op onze rpi.
try:
    sock = bluez.hci_open_dev(dev_id)
    #print("\n *** Looking for BLE Beacons ***\n") # Deze lijnen gebruikte ik om te kijken of het programma werkt.
    #print("\n *** CTRL-C to Cancel ***\n")

# Als het try: blok niet werkt, dan wordt het except blok uitgevoerd.
except:
    print("Error accessing bluetooth") # Dit print dat er een error was in het try blokje. Als deze error word gegeven komt dat meestal doordat Python geen
    # Permissie heeft om gebruik te maken van bluetooth.

ScanUtility.hci_enable_le_scan(sock) # De iBeacon scan wordt geactiveerd.


# Hier zetten we de pinnen in input/output modus.
GPIO.setup(GPIO_TRIGGER,GPIO.OUT)  # De trigger pin van de sensor word op GPIO.OUT ("output") gezet omdat deze pin een singaal moet sturen.
GPIO.setup(GPIO_ECHO,GPIO.IN)      # De echo pin van de sensor word op Input gezet omdat deze pin een signaal moet ontvangen.
GPIO.setup(GPIO_GreenLED,GPIO.OUT) # De Groene LED pin word op output gezet omdat deze led een signaal moet krijgen
GPIO.setup(GPIO_RedLED,GPIO.OUT)   # De rode led word op output gezet
GPIO.setup(GPIO_YellowLED,GPIO.OUT) # De witte led word ook op output gezet


# Probeer dit blok
try: # Terwijl waar ("While True") is een loop die voor altijd blijft lopen. Dit zorgt ervoor dat het programma blijft draaien
    while True:
        returnedList = ScanUtility.parse_events(sock, 10)   # Hier verkrijgen we een lijst van de scanutility module. deze lijst bevat waarden over
        # apparaten en bevat apparaten zelf. Deze informatie is verkregen door de scan die we eerder hadden uitgevoerd.
        for item in returnedList: # Deze functie vraagt om een item in de lijst hierboven.
            if (item['uuid'] == "12345678-0000-0000-0000-000000000000"): # Als dit item een uuid van "12345678-0000-0000-0000-000000000000" heeft dan word de volgende code uitgevoerd:
                GPIO.output(GPIO_RedLED, False) # De rode lamp word uit gezet ("GPIO_RedLED, False") dit zorgt ervoor dat als een lamp per ongeluk aan bleef hij nu uit gaat
                GPIO.output(GPIO_GreenLED, True) # De groene lamp word aan gezet omdat de iBeacon(uuid = "12345678-0000-0000-0000-000000000000") is gedetecteerd
                GPIO.output(GPIO_YellowLED, False) # De witte lamp word uit gezet
                GPIO.output(GPIO_TRIGGER, False) # De trigger word uit gezet zodat de afstand mooi schoon opnieuw gemeten kan worden


                time.sleep(0.5) # Hier geven we de afstands-sensor een delay van 0.5 seconden zodat de sensor rustig kan opstarten

                #print("\n *** Ultrasonic Measurement ***\n") # Een lijn voor testen

                # Hier sturen we een signaal van 10 micro seconden via de trigger pin van de sensor
                GPIO.output(GPIO_TRIGGER, True) # De trigger word aan gezet.
                time.sleep(0.00001) # Een delay van 10 micro seconden word uit gevoerd.
                GPIO.output(GPIO_TRIGGER, False) # En de trigger word weer uitgezet.
                start = time.time() # Leg de tijd vast sinds de laatste opdracht.

                while GPIO.input(GPIO_ECHO)==0: # Terwijl er geen signaal word ontvangen op de echo pin
                    start = time.time() # Leg hier de tijd vast in een nieuwe variabele. Dit is nodig om te meten hoelang het duurt voordat een signaal ontvangen word

                while GPIO.input(GPIO_ECHO)==1: # Wanneer er een signaal word ontvangen op de echo pin
                    stop = time.time() # Leg de tijd vast van wanneer het signaal ontvangen werd.

                # Leg de verstreken tijd vast door de stop tijd af te trekken van de start tijd. Op deze manier weten we hoelang het duurde voordat het signaal ontvangen werd
                elapsed = stop - start

                # De veriabele "distancet" word uitgerekend door de verstreken tijd "elapsed" te vermenigvuldigen door de snelheid van het geluid op aarde
                # Hierdoor krijgen we de afstand dat het signaal aflegde heen en terug.
                # Omdat we alleen de afstand tot een object willen weten moeten we dit delen door 2.
                # Nu hebben we een variabele met de afstand tot een object in cm
                distancet = round((elapsed * 34300) / 2, 0)


                # Terwijl de afstand ("distancet") groter is dan 75 cm
                while distancet > 75:
                    GPIO.output(GPIO_GreenLED, True) # De groene LED word aan gezet omdat de afstand tot de auto groter is dan 75 cm
                    car_still_near = False # Er word een nieuwe variabele gemaakt. Dit hebben we nodig om de status van de afstand tot de auto te bepalen
                    #print("The car is not near") # Hier print ik dat de auto niet dichtbij is. Dit deed ik voor het testen van het programma
                    break # We breken hier uit de loop. Dit zorgt ervoor dat deze loop niet voor altijd aan blijft

                # Terwijl de afstand ("distancet") kleiner is dan 75cm of gelijk aan 75cm
                while distancet <= 75 and car_still_near == False:
                    # Terwijl de auto niet dichtbij is:
                    #while car_still_near == False:
                    GPIO.output(GPIO_GreenLED, False) # De auto is dichterbij dan 75cm en de auto is nog steeds dichtbij variabele is False
                    # Dus gaat nu de groene lamp uit
                    GPIO.output(GPIO_RedLED, True) # De rode lamp gaat aan
                    GPIO.output(GPIO_YellowLED, True) # En de witte lamp gaat ook aan

                    time.sleep(300) # nu wachten we 300 seconden ("5 minuten")

                    GPIO.output(GPIO_RedLED, False) # En dan gaan de rode lamp weer uit
                    GPIO.output(GPIO_YellowLED, False) # En de witte lamp gaat ook uit

                    car_still_near = True # We zeggen nu dat de auto nog steeds dichtbij is zodat de lampen niet weer aan gaan wanneer het programma overnieuw draait
                        #print("The car_near variable is now True") # Hier print ik dat de auto nog steeds dichtbij is voor het testen van het programma
                        #break # We breken ook hier uit de loop zodat deze niet voor altijd aan blijft
                    break # Nu breken we weer uit de loop

                while car_still_near == True: # Hier gebruiken we de variabele "car_still_near" dit is de status van de afstand tot de auto.
                    # Deze variabele zorgt ervoor dat wanneer de rode en witte lampen al een keer aan zijn geweest en de auto staat er nog steeds
                    # Dan gaan de lampen niet nog een keer aan
                    GPIO.output(GPIO_GreenLED, False) # Hier worden alle lampen uit gezet omdat de auto nog steeds voor de sensor staat
                    GPIO.output(GPIO_RedLED, False)
                    GPIO.output(GPIO_YellowLED, False)
                    #print("The car is near") # Hier print ik dat de auto dichtbij is voor het testen van het programma
                    break # We breken weer uit de loop zodat deze niet voor altijd blijft draaien

            else: # Als het item met uuid="12345678-0000-0000-0000-000000000000" niet gevonden is dan breken we uit de loop en proberen we het programma overnieuw
                GPIO.output(GPIO_GreenLED, False) # Nu zetten we alles uit als het bluetooth apparaat niet gevonden is
                GPIO.output(GPIO_RedLED, False)
                GPIO.output(GPIO_YellowLED, False)
                break
except KeyboardInterrupt: # Als we op ctrl+c drukken dan stopt het programma. dit is nodig omdat we een While True loop gebruiken die voor altijd blijft lopen
    GPIO.output(GPIO_RedLED, False) # We zetten alle LEDs uit zodat wanneer het programma start we weer schoon kunnen beginnen
    GPIO.output(GPIO_GreenLED, False)
    GPIO.output(GPIO_YellowLED, False)
    GPIO.cleanup() # Hier maken we het trigger en echo signaal schoon, ook dit is zodat we weer schoon zonder errors het programma opnieuw kunnen draaien
    pass # Hier stopt het programma
