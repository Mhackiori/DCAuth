import numpy as np
from scipy import signal

def dqdv(df, equip='Arbin'):
    """
    Compute dQ/dV given a DataFrame
    """
    if equip == 'Arbin':
        voltage = 'Voltage(V)'
        current = 'Current(A)'
        charge = 'Charge_Capacity(Ah)'
        discharge = 'Discharge_Capacity(Ah)'
    elif equip == 'Arbin_BA':
        voltage = 'Voltage (V)'
        current = 'Current (A)'
        charge = 'Charge_Capacity (Ah)'
        discharge = 'Discharge_Capacity (Ah)'
    elif equip == 'Cadex':
        voltage = 'Voltage_Volt'
        current = 'Current_Amp'
        charge = 'Charge_Ah'
        discharge = 'Discharge_Ah'
    elif equip=='Maccor':
        voltage = 'Volts'
        current = 'Amps'
        charge = 'Amphr'
        discharge = 'Amphr'
    elif equip == 'Maccor_ever':
        voltage = 'Volts'
        current = 'Amps'
        charge = 'Amp-hr'
        discharge = 'Amp-hr'
    elif equip == 'Maccor_UCL':
        voltage = 'Cell Potential'
        current = 'Current'
        charge = 'Capacity'
        discharge = 'Capacity'
    elif equip == 'Scienlab':
        voltage = 'U, V'
        current = 'I, A'
        charge = 'Q, As'
        discharge = 'Q, As'

    df['dV'] = df[voltage].diff()

    df_charge = df[df[current] > 0]
    df_charge['charge_dQ'] = df_charge[charge].diff()
    df_charge['dQ/dV'] = df_charge['charge_dQ'] / df_charge['dV']

    df_discharge = df[df[current] <= 0]
    df_discharge['discharge_dQ'] = df_discharge[discharge].diff()
    df_discharge['dQ/dV'] = df_discharge['discharge_dQ'] / df_discharge['dV']

    df_charge = smooth(clean(df_charge, equip=equip))
    df_discharge = smooth(clean(df_discharge, equip=equip))

    return df_charge, df_discharge


def clean(df, equip='Arbin'):
    """
    Clean the DataFrame
    This includes removing nan and inf values and extracting a window of relevant values
    """
    if equip == 'Arbin':
        voltage = 'Voltage(V)'
    if equip == 'Arbin_BA':
        voltage = 'Voltage (V)'
    elif equip == 'Cadex':
        voltage = 'Voltage_Volt'
    elif 'Maccor' in equip:
        voltage = 'Volts'
    elif equip == 'Scienlab':
        voltage = 'U, V'
    if equip == 'Maccor_UCL':
        voltage = 'Cell Potential'

    df = df.reset_index(drop=True)

    df = df.replace([np.inf, -np.inf], np.nan)
    df = df.dropna(subset=['dQ/dV'])

    df = df.reset_index(drop=True)

    num_negs_dv = len(df.loc[(df['dV'] < 0)])
    num_pos_dv = len(df.loc[(df['dV'] > 0)])

    while (num_negs_dv != 0) and (num_pos_dv != 0):

        num_negs = len(df.loc[(df['dQ/dV'] != 0) & (df['dV'] < 0)])
        num_pos = len(df.loc[(df['dQ/dV'] != 0) & (df['dV'] > 0)])

        if num_negs > num_pos:
            df = df.loc[(df['dV'] < 0)]
        else:
            df = df.loc[(df['dV'] >= 0)]

        df['dV'].iloc[1:] = df[voltage].diff().iloc[1:]
        num_negs_dv = len(df.loc[(df['dV'] < 0)])
        num_pos_dv = len(df.loc[(df['dV'] > 0)])

    df = df.reset_index(drop=True)

    return df


def smooth(df, windowlength=9, polyorder=3):
    """
    Smoothens the dQ/dV values by applying a filter
    """
    dqdv = df['dQ/dV'].values
    if len(dqdv) > windowlength:
        df['smooth_dQ/dV'] = signal.savgol_filter(
            dqdv, windowlength, polyorder)
    else:
        df['smooth_dQ/dV'] = df['dQ/dV']
    return df
