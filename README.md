DUTCH VERSION:

Programmeur: Steffiejonko
Datum: 9 Maart 2022

Dit programma is gebaseerd op de Ble-beacon-scanner "https://github.com/bowdentheo/BLE-Beacon-Scanner"

Dit programma scanned voor bluetooth ibeacons. Dit programma simuleert een pakkeer systeem voor een garage.
Wanneer er een iBeacon is gevonden en de auto verderweg is dan 75 Centimeter, brandt er een groene lamp.
Wanneer de auto dichterbij dan 75 Centimeter is, brandt er een rode en een witte lamp, deze lampen blijven aan voor 5 minuten
Indien de auto na de 5 minuten nog steeds op de oprit staat, blijven de rode en witte lampen uit.
Wanneer de auto weer weg is gaat de groene lamp aan.

Het programma gebruikt de bluetooth._bluetooth library om te communiceren met de blutooth-chip op de raspberry pi4.
De ScanUtility library word gebruikt om voor een iBeacons te scannen en dan de juiste iBeacon uit de lijst te halen.
De RPi.GPIO library word gebruikt om de Afstands-sensor aan te sturen op de rpi.


ENGLISH VERSION:

Programmer: Steffiejonko
Date: March 9th 2022

This program is based on the Ble-beacon-scanner: "https://github.com/bowdentheo/BLE-Beacon-Scanner"

This program scans for bluetooth ibeacons. it simulates a parking system for a parking garage.
When an ibeacon is found and the car is more than 75cm away, a green LED will be on
When the car gets closer than 75cm, a red and white LED will turn on, these LEDs will stay on for 5 minutes.
If the car is still in the parking garage after 5 minutes, then the red and white LEDs will turn off.
When the car leaves again the green LED will turn on.

The program uses the pybluez library "https://github.com/pybluez/pybluez" to communicate with the bluetooth-chip on the raspberry pi4
The ScanUtility library is used to scan for ibeacons and to get the right beacon of your choice from the list of available beacons
The RPi.GPIO library "https://pypi.org/project/RPi.GPIO/" is used to communicate with the ultrasonic sensor




