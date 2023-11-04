<p align="center">
  <img src="https://media1.tenor.com/images/f3300b1ad8320c61263cbd37e1072a7c/tenor.gif?itemid=15501310" alt="scanner pic" width="150" height="150" /> 
</p>

# ScannerGUI

automated program that scan barcode and output data to csv file

Download:  [release v3.0](https://github.com/ZianWang-236/scannerGUI/releases/tag/v3.0)


## functionality
1. each scann is feedbacked with voices, 'next', 'duplicate', 'again', to help user know the scan status
2. the input data is filtered, namly, the duplicates are removed, the code that doesn't match predefined patern is removed
3. the data is saved to csv file in real time, even the program crashes or the user closed the program accidentially, no data will be lost
4. each csv file is named by date and each day will only have one csv file for better logging purpose
5. the program can be paused, and restart to continue scanning
6. the scan counter can help knowing how many unique barcode is scanned so far
7. the menu bar provide easy access to csv folder and program folder for better user experiences
8. the program can read scan history (implemented but not avaliable in current release V1.1)

## GUI
1. designed with PyQt6
2. includes input field and display field to input parcel ID and displays the scan history
3. start, stop button to start and stop the program
4. search input textbox
5. scan counter
6. menu bar that provide easy one-click action to open csv and program location

## future functionality
1. search scan history
2. menubar: read history period settings
3. UI: add search mode seleection(radio btn or drop down)
