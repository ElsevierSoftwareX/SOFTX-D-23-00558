NIFO_MAX = 8

# todo: split object into sections, and flatten them before validation
schema = {
    "type": "object",
    "properties": {
        "analysis": {
            "enum": ["1G", "2G"],
            "description": "true/false -> online/offline",
            "default": "2G"
        },
        "cfg_search": {
            "enum": ["r", "i", "p", "l", "s", "c", "g", "e", "b",
                     "R", "I", "P", "L", "S", "C", "G", "E", "B"],
            "description": "see description below",
            "default": "r"
        },
        "online": {
            "type": "boolean",
            "description": "true/false -> online/offline",
            "default": False
        },
        "optim": {
            "type": "boolean",
            "description": "true -> optimal resolution likelihood analysis",
            "default": False
        },
        "fLow": {
            "type": "number",
            "description": "low frequency of the search",
            "default": 64.
        },
        "fHigh": {
            "type": "number",
            "description": "high frequency of the search",
            "default": 2048.
        },
        "ifo": {
            "type": "array",
            "items": {
                "type": "string"
            },
            "uniqueItems": True,
            "description": "ifo[] can be redefined by user",
            "default": ["L1", "H1", "V1", "I1", "J1", "G1"]
        },
        "nIFO": {
            "type": "integer",
            "description": "number of interferometers",
            "default": NIFO_MAX
        },
        "refIFO": {
            "type": "string",
            "description": "reference IFO",
            "default": "L1"
        },
        "select_subrho": {
            "type": "number",
            "description": "subrho netcluster select function threshold (coherence)",
            "default": 5.0
        },
        "select_subnet": {
            "type": "number",
            "description": "subnet netcluster select function threshold (coherence)",
            "default": 0.1
        },
        "bpp": {
            "type": "number",
            "description": "probability for black pixel selection (netpixel)",
            "default": 0.001
        },
        "fResample": {
            "type": "number",
            "description": "if zero resampling is not applied",
            "default": 0
        },
        "inRate": {
            "type": "number",
            "description": "input data rate",
            "default": 16384
        },
        "EFEC": {
            "type": "boolean",
            "description": "Earth Fixed / Selestial coordinates",
            "default": True,
        },
        # fixme: implement Toolfun::GetPrecision
        "precision": {
            "type": "number",
            "description": "set parameters for big clusters events management",
            "default": 0.0,
        },
        "pattern": {
            "type": "integer",
            "description": "select pixel pattern used to produce the energy max maps for pixel's selection \n"
                           'patterns: "/" - ring-up, "\\" - ring-down, "|" - delta, "-" line, "*" - single \n'
                           'pattern =  0 - "*"   1-pixel  standard search \n'
                           'pattern =  1 - "3|"  3-pixels vertical packet (delta) \n'
                           'pattern =  2 - "3-"  3-pixels horizontal packet (line) \n'
                           'pattern =  3 - "3/"  3-pixels diagonal packet (ring-up) \n'
                           'pattern =  4 - "3\"  3-pixels anti-diagonal packet (ring-down) \n'
                           'pattern =  5 - "5/"  5-pixels diagonal packet (ring-up) \n'
                           'pattern =  6 - "5\"  5-pixels anti-diagonal packet (ring-down) \n'
                           'pattern =  7 - "3+"  5-pixels plus packet (plus) \n'
                           'pattern =  8 - "3x"  5-pixels cross packet (cross) \n'
                           'pattern =  9 - "9p"  9-pixels square packet (box) \n'
                           'pattern = else - "*" 1-pixel  packet (single) \n'
                           '------------------------------------------------------------------------------------ \n'
                           'pattern==0                   Standard Search : std-pixel    selection + likelihood2G \n'
                           'pattern!=0 && pattern<0      Mixed    Search : packet-pixel selection + likelihood2G  \n'
                           'pattern!=0 && pattern>0      Packed   Search : packet-pixel selection + likelihoodWP \n',
            "default": 0
        },
        "nSky": {
            "type": "integer",
            "description": "if nSky>0 -> # of skymap prob pixels dumped to ascii \n "
                           "if nSky=0 -> (#pixels==1000 || cum prob > 0.99) \n "
                           "if nSky<0 -> nSky=-XYZ... save all pixels with prob < 0.XYZ...",
            "default": 0
        },
        "subnet": {
            "type": "number",
            "description": "[0,0.7] sub network threshold (supercluster)",
            "default": 0.7,
            "minimum": 0,
            "maximum": 0.7,
        },
        "subcut": {
            "type": "number",
            "description": "[0,1]   sub network threshold in the skyloop (supercluster)",
            "default": 0.33,
            "minimum": 0,
            "maximum": 1,
        },
        "netRHO": {
            "type": "number",
            "description": "[>4.0] coherent network SNR (supercluster, likelihood)",
            "default": 4.0,
            "minimum": 4.0,
        },
        "netCC": {
            "type": "number",
            "description": "network correlation (supercluster, likelihood)",
            "default": 0.5
        },
        "Acore": {
            "type": "number",
            "description": "threshold of core pixels (supercluster, likelihood)",
            "default": 2 ** 0.5
        },
        "Tgap": {
            "type": "number",
            "description": "defragmentation time gap between clusters (sec)",
            "default": 3.0
        },
        "Fgap": {
            "type": "number",
            "description": "defragmentation frequency gap between clusters (Hz)",
            "default": 130.
        },
        "TFgap": {
            "type": "number",
            "description": "threshold on the time-frequency separation between two pixels",
            "default": 6.
        },
        "delta": {
            "type": "number",
            "description": "[-1:1] regulate 2 Detector sky locations. delta=0 : regulator is disabled, delta<0 : select Lo as skystat instead of Lr",
            "default": 0.5,
            "minimum": -1,
            "maximum": 1,
        },
        "cfg_gamma": {
            "type": "number",
            "description": "[-1:1] regulate |fx|<<|f+| and |f+|<<1 sky locations. gamma=0 : regulator is disabled, gamma<0 : sky prior is applied",
            "default": 0.5,
            "minimum": -1,
            "maximum": 1,
        },
        "Theta1": {
            "type": "number",
            "description": "start theta",
            "default": 0.0
        },
        "Theta2": {
            "type": "number",
            "description": "stop theta",
            "default": 180.,
        },
        "Phi1": {
            "type": "number",
            "description": "start phi",
            "default": 0.0
        },
        "Phi2": {
            "type": "number",
            "description": "stop phi",
            "default": 360.,
        },
        "skyMaskFile": {
            "type": "string",
            "description": "sky mask file",
            "default": ""
        },
        "skyMaskCCFile": {
            "type": "string",
            "description": "sky mask file",
            "default": ""
        },
        "segLen": {
            "type": "number",
            "description": "Segment length [sec]",
            "default": 600.
        },
        "segMLS": {
            "type": "number",
            "description": "Minimum Segment Length after DQ_CAT1 [sec]",
            "default": 300.
        },
        "segTHR": {
            "type": "number",
            "description": "Minimum Segment Length after DQ_CAT2 [sec] (to disable put segTHR=0)",
            "default": 30.
        },
        "segEdge": {
            "type": "number",
            "description": "wavelet boundary offset [sec]",
            "default": 8.
        },
        "segOverlap": {
            "type": "number",
            "description": "overlap between job segments [sec]",
            "default": 0.
        },
        "lagSize": {
            "type": "integer",
            "description": "number of lags (simulation:1)",
            "default": 1
        },
        "lagStep": {
            "type": "number",
            "description": "[sec] time interval between lags",
            "default": 1.
        },
        "lagOff": {
            "type": "integer",
            "description": "first lag id (lagOff=0 - include zero lag )",
            "default": 6.
        },
        "lagMax": {
            "type": "number",
            "description": "0/>0 -  standard/extended lags",
            "default": 150
        },
        "channelNamesRaw": {
            "type": "array",
            "description": "channel names for raw data",
            "default": []
        },
        "channelNamesMDC": {
            "type": "array",
            "description": "channel names for MDC data",
            "default": []
        },
        "frFiles": {
            "type": "array",
            "default": []
        },
        "DQF": {
            "type": "array",
            "c_type": "dqfile",
            "default": []
        },
        "nDQF": {
            "type": "integer",
            "default": NIFO_MAX
        },
        "iwindow": {
            "type": "number",
            "description": "injection time window (Tinj +/- iwindow/2)",
            "default": 5.0
        },
        "gap": {
            "type": "number",
            "description": "alias of iwindow",
            "default": 5.0
        },
        "l_low": {
            "type": "integer",
            "description": "low frequency resolution level (2^l_low Hz)",
            "default": 3
        },
        "l_high": {
            "type": "integer",
            "description": "high frequency resolution level (2^l_high Hz)",
            "default": 8
        },
        "l_white": {
            "type": "integer",
            "description": "whitening frequency resolution level (2^l_white Hz), if 0 then l_white=l_high",
            "default": 0
        },
        "whiteWindow": {
            "type": "number",
            "description": "[sec] time window dT. if = 0 - dT=T, where T is segment duration",
            "default": 60.
        },
        "whiteStride": {
            "type": "number",
            "description": "[sec] noise sampling time stride",
            "default": 20.
        },
        "simulation": {
            "type": "integer",
            "default": 0
        },
        "nfactor": {
            "type": "number",
            "description": "number of simulation factors",
            "default": 0
        },
        "factors": {
            "type": "array",
            "items": {
                "type": "number"
            },
            "description": "array of simulation factors (when sim=4 factors[0] is used as offset [must be int])",
            "default": []
        },
        "levelR": {
            "type": "integer",
            "description": "resampling level : inRate[fResample]/(2^levelR) Hz",
            "default": 2
        },
        "healpix": {
            "type": "number",
            "description": "if not 0 use healpix sky map (number of sky pixels = 12*pow(4,healpix))",
            "default": 7
        },
        "plugin": {
            "type": "string",
            "c_type": "TMacro",
            "default": ""
        },
        "configPlugin": {
            "type": "string",
            "c_type": "TMacro",
            "default": ""
        },
        "filter_dir": {
            "type": "string",
            "description": "filter directory, defaults to environment HOME_WAT_FILTERS",
            "default": ""
        },
        "wdmXTalk": {
            "type": "string",
            "description": "WDM cross-talk file",
            "default": "wdmXTalk/OverlapCatalog_Lev_8_16_32_64_128_256_iNu_4_Prec_10.bin"
        },
        "upTDF": {
            "type": "integer",
            "description": "upsample factor to obtain rate of TD filter : TDRate = (inRate>>levelR)*upTDF",
            "default": 4
        },
        "TDSize": {
            "type": "integer",
            "description": "time-delay filter size (max 20) ",
            "default": 12,
            "maximum": 20
        },
    },
    "required": ["analysis", "ifo", "refIFO"],
    "additionalProperties": False
}
