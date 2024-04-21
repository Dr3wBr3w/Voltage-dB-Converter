#!/usr/bin/env python3
"""Voltage / dB converter by Andrew Austin.
- Cross-platform Python tkinter GUI that converts between Voltage Root Mean Square (V-RMS),
  Voltage peak (Vp), Voltage peak to peak (Vpp), dBu (decibel unloaded), dBV (decibel Volt)
  and dBm (decibel milliwatt)
- dBu/dbV are logarithmic voltage ratios with references of 0.7745966692v / 1v
- The reference of 0.7745966692v comes from √(0.001W * 600 ohms)
- dBm is a logarithmic power ratio with reference of 1mW; requires impedance Z (default 600ohms)
- Vp = Vpp / 2 -OR- Vp = Vrms * √2
- Vpp = Vp * 2 -OR- Vpp = 2 * Vrms * √2
- Vrms = Vp * (1 / √2) -OR- Vrms = (Vpp / 2) * (1 / √2) -OR- Vrms = 0.7745966692 * 10 ^ (dBu / 20)
  -OR- Vrms = 10 ^ (dBV / 20) -OR- Vrms = √((0.001 * Z) * 10 ^ (dBm / 10))
- dBu = 20 * log(Vrms / 0.7745966692)
- dBV = 20 * log(Vrms)
- dBm = 10 * log((Vrms ^ 2) / (0.001 * Z))
"""
import math
import os
import platform
import sys
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox

APPTITLE: str = 'Voltage/dB Converter'

