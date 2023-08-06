'''
###########################
VTOFG: Vibration Test Object Function Generator
###########################
vtofg.plotter
Author: Zack Ravetz

This file contains VTOFG's "SweepWave" and "WaveUI classes. These are used for the creation
of wave in the signal for the function generator.
'''

import numpy as np
import tkinter as tk

class SweepWave:
    '''
    Backend for a wave swept linearly through frequencies

    Attributes
    ----------
    start_freq: int
        starting frequency for the swept wave, in Hz
    end_freq: int
        end frequency for the swept wave, in Hz
    amplitude: float
        relative amplitude of the swept wave, value<1
    sweep_period: float
        period of the swept wave, in seconds

    Methods
    -------
    get_signal(times_raw) -> (Any, float)
        returns signal for given times and amplitude
    '''
    def __init__(self,  start_freq: int, end_freq: int, amplitude: float, sweep_period: float) -> None:
        '''
        Constructs the swept wave

        Parameters
        ----------
        start_freq: int
            starting frequency for the swept wave, in Hz
        end_freq: int
            end frequency for the swept wave, in Hz
        amplitude: float
            relative amplitude of the swept wave, value<1
        sweep_period: float
            period of the swept wave, in seconds
        '''
        self.start_freq = start_freq
        self.end_freq = end_freq
        self.amplitude = amplitude
        self.sweep_period = sweep_period

    def get_signal(self, times_raw, norm_time = False, offset = 0):
        '''
        Returns the signal at the times provides

        Parameters
        ----------
        times_raw: array like
            an array of times to calculate the signal for, times in seconds after start

        Returns
        -------
        sig: array like
            signal of wave at the given times, arbitrary units
        self.amplitude: float
            relative amplitude of the swept wave, value<1
        '''
        if self.sweep_period == 0: #ensures no divide by zero in calculating frequencies
            return np.zeros(times_raw.shape), 0

        else:
            if self.start_freq != self.end_freq:
                times = (times_raw%self.sweep_period) #modular of given times for given period
                k_diff = self.start_freq - (self.start_freq-self.end_freq)*times/(2*self.sweep_period) #unitary frequencies for given times
            else:
                times = times_raw #keeps times if frequency doesn't change
                k_diff = self.start_freq
            wave_func = 2*np.pi*k_diff*times #phases for given times
            wave = np.sin(wave_func) 
            sig = wave*self.amplitude

            return sig, self.amplitude

