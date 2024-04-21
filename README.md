# Voltage / dB Converter

Cross-platform Python tkinter GUI that converts between Voltage Root Mean Square (V-RMS), Voltage peak (Vp), Voltage peak to peak (Vpp), dBu (decibel unloaded), dBV (decibel Volt) and dBm (decibel milliwatt). Run **voltage-db_convert.pyw** to launch the GUI.

![Voltage dB Converter in Windows](/media/ConverterWindows.png "Voltage dB Converter in Windows")
![Voltage dB Converter in Linux](/media/ConverterLinux.png "Voltage dB Converter in Linux")

- dBu/dbV are logarithmic voltage ratios with references of 0.7745966692v / 1v
- The reference of 0.7745966692v comes from √(0.001W * 600 ohms)
- dBm is a logarithmic power ratio with reference of 1mW; requires impedance Z (default 600ohms)
- **Vp** = Vpp / 2 *-OR-* **Vp** = Vrms * √2
- **Vpp** = Vp * 2 *-OR-* **Vpp** = 2 * Vrms * √2
- **Vrms** = Vp * (1 / √2) *-OR-* **Vrms** = (Vpp / 2) * (1 / √2) *-OR-* **Vrms** = 0.7745966692 * 10 ^ (dBu / 20)

  *-OR-* **Vrms** = 10 ^ (dBV / 20) *-OR-* **Vrms** = √((0.001 * Z) * 10 ^ (dBm / 10))
- **dBu** = 20 * log(Vrms / 0.7745966692)
- **dBV** = 20 * log(Vrms)
- **dBm** = 10 * log((Vrms ^ 2) / (0.001 * Z))

## Prerequisites

Requires [Python](https://python.org/) to be installed to work (at least v3.10). No additional packages required in Windows.

For Linux, requires a distribution with a GUI. Some Linux distributions may require tkinter to be installed separately, for example:
- Ubuntu: `sudo apt install python3-tk`
- CentOS: `sudo yum install python3-tkinter`

## Build Windows Exectutable

1. If you want to build this script into a portable Windows executable so the user doesn't need to install Python:

    `python -m pip install pyinstaller`

2. Run build.cmd to create the executable
3. Alternatively, browse to this folder in terminal / command prompt, and execute:

    `python -m PyInstaller --add-data "src\arrows.ico:." --icon=src\arrows.ico --onefile --clean --name=Voltage-dB-Converter -w src\voltage-db_convert.pyw`

4. The built exe is located in the **dist** folder.

**NOTE:** If you are having trouble running the exe, add `--console` and `--debug=all` to the end of the build command. Then run the exe from terminal / command prompt to view the debug / error output.

## Other

The arrows icon was created with [Inkscape](https://inkscape.org/)
