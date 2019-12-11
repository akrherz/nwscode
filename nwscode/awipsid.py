#!/usr/bin/env python
# encoding: utf-8
"""
A parser for the *AWIPS Identifier*.

Created by Alexander Ross on 2006-08-01.
Copyright (c) 2006 NOAA's National Weather Service. All rights reserved.
"""

__all__ = ["AwipsIdError", "AwipsId"]

import re
from nwscode import NwsCode, NwsCodeError
from misc import Bunch

CATEGORY = r"[A-Z0-9]{3}"
DESIGNATOR = r"[A-Z ]{3}"
AWIPSID = r"^(%s)(%s)$" % (CATEGORY, DESIGNATOR)

class AwipsIdError(NwsCodeError):
    pass

class AwipsId(NwsCode):
    """
    A parser for the *AWIPS Identifier*.
    
    Initialize this object with a AWIPS Identifier string. For a full
    description of the AWIPS Identifier see:
    
        http://www.weather.gov/tg/awips.html
    
    Attributes:
        
        ``raw``
            The raw AWIPS Identifier string.
        
        ``category``
            The product category.
        
        ``designator``
            The product designator.
        
        ``code``
            This attribute exposes the the individual unprocessed
            code groups.  Use this attribute to access portions of the 
            AWIPS Identifier string.
    
    Usage Example:
    
    >>> from nwscode.awipsid import AwipsId
    >>> a = AwipsId("ZFPAFG")
    >>> assert a.raw == "ZFPAFG"
    >>> assert a.category == "ZONE FORECAST PRODUCT"
    >>> assert a.designator == "AFG"
    >>> assert a.code.category == "ZFP"
    >>> assert a.code.designator == "AFG"
    """
    pattern = re.compile(AWIPSID)
    error = AwipsIdError
    interpreted = {
        "category":
            {"18A": "18 HOUR WINTEM",
             "24A": "24 HOUR WINTEM",
             "30L": "AVERAGE MONTHLY WEATHER OUTLOOK (LOCAL)",
             "3HR": "ROUTINE SPACE ENVIRONMENT PRODUCT ISSUED EVERY 3 HOURS",
             "5TC": "500 MILLIBAR TYPE CORRELATION",
             "ABV": "RAWINSONDE DATA ABOVE 100 MILLIBARS *",
             "ADA": "ALARM/ALERT ADMINISTRATIVE MSG (URGENT NOTIFICATION)",
             "ADM": "ALERT ADMINISTRATIVE MESSAGE",
             "ADR": "NWS ADMINISTRATIVE MESSAGE (EXTERNAL)",
             "ADV": "GENERIC SPACE ENVIRONMENT ADVISORY",
             "ADW": "ADMINISTRATIVE MESSAGE FOR NWWS",
             "ADX": "ADMIN ALERT FOR NON-RECEIPT OF TRANSMISSION",
             "AFD": "AREA FORECAST DISCUSSION",
             "AFM": "AREA FORECAST MATRICES",
             "AFP": "AREA FORECAST PRODUCT",
             "AGF": "AGRICULTURAL FORECAST",
             "AGO": "AGRICULTURAL OBSERVATIONS",
             "APG": "AIR STAGNATION GUIDANCE NARRATIVE",
             "ALM": "SPACE ENVIRONMENT ALARM",
             "ALT": "SPACE ENVIRONMENT ALERT",
             "AQI": "AIR QUALITY INDEX STATEMENT",
             "ARP": "AIREPS *",
             "ASA": "AIR STAGNATION ADVISORY",
             "AVA": "AVALANCHE WATCH",
             "AVM": "AVIATION VERIFICATION MATRIX",
             "AVW": "AVALANCHE WARNING",
             "AWG": "NATIONAL ATTACK WARNING",
             "AWS": "AREA WEATHER SUMMARY",
             "AWU": "AREA WEATHER UPDATE",
             "AWW": "AVIATION WEATHER WARNING",
             "BOY": "BUOY REPORTS - SYNOPTIC AND NON SYNOPTIC TIMES",
             "CAE": "CHILD ABDUCTION EMERGENCY",
             "CCF": "CODED CITY FORECAST",
             "CDW": "CIVIL DANGER WARNING",
             "CEM": "CIVIL EMERGENCY MESSAGE",
             "CF6": "WFO DAILY CLIMATE WEB PAGE MESSAGES ",
             "CFP": "CONVECTIVE FORECAST PRODUCT",
             "CFW": "COASTAL FLOOD WARNINGS, WATCHES OR STATEMENTS",
             "CGR": "COAST GUARD SURFACE REPORT",
             "CHG": "COMPUTER HURRICANE GUIDANCE",
             "CLI": "CLIMATOLOGICAL REPORT (DAILY)",
             "CLM": "CLIMATOLOGICAL REPORT (MISC, INC MONTHLY REPORTS)",
             "CMM": "CODED CLIMATOLOGICAL MONTHLY MEANS",
             "COD": "CODED ANALYSIS AND FORECASTS",
             "CRF": "CONTINGENCY RIVER FORECAST",
             "CSC": "CANADIAN SELECTED CITIES FORECAST (FPCN12 CWAO)",
             "CUR": "ROUTINE SPACE ENVIRONMENT PRODUCTS ISSUED "\
                    "FOR CURRENT DATA",
             "CWA": "CENTER (CWSU) WEATHER ADVISORY",
             "CWF": "COASTAL WATERS FORECAST",
             "CWS": "CENTER (CWSU) WEATHER STATEMENT",
             "DAY": "ROUTINE SPACE ENVIRONMENT PRODUCT ISSUED DAILY",
             "DHR": "DIGITAL HYBRID REFLECTIVITY 32/DHR",
             "DPA": "RADAR HOURLY DIGITAL PRECIPITATION ARRAY 81/DPA",
             "DSA": "UNNUMBERED DEPRESSION / SUSPICIOUS AREA ADVISORY",
             "DSM": "ASOS DAILY SUMMARY",
             "DST": "ASOS DAILY SUMMARY TEST",
             "EFP": "3 TO 5 DAY EXTENDED FORECAST",
             "EOL": "AVERAGE 6 TO 10 DAY WEATHER OUTLOOK (LOCAL)",
             "EON": "AVERAGE 6 TO 10 DAY WEATHER OUTLOOK (NATIONAL)",
             "EQR": "EARTHQUAKE REPORT",
             "EQW": "EARTHQUAKE WARNING",
             "ESF": "FLOOD POTENTIAL OUTLOOK",
             "ESG": "EXTENDED STREAMFLOW GUIDANCE",
             "ESP": "EXTENDED STREAMFLOW PREDICTION",
             "ESS": "WATER SUPPLY OUTLOOK",
             "EVI": "EVACUATION IMMEDIATE",
             "FA0": "AVIATION AREA FORECAST (PACIFIC)",
             "FA1": "AVIATION AREA FORECAST (NORTHEAST U.S.)",
             "FA2": "AVIATION AREA FORECAST (SOUTHEAST U.S.)",
             "FA3": "AVIATION AREA FORECAST (NORTH CENTRAL U.S.)",
             "FA4": "AVIATION AREA FORECAST (SOUTH CENTRAL U.S.)",
             "FA5": "AVIATION AREA FORECAST (U.S. ROCKY MOUNTAINS)",
             "FA6": "AVIATION AREA FORECAST (U.S. WEST COAST)",
             "FA7": "AVIATION AREA FORECAST (JUNEAU, ALASKA)",
             "FA8": "AVIATION AREA FORECAST (ANCHORAGE, ALASKA)",
             "FA9": "AVIATION AREA FORECAST (FAIRBANKS, ALASKA)",
             "FAK": "ALASKAN MODEL OUTPUT STATISTICS (MOS) FORECAST",
             "FAN": "AVN BASED MOS GUIDANCE",
             "FAV": "AVIATION AREA FORECAST (FOR INTERNATIONALS ONLY)",
             "FBP": "AK FOUS 24,36,& 48-HR BOUNDARY LYR WINDS & PRECIP",
             "FD0": "24 HR FD WINDS ALOFT FCST (45,000 AND 53,000 FT)",
             "FD1": "6 HOUR WINDS ALOFT FORECAST",
             "FD2": "12 HOUR WINDS ALOFT FORECAST",
             "FD3": "24 HOUR WINDS ALOFT FORECAST",
             "FD8": "6 HOUR FD WINDS ALOFT FCST (45,000 AND 53,000 FT)",
             "FD9": "12 HR FD WINDS ALOFT FCST (45,000 AND 53,000 FT)",
             "FDI": "FIRE DANGER INDICES",
             "FFA": "FLASH FLOOD WATCH",
             "FFG": "FLASH FLOOD GUIDANCE",
             "FFH": "HEADWATER GUIDANCE",
             "FFS": "FLASH FLOOD STATEMENT",
             "FFW": "FLASH FLOOD WARNING",
             "FLN": "NATIONAL FLOOD SUMMARY",
             "FLS": "FLOOD STATEMENT",
             "FLW": "FLOOD WARNING",
             "FMR": "FORECAST MEDIUM RANGE GUIDANCE",
             "FOF": "UPPER WIND FALLOUT FORECAST",
             "FOH": "ETA FOUS FREEZING AND RELATIVE HUMIDITY",
             "FRH": "FOUS RELATIVE HUMIDITY/TEMPERATURE GUIDANCE",
             "FRW": "FIRE WARNING",
             "FSH": "NATIONAL MARINE FISHERIES ADMINISTRATIVE SERVICE MESSAGE",
             "FSS": "URBAN AND SMALL STREAM FLOOD ADVISORY",
             "FTJ": "FOUS TRAJECTORY FORECAST",
             "FTM": "WSR-88D RADAR OUTAGE NOTIFICATION / FREE TEXT MESSAGE",
             "FTP": "FOUS PROG MAX/MIN TEMP/POP GUIDANCE",
             "FWA": "FIRE WEATHER ADMINISTRATIVE MESSAGE",
             "FWC": "FOUS WIND/CLOUD GUIDANCE",
             "FWD": "FIRE WEATHER OUTLOOK DISCUSSION",
             "FWE": "EXTENDED FIRE WEATHER OUTLOOK",
             "FWF": "ROUTINE FIRE WX FCST(WITH/WITHOUT 6-10 DAY OUTLOOK)",
             "FWL": "LAND MANAGEMENT FORECASTS",
             "FWM": "MISCELLANEOUS FIRE WEATHER PRODUCT",
             "FWN": "FIRE WEATHER NOTIFICATION",
             "FWO": "FIRE WEATHER OBSERVATION",
             "FWS": "SUPPRESSION FORECAST",
             "FWW": "FIRE WEATHER WATCH",
             "FZL": "FREEZING LEVEL DATA (RADAT)",
             "GLF": "GREAT LAKES FORECAST",
             "GLO": "GREAT LAKES STORM OUTLOOK",
             "GLS": "GREAT LAKES STORM SUMMARY",
             "GSM": "GENERAL STATUS MESSAGE ",
             "HCM": "HYDROMETEORLOGICAL COORDINATION MESSAGE",
             "HD1": "RFC DERIVED QPF DATA PRODUCT",
             "HD2": "RFC DERIVED QPF DATA PRODUCT",
             "HD3": "RFC DERIVED QPF DATA PRODUCT",
             "HD4": "RFC DERIVED QPF DATA PRODUCT",
             "HD5": "RFC DERIVED QPF DATA PRODUCT",
             "HD6": "RFC DERIVED QPF DATA PRODUCT",
             "HD7": "RFC DERIVED QPF DATA PRODUCT",
             "HD8": "RFC DERIVED QPF DATA PRODUCT",
             "HD9": "RFC DERIVED QPF DATA PRODUCT",
             "HDP": "WSR-88D HOURLY DIGITAL PRECIPITATION ARRAY",
             "HLS": "HURRICANE LOCAL STATEMENT",
             "HMD": "HYDROMETEOROLOGICAL DISCUSSION",
             "HMW": "HAZARDOUS MATERIALS WARNING",
             "HP1": "RFC QPF VERIFICATION PRODUCT",
             "HP2": "RFC QPF VERIFICATION PRODUCT",
             "HP3": "RFC QPF VERIFICATION PRODUCT",
             "HP4": "RFC QPF VERIFICATION PRODUCT",
             "HP5": "RFC QPF VERIFICATION PRODUCT",
             "HP6": "RFC QPF VERIFICATION PRODUCT",
             "HP7": "RFC QPF VERIFICATION PRODUCT",
             "HP8": "RFC QPF VERIFICATION PRODUCT",
             "HP9": "RFC QPF VERIFICATION PRODUCT",
             "HSF": "HIGH SEAS FORECAST",
             "HWO": "HAZARDOUS WEATHER OUTLOOK",
             "HYD": "DAILY HYDROMETEOROLOGICAL PRODUCTS",
             "HYM": "MONTHLY HYDROMETEOROLOGICAL PLAIN LANGUAGE PRODUCT    ",
             "HYW": "WEEKLY HYDROMETEOROLOGICAL PLAIN LANGUAGE PRODUCT    ",
             "ICE": "ICE FORECAST",
             "INI": "ADMINISTR [NOUS51 KWBC]",
             "IOB": "ICE OBSERVATION",
             "IRM": "INTERIM RADAR MESSAGE 83/IRM  ",
             "KPA": "KEEP ALIVE MESSAGE",
             "LAE": "LOCAL AREA EMERGENCY",
             "LAW": "GREAT LAKES WEATHER OBSERVATION (SHIP SYNOP CODE)",
             "LCO": "LOCAL COOPERATIVE OBSERVATION",
             "LEW": "LAW ENFORCEMENT WARNING",
             "LFP": "LOCAL FORECAST",
             "LLS": "LOW-LEVEL SOUNDING",
             "LSH": "LAKESHORE WARNING OR STATEMENT",
             "LSR": "LOCAL STORM REPORT",
             "LTG": "LIGHTNING DATA ",
             "MAN": "RAWINSONDE OBSERVATION MANDATORY LEVELS *",
             "MAP": "MEAN AREAL PRECIPITATION",
             "MAV": "MOS AVIATION-BASED GUIDANCE FROM AVN MODEL",
             "MAW": "AMENDED MARINE FORECAST",
             "MEF": "AFOS FORECAST VERIFICATION MATRIX",
             "MET": "ETA-BASED MOS ALPHANUMERIC MESSAGE",
             "MEX": "MOS EXTENDED-RANGE GUIDANCE FROM MRF MODEL",
             "MIM": "MARINE INTERPRETATION MESSAGE",
             "MIS": "MISCELLANEOUS LOCAL PRODUCT",
             "MON": "ROUTINE SPACE ENVIRONMENT PRODUCT ISSUED MONTHLY",
             "MRM": "MISSING RADAR MESSAGE (WSR-88D)",
             "MRP": "TECHNIQUES DEVELOPMENT LABORATORY MARINE PRODUCT",
             "MSM": "ASOS MONTHLY SUMMARY MESSAGE",
             "MST": "ASOS MONTHLY SUMMARY MESSAGE TEST",
             "MTR": "METAR FORMATTED SURFACE WEATHER OBSERVATION *",
             "MTT": "METAR TEST MESSAGE (ASOS) *",
             "MVF": "MARINE VERIFICATION CODED FORECAST",
             "MWS": "MARINE WEATHER STATEMENT",
             "N0R": "RADAR .5 REFLECTIVITY .54NM RES 16 LEVELS ID 19/R",
             "N0S": "RADAR .5 STORM REL. VELOCITY .54NM RES 16 LVLS ID 56/SRM",
             "N0V": "RADAR .5 VELOCITY .54NM RES 16 LEVELS ID 27/V",
             "N0W": "RADAR BASE RADIAL VELOCITY 25/V",
             "N0Z": "RADAR .5 REFLECTIVITY 1.1NM RES 16 LEVELS ID 20/R",
             "N1P": "RADAR 1 HOUR PRECIPITATION ACCUMULATION 78/OHP",
             "N1R": "RADAR 1.5 REFLECTIVITY .54NM RES 16 LEVELS ID 19/R",
             "N1S": "RADAR 1.5 STORM REL. VELOCITY .54NM RES 16 LVLS ID 56/SRM",
             "N1V": "RADAR 1.5 VELOCITY .54NM RES 16 LEVELS ID 27/V",
             "N2R": "RADAR 2.4/2.5 REFLECTIVITY .54NM RES 16 LEVELS ID 19/R",
             "N2S": "RADAR 2.4/2.5 STORM REL VLCTY .54NM RES 16 LVLS ID 56/SRM",
             "N2V": "RADAR 2.4/2.5 VELOCITY .54NM RES 16 LEVELS ID 27/V",
             "N3P": "RADAR 3 HOUR PRECIPITATION ACCUMULATION 79/THP",
             "N3R": "RADAR 3.4/3.5 REFLECTIVITY .54NM RES 16 LEVELS ID 19/R",
             "N3S": "RADAR 3.4/3.5 STORM REL VLCTY .54NM RES 16 LVLS ID 56/SRM",
             "N3V": "RADAR 3.4/3.5 VELOCITY .54NM RES 16 LEVELS ID 27/V",
             "N6P": "USER SELECTABLE PRECIPITATION 6 HOUR ACCUMULATION 31/USP",
             "NCF": "CLUTTER FILTER CONTROL",
             "NCO": "RADAR COMPOSITE REFLECTIVITY 2.2NM RES 8 LEVELS ID 36/CR",
             "NCR": "RADAR COMPOSITE REFLECTIVITY .54NM RES 16 LEVELS ID 37/CR",
             "NCZ": "RADAR COMPOSITE REFLECTIVITY 2.2NM RES 16 LEVELS ID 38/CR",
             "NET": "RADAR ECHO TOPS ID 41/ET",
             "NHI": "HAIL INDEX 59/HI",
             "NHL": "RADAR HIGH LAYER COMPOSITE REFLECTIVITY MAX ID 90/LRM",
             "NLA": "RADAR LOW LAYER COMPOSITE REFLECTIVITY AP RMVD ID 67/ARP",
             "NLL": "RADAR LOW LAYER COMPOSITE REFLECTIVITY MAX ID 65/LRM",
             "NME": "MESOCYCLONE 60/M",
             "NML": "RADAR MIDDLE LAYER COMPOSITE REFLECTIVITY MAX ID 66/LRM",
             "NOW": "SHORT TERM FORECAST",
             "NPW": "NON-PRECIPITATION WARNINGS, WATCHES, ADVISORIES",
             "NSH": "NEARSHORE MARINE FORECAST",
             "NSP": "BASE SPECTRUM WIDTH 32NM .13NM X 1 DEG",
             "NSS": "STORM STRUCTURE 62/SS",
             "NST": "STORM TRACKING INFORMATION 58/STI",
             "NSW": "BASE SPECTRUM WIDTH 124NM .54NM X 1 DEG",
             "NTP": "RADAR STORM TOTAL PRECIPITATION ACCUMULATION 80/STP",
             "NTV": "TORNADO VORTEX SIGNATURE 61/TVS",
             "NUP": "RADAR USER SELECT PRECIPITATION ACCUMULATION 31/USP",
             "NUW": "NUCLEAR POWER PLANT WARNING",
             "NVL": "RADAR VERTICALLY INTEGRATED LIQUID ID 57/VIL",
             "NVW": "RADAR VELOCITY AZIMUTH DISPLAY WIND PROFILE 48/VWP",
             "NWP": "SEVERE WEATHER PROBABILITY 47/SWP ",
             "OAV": "OTHER AVIATION PRODUCTS",
             "OCD": "OCEANOGRAPHIC DATA",
             "OFA": "OFFSHORE AVIATION AREA FORECAST",
             "OFF": "OFFSHORE FORECAST",
             "OMR": "OTHER MARINE PRODUCTS",
             "OPU": "OTHER PUBLIC PRODUCTS",
             "OSB": "OCEANOGRAPHIC SPECTRAL BULLETIN",
             "OSO": "OTHER SURFACE OBSERVATIONS",
             "OSW": "OCEAN SURFACE WINDS",
             "OUA": "OTHER UPPER AIR DATA",
             "PAR": "PERFORMANCE ACCOMPLISHMENT REPORT",
             "PBF": "PRESCRIBED BURN FORECAST",
             "PFM": "POINT FORECAST MATRICES",
             "PIB": "PIBAL OBSERVATION *",
             "PIR": "PILOT REPORT *",
             "PLS": "PLAIN LANGUAGE SHIP REPORT",
             "PMD": "PROGNOSTIC METEOROLOGICAL DISCUSSION",
             "PNS": "PUBLIC INFORMATION STATEMENT",
             "POE": "PROBABILITY OF EXCEED ",
             "PRC": "STATE PILOT REPORT COLLECTIVE",
             "PSH": "POST STORM HURRICANE REPORT",
             "PSM": "PROGNOSTIC SNOW MELT",
             "PVM": "PUBLIC VERIFICATION MATRIX",
             "PWO": "PUBLIC SEVERE WEATHER OUTLOOK",
             "QCD": "ASOS DAILY QUALITY CONTROL MESSAGE",
             "QCH": "ASOS HOURLY QUALITY CONTROL MESSAGE",
             "QCM": "ASOS MONTHLY QUALITY CONTROL MESSAGE",
             "QCW": "ASOS WEEKLY QUALITY CONTROL MESSAGE",
             "QPF": "QUANTITATIVE PRECIPITATION FORECAST",
             "QPS": "QUANTITATIVE PRECIPITATION STATEMENT",
             "RBG": "RED BOOK GRAPHIC ** ",
             "RCM": "WSR-88D RADAR CODED MESSAGE",
             "RDF": "REVISED DIGITAL FORECAST",
             "RDG": "REVISED DIGITAL GUIDANCE",
             "REC": "RECREATIONAL REPORT",
             "RER": "RECORD REPORT",
             "RFD": "RANGELAND FIRE DANGER FORECAST",
             "RFR": "ROUTE FORECAST",
             "RFW": "RED FLAG WARNING",
             "RHW": "RADIOLOGICAL HAZARD WARNING",
             "ROB": "RADAR OBSERVATION         ",
             "RR1": "HYDROLOGY METEOROLOGY DATA REPORT PART 1",
             "RR2": "HYDROLOGY-METEOROLOGY DATA REPORT PART 2",
             "RR3": "HYDROLOGY-METEOROLOGY DATA REPORT PART 3",
             "RR4": "HYDROLOGY-METEOROLOGY DATA REPORT PART 4",
             "RR5": "HYDROLOGY-METEOROLOGY DATA REPORT PART 5",
             "RR6": "ASOS SHEF PRECIP CRITERIA MESSAGE (COMMISSIONED)",
             "RR7": "ASOS SHEF HOURLY ROUTINE MESSAGE (COMMISSIONED)",
             "RR8": "HYDROLOGY-METEOROLOGY DATA REPORT PART 8  ",
             "RR9": "HYDROLOGY-METEOROLOGY DATA REPORT PART 9  ",
             "RRA": "AUTOMATED HYDROLOGIC OBSERVATION STA REPORT (AHOS)",
             "RRC": "SCS MANUAL SNOW COURSE DATA",
             "RRM": "MISCELLANEOUS HYDROLOGIC DATA",
             "RRS": "SPECIAL AUTOMATED HYDROMET DATA REPORT",
             "RRX": "ASOS SHEF PRECIPITATION CRITERIA TEST MESSAGE",
             "RRY": "ASOS SHEF HOURLY ROUTINE TEST MESSAGE",
             "RSD": "DAILY SNOTEL DATA",
             "RSL": "WSR-88D RPG SYSTEM STATUS LOGS",
             "RSM": "MONTHLY SNOTEL DATA",
             "RTP": "REGIONAL MAX/MIN TEMP AND PRECIPITATION TABLE ",
             "RVA": "RIVER SUMMARY",
             "RVD": "DAILY RIVER FORECASTS",
             "RVF": "RIVER FORECAST",
             "RVI": "RIVER ICE STATEMENT",
             "RVM": "MISCELLANEOUS RIVER PRODUCT",
             "RVR": "RIVER RECREATION STATEMENT",
             "RVS": "RIVER STATEMENT",
             "RWO": "RADAR SUPEROB",
             "RWR": "REGIONAL WEATHER ROUNDUP",
             "RWS": "REGIONAL WEATHER SUMMARY",
             "RZF": "REGIONAL ZONE FORECAST",
             "SAA": "SPACE ENVIRONMENT ALERT ADVISORY",
             "SAB": "SNOW AVALANCHE BULLETIN",
             "SAD": "DAILY SURFACE AVIATION WEATHER SUMMARY",
             "SAF": "SPECI AGRI WX FCST/ADVISORY/FLYING FARMER FCST OUTLOOK",
             "SAG": "SNOW AVALANCHE GUIDANCE",
             "SAM": "MONTHLY SURFACE AVIATION WEATHER SUMMARY",
             "SAW": "PRELIM NOTICE OF WATCH & CANCELLATION MSG AVIATION)",
             "SCC": "STORM SUMMARY",
             "SCD": "SUPPLEMENTARY CLIMATOLOGICAL DATA (ASOS)",
             "SCN": "SOIL CLIMATE ANALYSIS NETWORK DATA",
             "SCP": "SATELLITE CLOUD PRODUCT",
             "SCS": "SELECTED CITIES SUMMARY",
             "SCV": "SATELLITE AREAL EXTENT OF SNOW COVER",
             "SDO": "SUPPLEMENTARY DATA OBSERVATION (ASOS)",
             "SDS": "SPECIAL DISPERSION STATEMENT",
             "SEL": "SEVERE LOCAL STORM WATCH AND WATCH CANCELLATION MSG",
             "SES": "SPACE ENVIRONMENT SUMMARY",
             "SEV": "SPC WATCH POINT INFORMATION MESSAGE",
             "SFD": "STATE FORECAST DISCUSSION",
             "SFP": "STATE FORECAST",
             "SFT": "TABULAR STATE FORECAST",
             "SGL": "RAWINSONDE OBSERVATION SIGNIFICANT LEVELS *",
             "SGW": "PLAIN LANGUAGE SIGNIFICANT WEATHER FORECAST",
             "SHI": "SFC SHIP REPORT AT INTERMEDIATE SYNOPTIC TIME *",
             "SHN": "SURFACE SHIP REPORT AT NON-SYNOPTIC TIME *",
             "SHP": "SURFACE SHIP REPORT AT SYNOPTIC TIME *",
             "SIG": "INTERNATIONAL SIGMET / CONVECTIVE SIGMET",
             "SIM": "SATELLITE INTERPRETATION MESSAGE",
             "SLS": "SEVERE LOCAL STORM WATCH AND AREAL OUTLINE",
             "SMA": "MARINE SUBTROPICAL STORM ADVISORY",
             "SMF": "SMOKE MANAGEMENT WEATHER FORECAST",
             "SMW": "SPECIAL MARINE WARNING",
             "SPD": "SUPPLEMENTAL PRECIPITATION 82/SPD ",
             "SPE": "SATELLITE PRECIPITATION ESTIMATES (TXUS20 KWBC)  ",
             "SPF": "STORM STRIKE PROBABILITY BULLETIN(TPC)",
             "SPS": "SPECIAL WEATHER STATEMENT",
             "SPW": "SHELTER IN PLAce WARNING",
             "SRF": "SURF FORECAST",
             "SSA": "SPACE ENVIRONMENT SUMMARY ADVISORY",
             "SSI": "INTERMEDIATE SYNOPTIC HOUR SURFACE OBSERVATION *",
             "SSM": "MAIN SYNOPTIC HOUR SURFACE OBSERVATION *",
             "SSN": "NON STANDARD SYNOPTIC HOUR SURFACE OBSERVATION *",
             "STA": "NETWORK AND SEVERE WEATHER STATISTICAL SUMMARIES",
             "STD": "SATELLITE TROPICAL DISTURBANCE SUMMARY",
             "STO": "ROAD CONDITION REPORTS (STATE AGENCIES)",
             "STP": "STATE MAX/MIN TEMPERATURE AND PRECIPITATION TABLE",
             "STQ": "SPOT FORECAST REQUEST",
             "STW": "CANADIAN STORM WARNING",
             "SVR": "SEVERE THUNDERSTORM WARNING",
             "SVS": "SEVERE WEATHER STATEMENT",
             "SWD": "SPACE ENVIRONMENT WARNING ADVISORY",
             "SWE": "ESTIMATED SNOW WATER EQUIVALENT BY BASIN",
             "SWO": "SEVERE STORM OUTLOOK NARRATIVE (AC)",
             "SWS": "STATE WEATHER SUMMARY",
             "TAF": "TERMINAL AERODROME FORECAST *",
             "TAP": "TERMINAL ALERTING PRODUCTS (AFOS LOCAL USE ONLY)",
             "TAV": "TRAVELERS FORECAST TABLE",
             "TCA": "TROPICAL CYCLONE ADVISORY",
             "TCD": "TROPICAL CYCLONE DISCUSSION",
             "TCE": "TROPICAL CYCLONE POSITION ESTIMATE",
             "TCM": "MARINE/AVIATION TROPICAL CYCLONE ADVISORY",
             "TCP": "PUBLIC TROPICAL CYCLONE ADVISORY",
             "TCS": "SATELLITE TROPICAL CYCLONE SUMMARY",
             "TCU": "TROPICAL CYCLONE UPDATE",
             "TCV": "TROPICAL CYCLONE VTEC",
             "TID": "TIDE REPORT",
             "TMA": "TSUNAMI TIDE/SEISMIC MESSAGE ACKNOWLEDGMENT",
             "TOE": "911 TELEPHONE OUTAGE EMERGENCY",
             "TOR": "TORNADO WARNING",
             "TPT": "TEMPERATURE PRECIPITATION TABLE (NATL AND INTNL)",
             "TSM": "TSUNAMI TIDE/SEISMIC MESSAGE",
             "TST": "TEST MESSAGE",
             "TSU": "TSUNAMI WATCH/WARNING",
             "TVL": "TRAVELERS FORECAST",
             "TWB": "TRANSCRIBED WEATHER BROADCAST *",
             "TWD": "TROPICAL WEATHER DISCUSSION",
             "TWO": "TROPICAL WEATHER OUTLOOK AND SUMMARY",
             "TWS": "TROPICAL WEATHER SUMMARY",
             "UJX": "JSC UPPER AIR SOUNDINGS",
             "ULG": "UPPER AIR SITE PERFORMANCE & LOGISTICS MESSAGE",
             "UVI": "ULTRAVIOLET INDEX",
             "VAA": "VOLCANIC ACTIVITY ADVISORY",
             "VER": "FORECAST VERIFICATION STATISTICS",
             "VFT": "TERMINAL AERODROME FORECAST (TAF) VERIFICATION",
             "VGP": "VECTOR GRAPHIC **",
             "VOW": "VOLCANO WARNING",
             "WA0": "AIRMET (PACIFIC)",
             "WA1": "AIRMET (NORTHEAST U.S.)",
             "WA2": "AIRMET (SOUTHEAST U.S.)",
             "WA3": "AIRMET (NORTH CENTRAL U.S.)",
             "WA4": "AIRMET (SOUTH CENTRAL U.S.)",
             "WA5": "AIRMET (U.S. ROCKY MOUNTAINS)",
             "WA6": "AIRMET (U.S. WEST COAST)",
             "WA7": "AIRMET (JUNEAU, ALASKA)",
             "WA8": "AIRMET (ANCHORAGE, ALASKA)",
             "WA9": "AIRMET (FAIRBANKS, ALASKA)",
             "WAC": "AIRMET (CARIBBEAN)",
             "WAR": "SPACE ENVIRONMENT WARNING",
             "WAT": "SPACE ENVIRONMENT WATCH",
             "WCL": "WATCH CLEARANCE MESSAGE",
             "WCN": "WEATHER WATCH CLEARANCE NOTIFICATION",
             "WCR": "WEEKLY WEATHER AND CROP REPORT",
             "WDA": "WEEKLY DATA FOR AGRICULTURE",
             "WEK": "ROUTINE SPACE ENVIRONMENT PRODUCT ISSUED WEEKLY",
             "WPD": "WIND PROFILER DATA (BUFR CODE) **",
             "WRK": "LOCAL WORK FILE (ii IS CHOSEN BY SITE OR REGION)",
             "WS1": "SIGMET (NORTHEAST U.S.)",
             "WS2": "SIGMET (SOUTHEAST U.S.)",
             "WS3": "SIGMET (NORTH CENTRAL U.S.)",
             "WS4": "SIGMET (SOUTH CENTRAL U.S.)",
             "WS5": "SIGMET (U.S. ROCKY MOUNTAINS)",
             "WS6": "SIGMET (U.S. WEST COAST)",
             "WS7": "SIGMET (JUNEAU, ALASKA)",
             "WS8": "SIGMET (ANCHORAGE, ALASKA)",
             "WS9": "SIGMET (FAIRBANKS, ALASKA)",
             "WST": "TROPICAL CYCLONE SIGMET",
             "WSV": "VOLCANIC ACTIVITY SIGMET",
             "WSW": "WINTER WEATHER WARNINGS, WATCHES, ADVISORIES",
             "WTS": "WARNING TEST MESSAGE FROM NCF",
             "WVM": "WARNING VERIFICATION MESSAGE",
             "WWA": "WATCH STATUS REPORT",
             "WWP": "SEVERE THUNDERSTORM/TORNADO WATCH PROBABILITIES",
             "ZFP": "ZONE FORECAST PRODUCT"}
    }
    
    def _process_matches(self, matches):
        self.code = Bunch(category=matches[0], designator=matches[1])
        self.category = self._interpret("category", self.code.category)
        self.designator = self.code.designator
    
