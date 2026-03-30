# Referência https://wiki.seg.org/wiki/Seismic_Facies_Classification
SEISMIC_EVENTS = {
    'seismic': [
        'seismic section', 'seismic image', 'subsurface model', 'slice',
        'section', '2D section', '2D subsurface model',
        'subsurface representation', 'seismic model', '2D seismic model',
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
        'imbricated reflection sets', 'shingled stratification',
        'layer-on-layer reflection geometry',
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
        'a divergent bedform geometry', 'a spreading stratigraphic unit',
        'diverging seismic pattern', 'flaring reflection geometry',
        'a fanning reflection geometry', 'thickening wedge pattern',
        'divergent foreset reflections', 'differentially dipping reflectors',
    ],
    'mounded': [
        'mounded geometry', 'domed structure', 'rounded pattern',
        'positive-relief geometry', 'convex-up reflection geometry',
        'mounded depositional body', 'positive-relief feature',
        'lenticular reflection pattern', 'dome-shaped seismic pattern',
    ],
    'deformed': [
        'disturbed reflection zone', 'folded reflector package',
        'distorted reflection set', 'structurally disturbed reflections',
        'a folded and faulted strata', 'deformation-related geometry',
        'a warped reflection package', 'deformed structure', 'distorted seismic face',
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
        'imbricated reflection sets', 'layer-on-layer reflection geometry',
    ],
    # Intensity
    'high': [
        'elevated', 
    ],
    'connectors': ['of', 'with', 'containing', 'presenting', 'exhibiting',
                   'featuring', 'characterized by'],
    #'plural_connectors':   [' of', ' with', ' containing', ' presenting', ' exhibiting'],
}


POSSIBLE_LABELS = ['sigmoid', 'shingled', 'subparallel', 'parallel', 'divergent',
                   'mounded', 'deformed', 'hummocky', 'chaotic', 'wavy', ]