class VoltdBGUI:
    """Voltage/DB Converter GUI Class"""


    def __init__(self) -> None:
        """Provides a GUI that allows conversion between Vp, Vpp, VRMS, dBu, dBV and dBm.
        Constructor builds the GUI and starts the mainloop"""
        # Default calculation rounding value
        self.rounding = 4
        # Create the main window
        self.main = tk.Tk()
        self.main.title(APPTITLE)
        # Set the app style and icon
        self.set_style()
        # Set GUI paddings, then create the labels, entry boxes and buttons
        self.paddings = {'padx' : 2, 'pady' : 4}
        # Row 0: Title
        self.title = ttk.Label(self.main, text=APPTITLE, style='title.TLabel', anchor='center')
        self.title.grid(column=0, row=0, columnspan=3, sticky='ew')
        # Row 1: V-p
        self.vp_box = ttk.Entry(self.main, width=15, font=self.default_font)
        self.vp_box.grid(column=0, row=1, sticky='e', **self.paddings)
        self.vp_label = ttk.Label(self.main, text='V-p', width=6, style='main.TLabel')
        self.vp_label.grid(column=1, row=1, sticky='w', **self.paddings)
        self.vp_button = ttk.Button(self.main, text='Convert', command=self.calc_vp, style='main.TButton')
        self.vp_button.grid(column=2, row=1, sticky='ew', **self.paddings)
        # Row 2: V-pp
        self.vpp_box = ttk.Entry(self.main, width=15, font=self.default_font)
        self.vpp_box.grid(column=0, row=2, sticky='e', **self.paddings)
        self.vpp_label = ttk.Label(self.main, text='V-pp', style='main.TLabel')
        self.vpp_label.grid(column=1, row=2, sticky='w', **self.paddings)
        self.vpp_button = ttk.Button(self.main, text='Convert', command=self.calc_vpp, style='main.TButton')
        self.vpp_button.grid(column=2, row=2, sticky='ew', **self.paddings)
        # Row 3: V-RMS
        self.vrms_box = ttk.Entry(self.main, width=15, font=self.default_font)
        self.vrms_box.grid(column=0, row=3, sticky='e', **self.paddings)
        self.vrms_label = ttk.Label(self.main, text='V-RMS', style='main.TLabel')
        self.vrms_label.grid(column=1, row=3, sticky='w', **self.paddings)
        self.vrms_button = ttk.Button(self.main, text='Convert', command=self.calc_vrms, style='main.TButton')
        self.vrms_button.grid(column=2, row=3, sticky='ew', **self.paddings)
        # Row 4: dBu
        self.dbu_box = ttk.Entry(self.main, width=15, font=self.default_font)
        self.dbu_box.grid(column=0, row=4, sticky='e', **self.paddings)
        self.dbu_label = ttk.Label(self.main, text='dBu', style='main.TLabel')
        self.dbu_label.grid(column=1, row=4, sticky='w', **self.paddings)
        self.dbu_button = ttk.Button(self.main, text='Convert', command=self.calc_dbu, style='main.TButton')
        self.dbu_button.grid(column=2, row=4, sticky='ew', **self.paddings)
        # Row 5: dBV
        self.dbv_box = ttk.Entry(self.main, width=15, font=self.default_font)
        self.dbv_box.grid(column=0, row=5, sticky='e', **self.paddings)
        self.dbv_label = ttk.Label(self.main, text='dBV', style='main.TLabel')
        self.dbv_label.grid(column=1, row=5, sticky='w', **self.paddings)
        self.dbv_button = ttk.Button(self.main, text='Convert', command=self.calc_dbv, style='main.TButton')
        self.dbv_button.grid(column=2, row=5, sticky='ew', **self.paddings)
        # Row 6: dBm
        self.dbm_box = ttk.Entry(self.main, width=15, font=self.default_font)
        self.dbm_box.grid(column=0, row=6, sticky='e', **self.paddings)
        self.dbm_label = ttk.Label(self.main, text='dBm', style='main.TLabel')
        self.dbm_label.grid(column=1, row=6, sticky='w', **self.paddings)
        self.dbm_button = ttk.Button(self.main, text='Convert', command=self.calc_dbm, style='main.TButton')
        self.dbm_button.grid(column=2, row=6, sticky='ew', **self.paddings)
        # Row 7: Impedance
        self.impedance_box = ttk.Entry(self.main, width=10, font=self.default_font)
        # Default impedance is 600 ohms
        self.impedance_box.insert(0, '600')
        self.impedance_box.grid(column=0, row=7, sticky='e', **self.paddings)
        self.impedance_label = ttk.Label(self.main, text='ohms impedance (dBm)', width=20, style='main.TLabel')
        self.impedance_label.grid(column=1, columnspan=2, row=7, sticky='w', **self.paddings)
        # Row 8: Rounding
        self.rounding_spinbox = ttk.Spinbox(self.main, from_=1, to=10, width=6, font=self.default_font)
        self.rounding_spinbox.insert(0, self.rounding)
        self.rounding_spinbox.grid(column=0, row=8, sticky='e', **self.paddings)
        self.rounding_label = ttk.Label(self.main, text='decimal places', width=20, style='main.TLabel')
        self.rounding_label.grid(column=1, columnspan=2, row=8, sticky='w', **self.paddings)
        # Row 9: Window on-top option
        self.on_top = tk.IntVar()
        # Default window is not on top
        self.on_top.set(False)
        # Specify a callback function whenever the checkbox is clicked
        self.on_top.trace_add('write', self.update_on_top)
        self.on_top_checkbox = ttk.Checkbutton(self.main, variable=self.on_top)
        self.on_top_checkbox.grid(column=0, row=9, **self.paddings, sticky='se')
        self.on_top_label = ttk.Label(self.main, text='Window always on top', width=20, style='main.TLabel')
        self.on_top_label.grid(column=1, columnspan=2, row=9, sticky='w', **self.paddings)
        # End of constructor: start the GUI main loop
        self.main.mainloop() 

    def set_style(self) -> None:
        """Sets the application style/fonts based on the OS, and the app icon"""
        self.style = ttk.Style(self.main)
        if platform.system() == 'Windows':
            self.style.configure('title.TLabel', font=('Segoe UI', 15, 'bold'))
            self.style.configure('main.TLabel', font=('Segoe UI', 11, 'normal'))
            self.style.configure('main.TButton', font=('Segoe UI', 11, 'normal'))
            # For use by Entry and Spin boxes, as they don't honor font Styles...
            self.default_font = ('Segoe UI', 11, 'normal')
        else:
            self.style.configure('title.TLabel', font=('Liberation Sans', 15, 'bold'))
            self.style.configure('main.TLabel', font=('Liberation Sans', 11, 'normal'))
            self.style.configure('main.TButton', font=('Liberation Sans', 11, 'normal'))
            self.default_font = ('Liberation Sans', 11, 'normal')
        try:
            # Use an .ico icon if app is run as a frozen Windows exe via PyInstaller
            if getattr(sys, 'frozen', False):
                application_path = sys._MEIPASS
                self.main.iconbitmap(default=os.path.join(application_path, 'arrows.ico'))
            else:
                application_path = os.path.dirname(os.path.abspath(__file__))
                icon_path = os.path.join(application_path, 'arrows.png')
                self.main.iconphoto(False, tk.PhotoImage(file=icon_path))
        except Exception:
            # Use the default tkinter icon if there was an error. 
            pass

    def update_rounding(self) -> None:
        """Reads the current value of the rounding spinbox"""
        try:
            rounding_val = int(self.rounding_spinbox.get())
            if rounding_val < 1 or rounding_val > 10:
                raise ValueError
            else:
                self.rounding = rounding_val
        except ValueError:
            messagebox.showerror('Decimal places rounding error', 'Please enter a number between 1 and 10.') 

    def update_on_top(self, var, index, mode) -> None:
        """Sets the main window always on top property. Callback triggered
        by tkinter trace_add attached to the checkbox.
        """
        on_top_box = self.on_top.get()
        if on_top_box:
            self.main.attributes('-topmost', True)
        else:
            self.main.attributes('-topmost', False)

    def calc_vp(self) -> None:
        """Calculates/updates other values from the entered V-p"""
        self.update_rounding()
        try:
            entry_val = float(self.vp_box.get())
            if entry_val <= 0.0:
                raise ValueError
            else:
                # Update the vpp entry box
                self.update_vpp(vp = entry_val)
                # Update the vrms entry box
                self.update_vrms(vp = entry_val)                
                # With the vrms entry box calculated, update the db entry boxes with it
                self.update_dbu(float(self.vrms_box.get()))
                self.update_dbv(float(self.vrms_box.get()))
                self.update_dbm(float(self.vrms_box.get()))
        except ValueError:
            messagebox.showerror('V-p Error', 'Please enter a number greater than 0.')      

    def calc_vpp(self) -> None:
        """Calculates/updates other values from the entered V-pp"""
        self.update_rounding()
        try:
            entry_val = float(self.vpp_box.get())
            if entry_val <= 0.0:
                raise ValueError
            else:
                # Update the vp entry box
                self.update_vp(vpp = entry_val)
                # Update the vrms entry box
                self.update_vrms(vpp = entry_val)                  
                # With the vrms entry box calculated, update the db entry boxes with it
                self.update_dbu(float(self.vrms_box.get()))
                self.update_dbv(float(self.vrms_box.get()))
                self.update_dbm(float(self.vrms_box.get()))
        except ValueError:
            messagebox.showerror('V-pp Error', 'Please enter a number greater than 0.')

    def calc_vrms(self) -> None:
        """Calculates/updates other values from the entered V-RMS"""
        self.update_rounding()
        try:
            entry_val = float(self.vrms_box.get())
            if entry_val <= 0.0:
                raise ValueError
            else:
                # Update the vp entry box
                self.update_vp(vrms = entry_val)
                # Update the vpp entry box
                self.update_vpp(vrms = entry_val)                
                # Update the db entry boxes
                self.update_dbu(entry_val)
                self.update_dbv(entry_val)
                self.update_dbm(entry_val)
        except ValueError:
            messagebox.showerror('V-RMS Error', 'Please enter a number greater than 0.')

    def calc_dbu(self) -> None:
        """Calculates other values from the entered dbu"""
        self.update_rounding()
        try:
            entry_val = float(self.dbu_box.get())
        except ValueError:
            messagebox.showerror('dBu Error', 'Invalid number.')
        else:
            # Calculate / update the V-RMS text box
            self.update_vrms(dbu = entry_val)
            # Now that the V-RMS text box is correct, update the other values from V-RMS
            self.update_vp(vrms = float(self.vrms_box.get()))
            self.update_vpp(vrms = float(self.vrms_box.get()))
            self.update_dbv(vrms = float(self.vrms_box.get()))
            self.update_dbm(vrms = float(self.vrms_box.get()))

    def calc_dbv(self) -> None:
        """Calculates/updates other values from the entered dbv"""
        self.update_rounding()
        try:
            entry_val = float(self.dbv_box.get())
        except ValueError:
            messagebox.showerror('dBV Error', 'Invalid number.')
        else:
            # Calculate / update the V-RMS text box
            self.update_vrms(dbv = entry_val)
            # Now that the V-RMS text box is correct, update the other values from V-RMS
            self.update_vp(vrms = float(self.vrms_box.get()))
            self.update_vpp(vrms = float(self.vrms_box.get()))
            self.update_dbu(float(self.vrms_box.get()))
            self.update_dbm(float(self.vrms_box.get()))

    def calc_dbm(self) -> None:
        """Calculates/updates other values from the entered dbm"""
        self.update_rounding()
        try:
            entry_val = float(self.dbm_box.get())
        except ValueError:
            messagebox.showerror('dBm Error', 'Invalid number.')
        else:
            # Calculate / update the V-RMS text box
            self.update_vrms(dbm = entry_val)
            # Now that the V-RMS text box is correct, update the other values from V-RMS
            self.update_vp(vrms = float(self.vrms_box.get()))
            self.update_vpp(vrms = float(self.vrms_box.get()))
            self.update_dbu(float(self.vrms_box.get()))
            self.update_dbv(float(self.vrms_box.get()))

    def update_vp(self, vpp: int|float|None=None, vrms: int|float|None=None) -> None:
        """Updates the vp entry box using vpp or vrms"""
        if vpp is not None:
            vp = (vpp / 2)
            # Remove ".0" if a whole number
            if vp.is_integer():
                vp = int(vp)
            else:
                # Format as fixed-width floating point determined by the rounding (PEP498)
                vp = f'{vp:.{self.rounding}f}'
            # Clear and update the vp entry box
            self.vp_box.delete(0, tk.END)
            self.vp_box.insert(0, str(vp))
            
        elif vrms is not None:
            vp = (vrms * math.sqrt(2))
            if vp.is_integer():
                vp = int(vp)
            else:
                vp = f'{vp:.{self.rounding}f}'
            # Clear and update the vp entry box
            self.vp_box.delete(0, tk.END)
            self.vp_box.insert(0, str(vp))

    def update_vpp(self, vp: int|float|None=None, vrms: int|float|None=None) -> None:
        """Updates the vpp entry box using vp or vrms"""
        if vp is not None:
            vpp = (vp * 2)
            if vpp.is_integer():
                vpp = int(vpp)
            else:
                vpp = f'{vpp:.{self.rounding}f}'
            # Clear and update the vpp entry box
            self.vpp_box.delete(0, tk.END)
            self.vpp_box.insert(0, str(vpp))
        elif vrms is not None:
            vpp = (2 * vrms * math.sqrt(2))
            if vpp.is_integer(): # Remove ".0" if a whole number
                vpp = int(vpp)
            else:
                vpp = f'{vpp:.{self.rounding}f}'
            # Clear and update the vpp entry box
            self.vpp_box.delete(0, tk.END)
            self.vpp_box.insert(0, str(vpp))
    
    def update_vrms(self, vp: int|float|None=None, vpp: int|float|None=None, 
                    dbu: int|float|None=None, dbv: int|float|None=None, 
                    dbm: int|float|None=None) -> None:
        """Updates the vrms entry box using any other parameter"""
        if vp is not None:
            vrms = vp * (1 / math.sqrt(2))
            if vrms.is_integer():
                vrms = int(vrms)
            else:
                vrms = f'{vrms:.{self.rounding}f}'
            # Clear and update the vrms entry box
            self.vrms_box.delete(0, tk.END)
            self.vrms_box.insert(0, str(vrms))
        elif vpp is not None:
            vrms = (vpp / 2) * (1 / math.sqrt(2))
            if vrms.is_integer():
                vrms = int(vrms)
            else:
                vrms = f'{vrms:.{self.rounding}f}'
            # Clear and update the vrms entry box
            self.vrms_box.delete(0, tk.END)
            self.vrms_box.insert(0, str(vrms))
        elif dbu is not None:
            vrms = 0.7745966692 * 10**(dbu / 20)
            if vrms.is_integer():
                vrms = int(vrms)
            else:
                vrms = f'{vrms:.{self.rounding}f}'
            # Clear and update the vrms entry box
            self.vrms_box.delete(0, tk.END)
            self.vrms_box.insert(0, str(vrms))
        elif dbv is not None:
            vrms = 10**(dbv / 20)
            if vrms.is_integer():
                vrms = int(vrms)
            else:
                vrms = f'{vrms:.{self.rounding}f}'
            # Clear and update the vrms entry box
            self.vrms_box.delete(0, tk.END)
            self.vrms_box.insert(0, str(vrms))
        elif dbm is not None:
            try:
                impedance = float(self.impedance_box.get())
                if impedance <= 0.0:
                    raise ValueError
                else:
                    vrms = math.sqrt((0.001 * impedance) * 10**(dbm / 10))
                    if vrms.is_integer():
                        vrms = int(vrms)
                    else:
                        vrms = f'{vrms:.{self.rounding}f}'
                    # Clear and update the vrms entry box
                    self.vrms_box.delete(0, tk.END)
                    self.vrms_box.insert(0, str(vrms))   
            except ValueError:
                messagebox.showerror('dBm Impedance Error', 'Please enter an impedance number greater than 0.')                             

    def update_dbu(self, vrms: int|float|None) -> None:
        """Updates the dBu entry box using vrms"""
        dbu = 20 * math.log10((vrms / 0.7745966692))
        if dbu.is_integer():
            dbu = int(dbu)
        else:
            dbu = f'{dbu:.{self.rounding}f}'
        # Clear and update the dbu entry box
        self.dbu_box.delete(0, tk.END)
        self.dbu_box.insert(0, str(dbu))

    def update_dbv(self, vrms: int|float|None) -> None:
        """Updates the dBV entry box using vrms"""
        dbv = 20 * math.log10(vrms)
        if dbv.is_integer():
            dbv = int(dbv)
        else:
            dbv = f'{dbv:.{self.rounding}f}'
        # Clear and update the dbv entry box
        self.dbv_box.delete(0, tk.END)
        self.dbv_box.insert(0, str(dbv))

    def update_dbm(self, vrms: int|float|None) -> None:
        """Updates the dBm entry box using vrms & impedance"""
        try:
            impedance = float(self.impedance_box.get())
            if impedance <= 0.0:
                raise ValueError
            else:
                dbm = 10 * math.log10((vrms**2) / (0.001 * impedance))
                if dbm.is_integer():
                    dbm = int(dbm)
                else:
                    dbm = f'{dbm:.{self.rounding}f}'
                # Clear and update the dbm entry box
                self.dbm_box.delete(0, tk.END)
                self.dbm_box.insert(0, str(dbm))
        except ValueError:
            messagebox.showerror('dBm Impedance Error', 'Please enter an impedance number greater than 0.') 


# Main - start the GUI
if __name__ == '__main__':
    gui = VoltdBGUI()
