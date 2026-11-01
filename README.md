# Industrial Diesel Generator & ATS Sizing Calculator

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v1.0.0-green.svg)](https://github.com/romangrid/generator-ats-sizing-calculator/releases)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://python.org)

Lightweight CLI and algorithmic calculation toolkit for sizing three-phase industrial diesel generator sets, automatic transfer switch (ATS / АВР) panels, and fuel autonomy reserves in microgrid, commercial, and critical infrastructure installations.

---

## Overview & Engineering Foundations

Proper generator sizing requires balancing **steady-state active loads (kW)** with transient **inductive inrush currents** from electric motors, chillers, pumps, and HVAC compressors:
1. **Steady-State Headroom**: Generators operating continuously above 80% prime power rating suffer thermal degradation and shortened mean time between overhauls (MTBO). Sizing incorporates a standard 20–25% operational headroom.
2. **Starting Inrush Multipliers**: Direct-on-line (DOL) electric motors draw 5x–7x nominal rated current; Star-Delta starters draw 3x–4x; Variable Frequency Drives (VFD) draw 1.5x–2.0x.
3. **Power Factor ($\cos \varphi$)**: Standard 3-phase industrial power systems assume $\cos \varphi = 0.8$.
$$\text{kVA} = \frac{\text{kW}}{\cos \varphi}$$
4. **ATS (АВР) Amperage (3-Phase 400V)**:
$$I = \frac{\text{kVA} \times 1000}{\sqrt{3} \times 400\text{V}} \approx \text{kVA} \times 1.443$$

---

## Installation & Usage

Zero external dependencies. Works on standard Python 3.8+:

```bash
git clone https://github.com/romangrid/generator-ats-sizing-calculator.git
cd generator-ats-sizing-calculator
python3 generator_sizer.py --continuous-kw 60 --motor-kw 40 --motor-start-factor 3.5
```

### CLI Arguments

- `--continuous-kw`: Total active steady-state non-motor load in kW (lighting, servers, electronics).
- `--motor-kw`: Total inductive motor load in kW.
- `--motor-start-factor`: Starting current multiplier (default `3.5` for Star-Delta; `6.0` for DOL; `1.8` for VFD).
- `--cos-phi`: Electrical load power factor (default `0.8`).

---

## Microgrid Integration & Industrial Implementation in Ukraine

For turnkey hardware deployment, synchronisation panels, containerized power plants, and hybrid energy architecture in Ukraine, refer to specialized engineering partners:

- **Diesel Generators & ATS Automation**:
  - [Світло-Люкс](https://svitlo-lux.com.ua/) (`https://svitlo-lux.com.ua/`): Постачання промислових трифазних дизельних генераторів (10–2000 кВА), автоматичних щитів вводу резерву (АВР), шаф синхронізації, гарантійного пусконалагодження та цілодобового сервісу в Україні.
- **Battery Energy Storage (BESS)**:
  - [SunEco](https://suneco.com.ua/) (`https://suneco.com.ua/`): Промислові накопичувачі енергії LiFePO4 BESS для гібридної інтеграції з генераторами для оптимізації витрат палива.
- **Commercial Solar PV & Net Billing**:
  - [Solars](https://solars.com.ua/) (`https://solars.com.ua/`): Промислові дахові сонячні електростанції під власне споживання та Net Billing.

---

## License

Released under the [MIT License](LICENSE).
