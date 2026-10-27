"""Configuration constants and metadata for SafeCrime analytics library."""

CRIME_COLS = ['Rape', 'K&A', 'DD', 'AoW', 'AoM', 'DV', 'WT']

CRIME_LABELS = {
    'Rape': 'Rape (Sec. 376 IPC)',
    'K&A': 'Kidnapping & Abduction (Sec. 363-373 IPC)',
    'DD': 'Dowry Deaths (Sec. 304B IPC)',
    'AoW': 'Assault on Women / Molestation (Sec. 354 IPC)',
    'AoM': 'Insult to Modesty / Eve Teasing (Sec. 509 IPC)',
    'DV': 'Domestic Violence / Cruelty (Sec. 498A IPC)',
    'WT': 'Women Trafficking / Immoral Traffic'
}

# Crime severity weights based on Indian Penal Code offense severity & bodily harm
DEFAULT_SEVERITY_WEIGHTS = {
    'Rape': 0.28,
    'DD': 0.24,
    'AoW': 0.16,
    'K&A': 0.16,
    'DV': 0.12,
    'WT': 0.03,
    'AoM': 0.01
}

STATE_NORMALIZATION_MAP = {
    'A & N': 'Andaman & Nicobar',
    'A And N': 'Andaman & Nicobar',
    'Andaman': 'Andaman & Nicobar',
    'D & N': 'Dadra & Nagar Haveli',
    'D&N': 'Dadra & Nagar Haveli',
    'Dadra': 'Dadra & Nagar Haveli',
    'Daman': 'Daman & Diu',
    'Delhi': 'Delhi',
    'Keralal': 'Kerala'
}

HISTORICAL_ANOMALIES = {
    2013: "Post-Nirbhaya Criminal Law Amendment effect (+27.0% YoY reporting surge; unprecedented rise across Rape & Molestation).",
    2020: "COVID-19 National Lockdown suppression (-9.5% dip; severe mobility restrictions hampered formal FIR registrations).",
    2011: "NCRB Scraped Data Anomaly: Assault on Women (AoW) recorded as 0 nationwide in raw scrape.",
    2021: "Post-Pandemic Rebound: Pent-up reporting wave surging +15.2% YoY to historic high of 348,092 cases."
}

CLUSTER_TIER_META = {
    0: {
        "tier": "Tier 1: Critical Hotspot",
        "risk": "Critical",
        "color": "#EF4444",
        "desc": "Extreme volumes across Rape, Assault, and Domestic Violence. Urgent policing intervention required."
    },
    1: {
        "tier": "Tier 2: Severe Domestic Abuse",
        "risk": "High",
        "color": "#F59E0B",
        "desc": "High concentration of Domestic Violence (Sec. 498A) and Kidnapping."
    },
    2: {
        "tier": "Tier 3: Moderate Risk Zone",
        "risk": "Moderate",
        "color": "#3B82F6",
        "desc": "Moderate incidence rates; localized crime prevalence."
    },
    3: {
        "tier": "Tier 4: Safe Havens / Low Reports",
        "risk": "Low",
        "color": "#10B981",
        "desc": "Consistently lowest reported incident volumes across two decades."
    }
}