class BandWave:
    ##########
    #Doesnt work dont think
    #is it working now? kind of but not when phases change 
    ##########
    '''
    Backend for a wave swept linearly through frequencies

    Attributes
    ----------
    start_freq: int
        starting frequency for the swept wave, in Hz
    end_freq: int
        end frequency for the swept wave, in Hz
    amplitude: float
        relative amplitude of the swept wave, value<1
    sweep_period: float
        period of the swept wave, in seconds

    Methods
    -------
    get_signal(times_raw) -> (Any, float)
        returns signal for given times and amplitude
    '''
    def __init__(self,  start_high_freq: int, start_low_freq: int, end_high_freq: int, end_low_freq: int, amplitude: float, sweep_period: float, FR: float) -> None:
        '''
        Constructs the swept wave

        Parameters
        ----------
        start_freq: int
            starting frequency for the swept wave, in Hz
        end_freq: int
            end frequency for the swept wave, in Hz
        amplitude: float
            relative amplitude of the swept wave, value<1
        sweep_period: float
            period of the swept wave, in seconds
        '''
        self.start_high_freq = start_high_freq
        self.end_high_freq = end_high_freq
        self.start_low_freq = start_low_freq
        self.end_low_freq = end_low_freq
        self.amplitude = amplitude
        self.sweep_period = sweep_period
        self.FR = FR

    def get_signal(self, times_raw, norm_time = False, offset = 0):
        '''
        Returns the signal at the times provides

        Parameters
        ----------
        times_raw: array like
            an array of times to calculate the signal for, times in seconds after start

        Returns
        -------
        sig: array like
            signal of wave at the given times, arbitrary units
        self.amplitude: float
            relative amplitude of the swept wave, value<1
        '''
        if self.sweep_period == 0: #ensures no divide by zero in calculating frequencies
            return np.zeros(times_raw.shape), 0

        else:
            times_raw = times_raw+offset
            
            if (self.start_high_freq != self.end_high_freq) or (self.start_low_freq != self.end_low_freq):
                times = (times_raw%self.sweep_period) #modular of given times for given period
                k_high = self.start_high_freq - (self.start_high_freq-self.end_high_freq)*times/(self.sweep_period) #unitary frequencies for given times
                k_low = self.start_low_freq - (self.start_low_freq-self.end_low_freq)*times/(self.sweep_period) #unitary frequencies for given times
                times = times%(1/self.FR)
                times = times - np.max(times)/2
            
            else:
                times = times_raw #keeps times if frequency doesn't change
                k_high = self.start_high_freq
                k_low = self.start_low_freq

            # period = times[1]-times[0]
            # freqs = np.fft.rfftfreq(10*times.size, d = period)
            # freqs_mask = freqs>=np.min([k_low, k_high])
            # freqs_mask = freqs_mask*(freqs<=np.max([k_low, k_high]))
            # thetas = np.random.uniform(-np.pi, np.pi, freqs.size)
            # random_ft_sig = (np.cos(thetas)+1j*np.sin(thetas))*freqs_mask
            # sig = np.fft.irfft(random_ft_sig)[-times.size:]
            # sig = sig/np.max(sig)

            #discrete resolution method
            k_diff = np.abs(k_high-k_low)
            n_angles = (k_diff//self.FR)+1
            # added = np.abs(n_angles%2 -1)
            # n_angles = n_angles+added
            k_avg = (k_high+k_low)
            numer_sin = np.sin(np.pi*n_angles*self.FR*times)
            denom_sin = np.sin(np.pi*self.FR*times)*np.max(n_angles)
            mult = np.divide(numer_sin, denom_sin, out=np.zeros_like(numer_sin), where=denom_sin!=0)
            sig = mult*np.sin(np.pi*k_avg*times)

            # fliper = 1
            # if self.FR>0:
            #     times = times%self.frame_period
            #     fliper = times//self.frame_period
            #     fliper = (-1)**fliper
            #     times = times-self.frame_period/2
            # wave_func_high = 2*k_high*times #phases for given times
            # wave_func_low = 2*k_low*times #phases for given times
            # wave = (k_high*np.sinc(wave_func_high) - k_low*np.sinc(wave_func_low))/(k_high-k_low)
            sig = sig*self.amplitude
            #if self.FR>0:
            #    sig = sig*fliper

            return sig, self.amplitude

class SweepwaveUI:
    '''
    The user interface for the swept waves

    Attributes
    -----------
    main: FunctionGenerator
        The FunctionGenerator object that this wave is attached to
    frame: tkinter Frame
        the tkinter frame object that the tkinter widgets for this wave are placed in
    index: int
        the unique index 
    amp_var: tkinter DoubleVar
        the tkinter variable attached to the amplitude input
    amp_input: tkinter Entry
        the tkinter entry box for the amplitude 
    start_var: tkinter IntVar
        the tkinter variable attached to the start frequency input
    start_input: tkinter Entry
        the tkinter entry box for the start frequency 
    end_var: tkinter IntVar
        the tkinter variable attached to the end frequency input
    end_input: tkinter Entry
        the tkinter entry box for the end frequency 
    time_var: tkinter DoubleVar
        the tkinter variable attached to the sweep period input
    time_input: tkinter Entry
        the tkinter entry box for the sweep period 
    
    Methods
    -------
    get_wave -> SweepWave
        Creates the backend SweepWave object for the values entered into the UI
    remove_widgets
        Function to remove the tkinter widgets from view, used when deleting a wave
    update_index
        Updates the index and shows the tkinter widgets at the new index after a wave has been deleted
    '''

    def __init__(self, main, frame:tk.Frame, index: int):
        '''
        Constructs the user interface

        Parameters
        -----------
        main: FunctionGenerator
            The FunctionGenerator object that this wave is attached to
        frame: tkinter Frame
            The tkinter frame object that the tkinter widgets for this wave are placed in
        index: int
            The unique index of this wave
        '''
        self.main = main
        self.frame = frame
        self.index = index

        #creating the tkinter variables and widgets for this wave
        self.amp_var = tk.DoubleVar()
        self.amp_var.set(100)
        self.amp_input = tk.Entry(self.frame,
            textvariable=self.amp_var,
            validate='all',
            validatecommand=(self.main.vcmd_perc, '%P'))
        self.amp_input.grid(column=1, row=index, sticky='nsew')

        self.start_var = tk.IntVar()
        self.start_var.set(2000)
        self.start_input = tk.Entry(self.frame,
            textvariable=self.start_var,
            validate='all',
            validatecommand=(self.main.vcmd_int, '%P'))
        self.start_input.grid(column=3, row=index, sticky='nsew')

        self.end_var = tk.IntVar()
        self.end_var.set(2000)
        self.end_input = tk.Entry(self.frame,
            textvariable=self.end_var,
            validate='all',
            validatecommand=(self.main.vcmd_int, '%P'))
        self.end_input.grid(column=4, row=index, sticky='nsew')

        self.time_var = tk.DoubleVar()
        self.time_var.set(10)
        self.time_input = tk.Entry(self.frame,
            textvariable=self.time_var,
            validate='all',
            validatecommand=(self.main.vcmd_float, '%P'))
        self.time_input.grid(column=5, row=index, sticky='nsew')
    
    def __str__(self)->str:
        '''
        Creates the backend SweepWave object for the values entered into the UI

        Returns
        -------
        sweepwave: SweepWave
            the SweepWave object for the entries into this UI
        '''
        start_freq = self.start_var.get()
        end_freq = self.end_var.get()
        amplitude = self.amp_var.get()
        sweep_period = self.time_var.get()
        line = "S;{};{};{};{}\n".format(start_freq,  end_freq, amplitude, sweep_period)
        return line

    def from_line(self, line:str)->None:
        line = line.strip('S\n ;')
        line_l = line.split(';')
        self.start_var.set(int(line_l[0]))
        self.end_var.set(int(line_l[1]))
        self.amp_var.set(float(line_l[2]))
        self.time_var.set(float(line_l[3]))
                
    def get_wave(self)->SweepWave:
        '''
        Creates the backend SweepWave object for the values entered into the UI

        Returns
        -------
        sweepwave: SweepWave
            the SweepWave object for the entries into this UI
        '''
        start_freq = self.start_var.get()
        end_freq = self.end_var.get()
        amplitude = self.amp_var.get()/100
        sweep_period = self.time_var.get()
        sweepwave = SweepWave(start_freq, end_freq, amplitude, sweep_period)
        return sweepwave

    def remove_widgets(self)->None:
        '''
        Function to remove the tkinter widgets from view, used when deleting a wave
        '''
        self.amp_input.grid_forget()
        self.start_input.grid_forget()
        self.end_input.grid_forget()
        self.time_input.grid_forget()

    def update_index(self, index)->None:
        '''
        Updates the index and shows the tkinter widgets at the new index after a wave has been deleted

        Parameters
        ----------
        index: int
            New index for the wave
        '''
        self.index = index

        self.amp_input.grid(column=1, row=index, sticky='nsew')
        self.start_input.grid(column=3, row=index, sticky='nsew')
        self.end_input.grid(column=4, row=index, sticky='nsew')
        self.time_input.grid(column=5, row=index, sticky='nsew')

class BandwaveUI:
    '''
    The user interface for the swept waves

    Attributes
    -----------
    main: FunctionGenerator
        The FunctionGenerator object that this wave is attached to
    frame: tkinter Frame
        the tkinter frame object that the tkinter widgets for this wave are placed in
    index: int
        the unique index 
    amp_var: tkinter DoubleVar
        the tkinter variable attached to the amplitude input
    amp_input: tkinter Entry
        the tkinter entry box for the amplitude 
    start_var: tkinter IntVar
        the tkinter variable attached to the start frequency input
    start_input: tkinter Entry
        the tkinter entry box for the start frequency 
    end_var: tkinter IntVar
        the tkinter variable attached to the end frequency input
    end_input: tkinter Entry
        the tkinter entry box for the end frequency 
    time_var: tkinter DoubleVar
        the tkinter variable attached to the sweep period input
    time_input: tkinter Entry
        the tkinter entry box for the sweep period 
    
    Methods
    -------
    get_wave -> SweepWave
        Creates the backend SweepWave object for the values entered into the UI
    remove_widgets
        Function to remove the tkinter widgets from view, used when deleting a wave
    update_index
        Updates the index and shows the tkinter widgets at the new index after a wave has been deleted
    '''

    def __init__(self, main, frame:tk.Frame, index: int):
        '''
        Constructs the user interface

        Parameters
        -----------
        main: FunctionGenerator
            The FunctionGenerator object that this wave is attached to
        frame: tkinter Frame
            The tkinter frame object that the tkinter widgets for this wave are placed in
        index: int
            The unique index of this wave
        '''
        self.main = main
        self.frame = frame
        self.index = index

        self.start_frame = tk.Frame(self.frame)
        self.start_frame.grid(column=3, row=index, sticky='nsew')
        self.start_frame.columnconfigure(0, weight=1)
        self.start_frame.rowconfigure(0, weight=1)
        self.start_frame.rowconfigure(1, weight=1)

        self.end_frame = tk.Frame(self.frame)
        self.end_frame.grid(column=4, row=index, sticky='nsew')
        self.end_frame.columnconfigure(0, weight=1)
        self.end_frame.rowconfigure(0, weight=1)
        self.end_frame.rowconfigure(1, weight=1)

        self.label_frame = tk.Frame(self.frame)
        self.label_frame.grid(column=2, row=index, sticky='nsew')
        self.start_label = tk.Label(self.label_frame, text = "High Frequency")
        self.start_label.grid(column=0, row=0, sticky='nsew')
        self.end_label = tk.Label(self.label_frame, text = "Low Frequency")
        self.end_label.grid(column=0, row=1, sticky='nsew')

        #creating the tkinter variables and widgets for this wave
        self.amp_var = tk.DoubleVar()
        self.amp_var.set(100)
        self.amp_input = tk.Entry(self.frame,
            textvariable=self.amp_var,
            validate='all',
            validatecommand=(self.main.vcmd_perc, '%P'))
        self.amp_input.grid(column=1, row=index, sticky='nsew')

        self.start_high_var = tk.IntVar()
        self.start_high_var.set(2000)
        self.start_high_input = tk.Entry(self.start_frame,
            textvariable=self.start_high_var,
            validate='all',
            validatecommand=(self.main.vcmd_int, '%P'))
        self.start_high_input.grid(column=0, row=0, sticky='nsew')

        self.start_low_var = tk.IntVar()
        self.start_low_var.set(1000)
        self.start_low_input = tk.Entry(self.start_frame,
            textvariable=self.start_low_var,
            validate='all',
            validatecommand=(self.main.vcmd_int, '%P'))
        self.start_low_input.grid(column=0, row=1, sticky='nsew')

        self.end_high_var = tk.IntVar()
        self.end_high_var.set(2000)
        self.end_high_input = tk.Entry(self.end_frame,
            textvariable=self.end_high_var,
            validate='all',
            validatecommand=(self.main.vcmd_int, '%P'))
        self.end_high_input.grid(column=0, row=0, sticky='nsew')

        self.end_low_var = tk.IntVar()
        self.end_low_var.set(1000)
        self.end_low_input = tk.Entry(self.end_frame,
            textvariable=self.end_low_var,
            validate='all',
            validatecommand=(self.main.vcmd_int, '%P'))
        self.end_low_input.grid(column=0, row=1, sticky='nsew')

        self.time_var = tk.DoubleVar()
        self.time_var.set(10)
        self.time_input = tk.Entry(self.frame,
            textvariable=self.time_var,
            validate='all',
            validatecommand=(self.main.vcmd_float, '%P'))
        self.time_input.grid(column=5, row=index, sticky='nsew')

        self.FR_var = tk.DoubleVar()
        self.FR_var.set(10)
        self.FR_input = tk.Entry(self.frame,
            textvariable=self.FR_var,
            validate='all',
            validatecommand=(self.main.vcmd_float, '%P'))
        self.FR_input.grid(column=6, row=index, sticky='nsew')

    def __str__(self)->str:
        '''
        Creates the string for saving the wave

        Returns
        -------
        line:str
            the line for saving waves
        '''
        start_high_freq = self.start_high_var.get()
        end_high_freq = self.end_high_var.get()
        start_low_freq = self.start_low_var.get()
        end_low_freq = self.end_low_var.get()
        amplitude = self.amp_var.get()
        sweep_period = self.time_var.get()
        fps = self.FR_var.get()
        line = "B;{};{};{};{};{};{};{}\n".format(start_high_freq, end_high_freq, start_low_freq, end_low_freq, amplitude, sweep_period, fps)
        return line
    
    def from_line(self, line:str)->None:
        line = line.strip('B\n ;')
        line_l = line.split(';')
        self.start_high_var.set(int(line_l[0]))
        self.end_high_var.set(int(line_l[1]))
        self.start_low_var.set(int(line_l[2]))
        self.end_low_var.set(int(line_l[3]))
        self.amp_var.set(float(line_l[4]))
        self.time_var.set(float(line_l[5]))
        self.FR_var.set(float(line_l[6]))

    def get_wave(self)->BandWave:
        '''
        Creates the backend BandWave object for the values entered into the UI

        Returns
        -------
        bandwave: BandWave
            the BandWave object for the entries into this UI
        '''
        start_high_freq = self.start_high_var.get()
        end_high_freq = self.end_high_var.get()
        start_low_freq = self.start_low_var.get()
        end_low_freq = self.end_low_var.get()
        amplitude = self.amp_var.get()/100
        sweep_period = self.time_var.get()
        fps = self.FR_var.get()
        bandwave = BandWave(start_high_freq, start_low_freq, end_high_freq, end_low_freq, amplitude, sweep_period, fps)
        return bandwave

    def remove_widgets(self)->None:
        '''
        Function to remove the tkinter widgets from view, used when deleting a wave
        '''
        self.amp_input.grid_forget()
        self.start_frame.grid_forget()
        self.end_frame.grid_forget()
        self.time_input.grid_forget()
        self.label_frame.grid_forget()
        self.FR_input.grid_forget()

    def update_index(self, index)->None:
        '''
        Updates the index and shows the tkinter widgets at the new index after a wave has been deleted

        Parameters
        ----------
        index: int
            New index for the wave
        '''
        self.index = index

        self.amp_input.grid(column=1, row=index, sticky='nsew')
        self.label_frame.grid(column=2, row=index, sticky='nsew')
        self.start_frame.grid(column=3, row=index, sticky='nsew')
        self.end_frame.grid(column=4, row=index, sticky='nsew')
        self.time_input.grid(column=5, row=index, sticky='nsew')
        self.FR_input.grid(column=6, row=index, sticky='nsew')