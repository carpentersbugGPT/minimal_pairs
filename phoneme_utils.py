# phoneme_utils.py

def compare_phonemes(expected_word, recognized_word, phonemic_contrasts):
    """
    Compare the phonemes of the expected word and the recognized word,
    and provide feedback based on phonemic contrasts.

    Parameters:
    - expected_word (str): The word that was expected.
    - recognized_word (str): The word that was recognized.
    - phonemic_contrasts (list): A list of dictionaries containing contrast phonemes and descriptions.

    Returns:
    - tuple: A message string and the contrast description (if any).
    """
    
    # Expanded word-to-phoneme mapping with minimal pairs
    word_to_phoneme = {
        # Monophthongs (Vowels)
        "pan": "/pæn/",
        "cap": "/kæp/",
        "pen": "/pɛn/",
        "bed": "/bɛd/",
        "cup": "/kʌp/",
        "bud": "/bʌd/",
        "pot": "/pɒt/",
        "cot": "/kɒt/",
        "pin": "/pɪn/",
        "sheep": "/ʃiːp/",
        "ship": "/ʃɪp/",
        "keep": "/kiːp/",
        "port": "/pɔːt/",
        "pull": "/pʊl/",
        "pool": "/puːl/",
        "pain": "/peɪn/",
        "pawn": "/pɔːn/",
        "part": "/pɑːt/",
        "purn": "/pɜːn/",
        "pun": "/pʌn/",
        "poon": "/puːn/",
        "pon": "/pɒn/",
        "pint": "/paɪnt/",
        "kite": "/kaɪt/",
        "cute": "/kjuːt/",
        "caught": "/kɔːt/",
        "cat": "/kæt/",
        "kit": "/kɪt/",
        "cop": "/kɒp/",
        "cope": "/kəʊp/",
        "cape": "/keɪp/",
        "kept": "/kɛpt/",
        "flea": "/fliː/",
        "flee": "/fliː/",
        "fly": "/flaɪ/",
        "flow": "/fləʊ/",
        "flaw": "/flɔː/",
        "flew": "/fluː/",
        "floor": "/flɔː/",
        "flower": "/flaʊə/",
        "flair": "/fleə/",
        "flour": "/flaʊə/",
        "fright": "/fraɪt/",
        "fruit": "/fruːt/",
        "free": "/friː/",
        "fee": "/fiː/",
        "few": "/fjuː/",
        "go": "/gəʊ/",
        "guy": "/gaɪ/",
        "gay": "/geɪ/",
        "gore": "/gɔː/",
        "gear": "/gɪə/",
        "gare": "/geə/",
        "tour": "/tʊə/",
        "beer": "/bɪə/",
        "bear": "/beə/",
        "poor": "/pʊə/",
        "peer": "/pɪə/",
        "pair": "/peə/",
        "power": "/paʊə/",
        "par": "/pɑː/",
        "paw": "/pɔː/",
        "pear": "/peə/",
        "pier": "/pɪə/",
        "put": "/pʊt/",
        "poo": "/puː/",
        "purr": "/pɜː/",
        
        # Minimal pairs for "pan" (/æ/)
        "pain": "/peɪn/",    # pan vs pain
        "pawn": "/pɔːn/",    # pan vs pawn
        "part": "/pɑːt/",    # pan vs part
        "purn": "/pɜːn/",    # pan vs purn
        "pun": "/pʌn/",       # pan vs pun
        "poon": "/puːn/",     # pan vs poon
        "pin": "/pɪn/",       # pan vs pin
        "pen": "/pɛn/",       # pan vs pen
        
        # Minimal pairs for "cap" (/æ/)
        "cape": "/keɪp/",     # cap vs cape
        "cup": "/kʌp/",       # cap vs cup
        "cop": "/kɒp/",       # cap vs cop
        "keep": "/kiːp/",     # cap vs keep
        "kit": "/kɪt/",       # cap vs kit
        "caught": "/kɔːt/",   # cap vs caught
        "carp": "/kɑːp/",     # cap vs carp
        "curb": "/kɜːb/",     # cap vs curb
        
        # Minimal pairs for "pen" (/e/)
        "pan": "/pæn/",       # pen vs pan
        "pin": "/pɪn/",       # pen vs pin
        "pain": "/peɪn/",     # pen vs pain
        "pun": "/pʌn/",       # pen vs pun
        "pawn": "/pɔːn/",     # pen vs pawn
        "purn": "/pɜːn/",     # pen vs purn
        "poon": "/puːn/",     # pen vs poon
        
        # Minimal pairs for "keep" (/iː/)
        "cape": "/keɪp/",     # keep vs cape
        "kip": "/kɪp/",       # keep vs kip
        "cup": "/kʌp/",       # keep vs cup
        "coop": "/kuːp/",     # keep vs coop
        "cop": "/kɒp/",       # keep vs cop
        "cap": "/kæp/",       # keep vs cap
        "carp": "/kɑːp/",     # keep vs carp
        
        # Minimal pairs for "fly" (/aɪ/)
        "flew": "/fluː/",     # fly vs flew
        "flow": "/fləʊ/",     # fly vs flow
        "flea": "/fliː/",     # fly vs flea
        "flee": "/fliː/",     # fly vs flee
        "flue": "/fluː/",     # fly vs flue
        "flaw": "/flɔː/",     # fly vs flaw
        "floor": "/flɔː/",    # fly vs floor
        
        # Minimal pairs for "cape" (/eɪ/)
        "keep": "/kiːp/",     # cape vs keep
        "cop": "/kɒp/",       # cape vs cop
        "cap": "/kæp/",       # cape vs cap
        "cup": "/kʌp/",       # cape vs cup
        "cope": "/kəʊp/",     # cape vs cope
        "kip": "/kɪp/",       # cape vs kip
        "carp": "/kɑːp/",     # cape vs carp
        
        # Minimal pairs for "go" (/əʊ/)
        "guy": "/gaɪ/",       # go vs guy
        "gay": "/geɪ/",       # go vs gay
        "gow": "/gaʊ/",       # go vs gow
        "goo": "/guː/",       # go vs goo
        "gore": "/gɔː/",      # go vs gore
        "gear": "/gɪə/",      # go vs gear
        "gare": "/geə/",      # go vs gare
        
        # Minimal pairs for "tour" (/ʊə/)
        "tire": "/taɪə/",     # tour vs tire
        "tear": "/teə/",      # tour vs tear
        "tower": "/taʊə/",    # tour vs tower
        "tore": "/tɔː/",      # tour vs tore
        "tear": "/tɪə/",      # tour vs tear
        "too": "/tuː/",       # tour vs too
        "tug": "/tʌg/",       # tour vs tug
        
        # Minimal pairs for Phoneme Practice
        # Vowel Minimal Pairs
        "sit": "/sɪt/",
        "seat": "/siːt/",
        "desk": "/dɛsk/",
        "disk": "/dɪsk/",
        "wet": "/wɛt/",
        "wait": "/weɪt/",
        
        # Additional minimal pairs can be added here...
    }

    # Retrieve phonemes for the expected and recognized words
    expected_phoneme = word_to_phoneme.get(expected_word.lower())
    recognized_phoneme = word_to_phoneme.get(recognized_word.lower())

    # Check if both phonemes exist
    if not expected_phoneme or not recognized_phoneme:
        # Provide feedback if either word is not found
        return f"You said '{recognized_word}', but the correct word was '{expected_word}'.", "No contrast found"

    # Check for exact match (case-insensitive)
    if expected_word.lower() == recognized_word.lower():
        return "Your pronunciation was correct!", None

    # Iterate through phonemic contrasts to find a match
    for contrast in phonemic_contrasts:
        contrast_phoneme = contrast.get('contrast_phoneme')
        contrast_description = contrast.get('contrast_description')

        if recognized_phoneme == contrast_phoneme:
            return (
                f"You said '{recognized_word}', but the correct word was '{expected_word}' "
                f"({contrast_description}).",
                contrast_description
            )

    # Default feedback if no specific contrast is found
    return f"You said '{recognized_word}', but the correct word was '{expected_word}'.", "No contrast found"
