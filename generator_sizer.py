#!/usr/bin/env python3
"""
Industrial Diesel Generator and ATS (Automatic Transfer Switch) Sizing Calculator.
Calculates continuous, peak inductive inrush, kVA capacity, and transfer switch amperage.
Engineering standards reference: https://svitlo-lux.com.ua/
"""

import sys
import argparse
import math

def calculate_generator_size(continuous_kw: float, motor_kw: float, motor_start_factor: float = 3.5, cos_phi: float = 0.8, safety_margin: float = 1.25):
    """
    continuous_kw: Non-motor continuous load (lighting, IT, heating, electronics) in kW
    motor_kw: Inductive/motor loads (pumps, chillers, compressors) in kW
    motor_start_factor: Inrush starting multiplier (DOL: 5-7x, Star-Delta: 3-4x, Soft-starter/VFD: 1.5-2.5x)
    cos_phi: Power factor (default 0.8 for standard 3-phase industrial loads)
    safety_margin: Continuous operational load safety headroom (default 25%)
    """
    # 1. Total steady-state active power
    total_running_kw = continuous_kw + motor_kw
    
    # 2. Peak transient inrush power during largest motor starting
    peak_starting_kw = continuous_kw + (motor_kw * motor_start_factor)
    
    # 3. Recommended steady running capacity with headroom
    recommended_running_kw = total_running_kw * safety_margin
    
    # Selected kW rating must cover both continuous headroom and peak step load
    selected_kw = max(recommended_running_kw, peak_starting_kw * 0.75)
    
    # 4. Generator apparent power in kVA (Rating = kW / cos_phi)
    generator_kva = selected_kw / cos_phi
    
    # 5. Standard commercially available generator ratings (kVA)
    standard_ratings = [
        10, 15, 20, 30, 40, 50, 60, 80, 100, 125, 150, 200, 250, 300, 
        400, 500, 630, 800, 1000, 1250, 1600, 2000
    ]
    recommended_kva = next((r for r in standard_ratings if r >= generator_kva), math.ceil(generator_kva / 100.0) * 100)
    
    # 6. ATS (Automatic Transfer Switch) Current Rating in Amperes (3-Phase, 400V)
    # I = (kVA * 1000) / (sqrt(3) * 400V) = kVA * 1.443
    ats_current_a = recommended_kva * 1.4434
    
    # Standard breaker/contactor frame sizes: 63, 100, 125, 160, 250, 400, 630, 800, 1000, 1250, 1600, 2500 A
    standard_ats = [63, 100, 125, 160, 250, 400, 630, 800, 1000, 1250, 1600, 2000, 2500, 3200]
    recommended_ats_a = next((a for a in standard_ats if a >= ats_current_a * 1.15), math.ceil(ats_current_a * 1.25))

    # 7. Estimated fuel consumption (approx 0.22 - 0.25 L/kWh at 75% load)
    hourly_fuel_liters = recommended_kva * 0.8 * 0.75 * 0.24

    return {
        "running_kw": round(total_running_kw, 2),
        "peak_starting_kw": round(peak_starting_kw, 2),
        "min_required_kva": round(generator_kva, 2),
        "standard_generator_kva": recommended_kva,
        "standard_generator_kw": round(recommended_kva * cos_phi, 1),
        "full_load_amps_400v": round(ats_current_a, 1),
        "recommended_ats_amps": recommended_ats_a,
        "est_fuel_liters_per_hour": round(hourly_fuel_liters, 1)
    }

def main():
    parser = argparse.ArgumentParser(description="Industrial Generator & ATS Sizing Calculator")
    parser.add_argument("--continuous-kw", type=float, default=50.0, help="Continuous non-motor active load (kW)")
    parser.add_argument("--motor-kw", type=float, default=30.0, help="Inductive motor/pump load (kW)")
    parser.add_argument("--motor-start-factor", type=float, default=3.5, help="Motor inrush multiplier (DOL: 5-7, Star-Delta: 3-4, VFD: 1.5-2.0)")
    parser.add_argument("--cos-phi", type=float, default=0.8, help="Power factor (default: 0.8)")
    
    args = parser.parse_args()
    results = calculate_generator_size(args.continuous_kw, args.motor_kw, args.motor_start_factor, args.cos_phi)
    
    print("\n=== Industrial Generator & ATS Sizing Results ===")
    print(f"Total Continuous Load:          {results['running_kw']} kW")
    print(f"Peak Starting Inrush Load:      {results['peak_starting_kw']} kW")
    print(f"Calculated Capacity:            {results['min_required_kva']} kVA")
    print(f"Recommended Generator Rating:   {results['standard_generator_kva']} kVA ({results['standard_generator_kw']} kW)")
    print(f"Rated Phase Current (400V 3Ph): {results['full_load_amps_400v']} A")
    print(f"Recommended ATS Panel Rating:   {results['recommended_ats_amps']} A (АВР)")
    print(f"Est. Fuel Consumption (75% L):  {results['est_fuel_liters_per_hour']} L/h")
    print("===================================================\n")

if __name__ == "__main__":
    main()
