# Referência https://wiki.seg.org/wiki/Seismic_Facies_Classification
SEISMIC_EVENTS = {
    'seismic': [
        'seismic section', 'seismic image', 'slice', 'seismic slice',
        'section', '2D section', 'seismic model', '2D seismic model',
    ],
    'casual': [
        'we see here', 'this image represents', 'we observe here',
        'this image demonstrates', 'this depicts', '',
    ],
    'sigmoid': [
        'a sigmoid', 'a clinoform', 'progradational geometry',
        'a sigmoidal clinoform set', 'an oblique clinoform pattern',
        'forward-prograding geometry',
    ],
    'shingled': [
        'overlapping geometry', 'superposed structure', 'shingled reflection',
        'shingled stratification',
    ],
    'subparallel': [
        'nearly parallel reflection set', 'almost parallel reflectors',
        'weakly dipping layers', 'gently converging reflections',
        'subhorizontal bedding pattern', 'mildly inclined strata',
        'semi-parallel internal geometry', 'uniformly stratified reflections',
        'near-parallel lamination',
    ],
    'parallel': [
        'a parallel geometry', 'continuous horizontal reflections', 'a planar geometry',
        'an uniform layering pattern', 'a parallel-bedded strata',
        'concordant seismic layering', 'a tabular reflection pattern',
        'laterally uniform bedding', 'a parallel-laminated unit',
        'an horizontally layered sequence',
    ],
    'divergent': [
        'a divergent bedform geometry', 'diverging seismic pattern',
        'thickening wedge pattern', 'divergent foreset reflections',
        'differentially dipping reflectors',
    ],
    'mounded': [
        'mounded geometry', 'domed structure', 'rounded pattern',
        'positive-relief geometry', 'convex-up reflection geometry',
        'mounded depositional body', 'positive-relief feature',
        'dome-shaped seismic pattern',
    ],
    'hummocky': [
        'a rugged reflector package', 'a corrugated seismic unit.',
        'a hummocky cross-stratified pattern', 'a low-relief mound-and-swale structure',
        'an uneven depositional surface', 'gently rolling internal reflections',
        'a corrugated seismic texture',
    ],
    'chaotic': [
        'chaotic reflections', 'an undefined seismic structure', 'a chaotic pattern',
        'undefined internal geometry', 'chaotic internal geometry',
        'internal structuraly disturbed reflexions',
    ],
    'chaotic-channels': [
        'disordered reflection patterns indicative of potential meandering channels',
        'irregular seismic reflections suggestive of channel systems',
        'undefined internal geometry with possibility of containing channels',
        'complex and chaotic reflection patterns indicating possible presence of channels',
        'chaotic seismic reflections potentially indicative of meandering channel systems',
    ],
    'wavy': [
        'a wavy structure', 'wavy seismic reflection geometry', 'wave-like seismic unit',
        'undulating bedding configuration', 'undulatory reflector pattern',
    ],
    'folded': [
        'a folded reflector package', 'a folded strata',
        'deformation-related geometry',
    ],
    'faulted': [
        'faulted structure', 'rigid deformation known or fault',
        'structural discontinuity', 'tectonic fault',
    ],
    'tilted': [
        'tilt', 'tectonic tilting', 'inclined horizontal beds',
        'tilted horizontal beds',
    ],
    'connectors': [
        'of', 'containing', 'presenting', 'exhibiting',
        'featuring', 'characterized by',
    ],
    'connectors details': [
        'with', '. This section has',
        '. The seismic section has', '. The image has',
    ],
}

AMPL_FREQ_NOISE = {
    'high amplitude': ['high amplitude', 'strong signal',],
    'low amplitude' : ['low amplitude', 'weak signal'],
    'high frequency': ['high frequency', 'short-period signal',
                       'short wavelength', 'high-frequency components',],
    'low frequency' : ['low frequency', 'long-period signal',
                       'low-frequency seismic energy',],
    'high noise'    : ['high noise', 'noisy data', 'low signal-to-noise ratio',],
    'low noise'     : ['low noise', 'noise-free components', ],
}

POSSIBLE_LABELS = ['sigmoid', 'shingled', 'subparallel', 'parallel', 'divergent',
                   'mounded', 'hummocky', 'chaotic', 'wavy', ]


FULL_FACIES_NAMES = {'cha': 'chaotic', 'par': 'parallel',
                     'sig': 'sigmoid', 'div': 'divergent',}
