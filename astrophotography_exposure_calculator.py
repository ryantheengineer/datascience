import numpy as np
from scipy.optimize import fsolve


# Improvements to add:
    # Plotting exposures needed by single exposure time
    # Plotting total exposure needed by object magnitude, with labels of specific objects for reference
    # 


def bortle_to_sky_brightness(bortle):
    """Approximate sky brightness (mag/arcsec^2) from Bortle scale."""
    bortle_map = {
        1: 21.99, 2: 21.89, 3: 21.69, 4: 21.39, 5: 20.99,
        6: 19.99, 7: 18.94, 8: 18.38, 9: 17.99
    }
    return bortle_map.get(bortle, 20.99)  # Default to Bortle 5 if unknown

def exposure_time(magnitude, aperture, f_ratio, pixel_size, quantum_efficiency, 
                   read_noise, dark_current, bortle, single_exposure_snr, final_snr):
    """Compute the required single exposure time for given astrophotography parameters."""
    # Constants
    zero_magnitude_flux = 1.5e6  # photons/s/m^2 (approximate for V-band)
    aperture_area = np.pi * (aperture / 2) ** 2  # in m^2
    
    # Target flux in photons per second
    flux_object = zero_magnitude_flux * 10**(-0.4 * magnitude)
    collected_photons_per_sec = flux_object * aperture_area * quantum_efficiency
    
    # Pixel scale (arcsec/pixel)
    pixel_scale = 206.265 * pixel_size / (f_ratio * aperture)
    sky_brightness_mag = bortle_to_sky_brightness(bortle)
    sky_flux = zero_magnitude_flux * 10**(-0.4 * sky_brightness_mag)
    
    # Sky background photons per second per pixel
    sky_photons_per_sec = sky_flux * aperture_area * quantum_efficiency * (pixel_scale**2)
    
    # Define equation to solve for exposure time t
    def snr_equation(t):
        signal = collected_photons_per_sec * t
        noise = np.sqrt(signal + (sky_photons_per_sec * t) + read_noise**2 + (dark_current * t))
        return signal / noise - single_exposure_snr
    
    # Solve for exposure time
    t_solution = fsolve(snr_equation, 10)[0]  # Initial guess: 10 seconds
    return max(t_solution, 1)  # Ensure at least 1s exposure

def total_exposure_time(single_exposure_time, final_snr, single_exposure_snr):
    """Compute the total exposure time and number of exposures needed to reach final SNR."""
    num_exposures = (final_snr / single_exposure_snr) ** 2
    total_time = num_exposures * single_exposure_time
    return total_time, int(np.ceil(num_exposures))

def get_single_exposure_snr(magnitude, aperture, f_ratio, pixel_size, quantum_efficiency, 
                   read_noise, dark_current, bortle, single_exposure_time, final_snr):
    # Constants
    zero_magnitude_flux = 1.5e6  # photons/s/m^2 (approximate for V-band)
    aperture_area = np.pi * (aperture / 2) ** 2  # in m^2
    
    # Target flux in photons per second
    flux_object = zero_magnitude_flux * 10**(-0.4 * magnitude)
    collected_photons_per_sec = flux_object * aperture_area * quantum_efficiency
    
    # Pixel scale (arcsec/pixel)
    pixel_scale = 206.265 * pixel_size / (f_ratio * aperture)
    sky_brightness_mag = bortle_to_sky_brightness(bortle)
    sky_flux = zero_magnitude_flux * 10**(-0.4 * sky_brightness_mag)
    
    # Sky background photons per second per pixel
    sky_photons_per_sec = sky_flux * aperture_area * quantum_efficiency * (pixel_scale**2)
    
    # Define equation to solve for exposure time t
    def snr_equation(t):
        signal = collected_photons_per_sec * t
        noise = np.sqrt(signal + (sky_photons_per_sec * t) + read_noise**2 + (dark_current * t))
        return signal / noise
    
    return snr_equation(single_exposure_time)

# Example usage
params1 = {
    "magnitude": 9.6,  # Target magnitude (whirlpool galaxy is 9.3 photographic magnitude, Bode's is 7.9)
    "aperture": 0.15,  # Telescope aperture in meters (200mm)
    "f_ratio": 10,  # Focal ratio
    "pixel_size": 4.3,  # Pixel size in microns
    "quantum_efficiency": 0.8,  # QE (fraction)
    "read_noise": 5,  # Read noise in electrons
    "dark_current": 0.02,  # Dark current in electrons/sec
    "bortle": 4,  # Bortle scale rating (Payson home is Bortle 4, cabin is Bortle 2)
    "single_exposure_snr": 10,  # Desired SNR for a single exposure
    "final_snr": 50  # Target final SNR after stacking
}

single_exposure = exposure_time(**params1)
total_time, num_exposures = total_exposure_time(single_exposure, params1["final_snr"], params1["single_exposure_snr"])

print(f"Desired single exposure SNR: {params1['single_exposure_snr']}")
print(f"Estimated single exposure time: {single_exposure/60:.2f} minutes")
print(f"Total required exposure time: {total_time/60:.2f} minutes")
print(f"Number of exposures needed for stacked image SNR {params1['final_snr']}: {num_exposures}")


params2 = {
    "magnitude": params1["magnitude"],  # Target magnitude
    "aperture": params1["aperture"],  # Telescope aperture in meters (200mm)
    "f_ratio": params1["f_ratio"],  # Focal ratio
    "pixel_size": params1["pixel_size"],  # Pixel size in microns
    "quantum_efficiency": params1["quantum_efficiency"],  # QE (fraction)
    "read_noise": params1["read_noise"],  # Read noise in electrons
    "dark_current": params1["dark_current"],  # Dark current in electrons/sec
    "bortle": params1["bortle"],  # Bortle scale rating
    "single_exposure_time": 180.0,  # Desired SNR for a single exposure
    "final_snr": 50  # Target final SNR after stacking
}

single_exposure_snr = get_single_exposure_snr(**params2)
total_time, num_exposures = total_exposure_time(params2["single_exposure_time"], params2["final_snr"], single_exposure_snr)

print(f"\nSingle exposure time: {params2['single_exposure_time']}")
print(f"Single exposure SNR: {single_exposure_snr}")
print(f"Number of exposures needed: {num_exposures} ({total_time/360:.2f} hours)")

