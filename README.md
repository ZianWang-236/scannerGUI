# scannerGUI
automated program that scan barcode and output data to csv file
release v1.0: https://github.com/ZianWang-236/scannerGUI/releases/tag/v1

functionality
1. each scann is feedbacked with voices, 'next', 'duplicate', 'again', to help user know the scan status
2. the input data is filtered, namly, the duplicates are removed, the code that doesn't match predefined patern is removed
3. the data is saved to csv file in real time, even the program crashes or the user closed the program accidentially, no data will be lost
4. each csv file is named by date and each day will only have one csv file for better logging purpose
5. the program can be paused, and restart to continue scanning

GUI
1. designed with PyQt6
2. includes input field and display field to input parcel ID and displays the scan history
3. start, stop button to start and stop the program

future functionality
1. search scan history
