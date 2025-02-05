import pytest
import pandas as pd
import json
from tasks.task1 import task1
from tasks.task2 import task2, task2_preprocess
from tasks.task3 import task3, task3_preprocess
from tasks.task4 import task4, task4_preprocess
from tasks.task5 import task5, task5_preprocess
from tasks.task6 import task6, task6_preprocess
from tasks.task7 import task7, task7_preprocess
from tasks.task8 import task8, task8_preprocess
from tasks.task9 import task9, task9_preprocess


# --------------------------- FIXTURES --------------------------- #
@pytest.fixture
def sentences1():
    """Returns a fresh copy of DUMMY_SENTENCES1 for each test."""
    return pd.DataFrame({"sentence": [
    "Karkaroff looked extremely worried, and Snape looked angry.",
    "Karkaroff hovered behind Snape's desk for the rest of the double period.",
    "Karkaroff seemed intent on preventing Snape from slipping away at the end of class.",
    "Harry deliberately knocked over a bottle to delay Snape."
]})

@pytest.fixture
def sentences2():
    """Returns a fresh copy of DUMMY_SENTENCES2 for each test."""
    return pd.DataFrame({"sentence": [
    "`This is urgent,` said Harry curtly.",
    "`Ooooh, urgent, is This?` said the other gargoyle in a high-pitched voice."
    "`Well, that's put us in our place, hasn't that?`",
]})

@pytest.fixture
def sentences3():
    """Returns a fresh copy of DUMMY_SENTENCES3 for each test."""
    return pd.DataFrame({"sentence": [
    "`Professor, I must insist,` Harry said firmly.",
    "Snape sneered, his dark eyes glittering under the dim candlelight."
]})

@pytest.fixture
def sentences4():
    """Returns a fresh copy of DUMMY_SENTENCES4 for each test."""
    return pd.DataFrame({"sentence": [
    "The parchment was old and fragile, crumbling at the edges."
]})

@pytest.fixture
def sentences5():
    """Returns a fresh copy of DUMMY_SENTENCES5 for each test."""
    return pd.DataFrame({"sentence": [
        "The room was silent except for the scratching of quills on parchment.",
        "Dumbledore gave Harry a long, piercing look over his half-moon glasses.",
        "A chill ran down Hermione's spine as she read the passage from the old book.",
        "The Sorting Hat barely touched Malfoy's head before calling 'SLYTHERIN!'",
        "The train whistled as it pulled into the station, steam billowing from its smokestack.",
        "Neville nervously adjusted his robes before stepping into the dueling ring."
    ]})

@pytest.fixture
def sentences6():
    """Returns a fresh copy of DUMMY_SENTENCES6 for each test."""
    return pd.DataFrame({
        "sentence": [
            "\"This is urgent,' said  Harry curtly.   '",
            "\"Ooooh, urgent, is This?'\"",
            "said the other gargoyle in a high- pitched voice.'",
            "\"Well, that's put us in our place, hasn't that?'\"",
            "Harry knocked.",
            "Harry heard footsteps, then the door opened and  Harry found  Harry face to face with Professor  McGonagall.   '",
            "You haven't been given another detention!'",
            "\"McGonagall said at once,  McGonagall square spectacles flashing alarmingly.   '\"",
            "No... not exactly... said  Hermione slowly.'",
            "More... wondering...",
            "I suppose we're doing the right thing...",
            "I think... aren't     Harry and  Ron looked at each other.   '",
            "\"Well, that clears that up,' said  Ron.'\"",
            "It would've been really annoying if you hadn't explained yourself properly.'",
            "Hermione looked at  Ron as though  Hermione had only just realised  Ron was there.   '",
            "\"I was just wondering,'  Hermione said,  Hermione voice stronger now,' whether we're doing the right thing, starting this Defence Against the Dark Arts group.'\"",
            "' What?'",
            "said  Harry and  Ron together.   '",
            "\"Hermione, group was your idea in the first place!'\"",
            "said  Ron indignantly.   '"
        ]
    })

@pytest.fixture
def names1():
    """Returns a fresh copy of DUMMY_NAMES1 for each test."""
    return pd.DataFrame({
    "Name": ["Ignatia Wildsmith", "Ignatius Tuft","Ignotus Peverell", "Igor Karkaroff"],
    "Other Names": [None]*4
})

@pytest.fixture
def names2():
    """Returns a fresh copy of DUMMY_NAMES2 for each test."""
    return pd.DataFrame({
    "Name": [
        "Magnus", "Malcolm", "Malcolm Baddock", "Malcolm McGonagall",
        "Harold Skively", "Harper", "Harry Potter", "Hassan Mostafa"
    ],
    "Other Names": [
        None, None, None, None, None, None,
        "the boy who lived, undesirable number one, the chosen one, parry otter, the chosen boy, the mudbloods friend",
        None
    ]  # Now correctly has 8 values
})

@pytest.fixture
def names3():
    """Returns a fresh copy of DUMMY_NAMES3 for each test."""
    return pd.DataFrame({
    "Name": [
        "Abernathy", "Abraham Peasegood", "Abraham Potter", "Abraxas Malfoy",
        "Achilles Tolliver", "Stewart Ackerley", "Mrs. Granger"
    ],
    "Other Names": [None] * 7
})

@pytest.fixture
def names4():
    """Returns a fresh copy of DUMMY_NAMES4 for each test."""
    return pd.DataFrame({
    "Name": [
        "Gellert Grindelwald", "Godric Gryffindor", "Gwenog Jones",
        "Glenda Chittock"
    ],
    "Other Names": [""] * 4
})

@pytest.fixture
def names5():
    """Returns a fresh copy of DUMMY_NAMES5 for each test."""
    return pd.DataFrame({
        "Name": [
            "Over-Attentive Wizard", "Bertram Aubrey", "Audrey Weasley",
            'Augusta "Gran" Longbottom', "Augustus Pye", "Augustus Rookwood",
            "Augustus Worme", "Auntie Muriel", "Aunt Marge Dursley",
            "Aurelius Dumbledore", "Aurora Sinistra", "Bathilda Bagshot",
            "Kquewanda Bailey", "Ballyfumble Stranger", "Harry Potter",
            "Aberforth Dumbledore"
        ],
        "Other Names": [
            None, None, None, None, None, None, None, None, None,
            None, None, "Batty", None,
            "Quin, Quivering Quintus, Quintus-Of-The-Silly-Name",
            "The boy who lived, Undesirable Number One, the Chosen One, Parry Otter, the Chosen Boy, the Mudbloods friend",
            None
        ]
    })

@pytest.fixture
def names6():
    """Returns a fresh copy of DUMMY_NAMES6 for each test."""
    return pd.DataFrame({
        "Name": [
            "Abernathy", "Abraham Peasegood", "Abraham Potter", "Abraxas Malfoy",
            "Achilles Tolliver", "Stewart Ackerley", "Mrs. Granger", "Hermione Granger",
            "Hugo Granger-Weasley", "Rose Granger-Weasley", "Granville Jorkins",
            "Gondulphus Graves", "Merton Graves", "Percival Graves", "Grawp",
            "Irma Pince", "Irving Warble", "Isadora Rose", "Isobel McGonagall",
            "Isobel Ross", "Isolt Sayre"
        ],
        "Other Names": [
            None, None, None, None, None, None, None, None, None, None, None, None,
            None, None, None, None, None, None, None, None, "morrigan, elias story"
        ]
    })


@pytest.fixture
def remove_words():
    """Returns a fresh copy of DUMMY_REMOVEWORDS for each test."""
    return pd.DataFrame({"words": [
    "a", "about", "above", "actual", "after", "again", "against", "all",
    "alreadi", "also", "alway", "am", "amp", "an", "and", "ani", "anoth",
    "any", "anyth", "are", "around", "as", "at", "aww", "babi", "back",
    "be", "becaus", "because", "bed", "been", "befor", "before", "being",
    "below", "between", "birthday", "bit", "book", "both", "boy", "but",
    "by", "call", "can", "cannot", "cant", "car", "check", "com", "come",
    "could", "day", "did", "didn", "dinner", "do", "doe", "does", "doesn",
    "doing", "don", "done", "dont", "down", "during", "each", "eat", "end",
    "even", "ever", "everyon", "exam", "famili", "feel", "few", "final",
    "find", "first", "follow", "for", "found", "friday", "from", "further",
    "game", "get", "girl", "give", "gone", "gonna", "got", "gotta", "guess",
    "guy", "had", "hair", "happen", "has", "have", "haven", "having", "he",
    "head", "hear", "her", "here", "hers", "herself", "hey", "him", "himself",
    "his", "home", "hour", "hous", "how", "http", "i", "if", "im", "in",
    "into", "is", "isn", "it", "its", "itself", "job", "just", "keep",
    "know", "last", "later", "least", "leav", "let", "life", "listen",
    "littl", "live", "look", "lot", "lunch", "made", "make", "man", "mani",
    "may", "mayb", "me", "mean", "meet", "might", "mom", "monday", "month",
    "more", "morn", "most", "move", "movi", "much", "must", "my", "myself",
    "need", "never", "new", "night", "no", "nor", "not", "noth", "now",
    "of", "off", "on", "once", "one", "onli", "only", "or", "other", "ought",
    "our", "ours", "ourselves", "out", "over", "own", "peopl", "phone",
    "pic", "pictur", "play", "post", "put", "quot", "rain", "read", "readi",
    "realli", "run", "said", "same", "saw", "say", "school", "see", "seem",
    "she", "shop", "should", "show", "sinc", "sleep", "so", "some", "someon",
    "someth", "song", "soon", "sound", "start", "stay", "still", "studi",
    "stuff", "such", "summer", "sunday", "sure", "take", "talk", "tell",
    "than", "thank", "that", "the", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "thing", "think", "this", "those",
    "though", "thought", "through", "time", "to", "today", "tomorrow",
    "tonight", "too", "total", "tri", "tweet", "twitpic", "twitter", "two",
    "u", "under", "until", "up", "updat", "use", "veri", "very", "video",
    "wait", "wanna", "want", "was", "watch", "way", "we", "weather", "week",
    "weekend", "went", "were", "what", "when", "where", "whi", "which",
    "while", "who", "whom", "why", "will", "with", "woke", "won", "work",
    "world", "would", "www", "yay", "yeah", "year", "yes", "yesterday",
    "yet", "you", "your", "yours", "yourself", "yourselves",
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m", "n",
    "o", "p", "k", "r", "s", "t", "u", "v", "w", "x", "u", "z",
    "mr", "miss", "mrs", "ms"
]})

@pytest.fixture
def kseq_1():
    return {
    "keys":[
		["snape", "looked"],
		["harry", "heard"],
		["karkaroff"],
		["well", "go", "join", "celebrations"],
		["lips"]
    ]
}

@pytest.fixture
def kseq_2():
    return {
    "keys":[
		["breeze", "ruffled"],
        ["small", "hand", "closed"],
        ["dumbledore", "finally"],
        ["dumbledore"]
    ]
}


@pytest.fixture
def pairs1():
    """Returns a fresh copy of Pairs 1 for each test."""
    return {
        "keys": [
            ["harry potter", "aurelius dumbledore"],
            ["hermione granger", "draco malfoy"],
            ["hermione granger", "harry potter"]
        ]
    }


@pytest.fixture
def pairs2():
    """Returns a fresh copy of Pairs 2 for each test."""
    return {
        "keys": [
            ["otto bagman", "aurelius dumbledore"],
            ["hermione granger", "draco malfoy"],
            ["hermione granger", "harry potter"]
        ]
    }


@pytest.fixture
def pairs3():
    """Returns a fresh copy of Pairs 3 for each test."""
    return {
        "keys": [
            ["harry potter", "aurelius dumbledore"],
            ["hermione granger", "draco malfoy"],
            ["hermione granger", "harry potter"]
        ]
    }


@pytest.mark.parametrize(
    "sentences_fixture, names_fixture, expected_output",
    [
        ("sentences1", "names1", {
            "Question 1": {
                "Processed Sentences": [
                    ["karkaroff", "looked", "extremely", "worried", "snape", "looked", "angry"],
                    ["karkaroff", "hovered", "behind", "snape", "desk", "rest", "double", "period"],
                    ["karkaroff", "seemed", "intent", "preventing", "snape", "slipping", "away", "class"],
                    ["harry", "deliberately", "knocked", "bottle", "delay", "snape"]
                ],
                "Processed Names": [
                    [["ignatia", "wildsmith"], []], 
                    [["ignatius", "tuft"], []],
                    [["ignotus", "peverell"], []], 
                    [["igor", "karkaroff"], []]
                ]
            }
        }),
        ("sentences2", "names2", {
            "Question 1": {
                "Processed Sentences": [
                    ["urgent", "harry", "curtly"],
                    ["ooooh", "urgent", "gargoyle", "high", "pitched", "voice", "well", "us", "place", "hasn"]
                ],
                "Processed Names": [
                    [["magnus"], []],
                    [["malcolm"], []],
                    [["malcolm", "baddock"], []],
                    [["malcolm", "mcgonagall"], []],
                    [["harold", "skively"], []],
                    [["harper"], []],
                    [["harry", "potter"], [
                        ["lived"],
                        ["undesirable", "number"],
                        ["chosen"],
                        ["parry", "otter"],
                        ["chosen"],
                        ["mudbloods", "friend"]
                    ]],
                    [["hassan", "mostafa"], []]
                ]
            }
        }),
        ("sentences3", "names3", {
            "Question 1": {
                "Processed Sentences": [
                    ["professor", "insist", "harry", "firmly"],
                    ["snape", "sneered", "dark", "eyes", "glittering", "dim", "candlelight"]
                ],
                "Processed Names": [
                    [["abernathy"], []],
                    [["abraham", "peasegood"], []],
                    [["abraham", "potter"], []],
                    [["abraxas", "malfoy"], []],
                    [["achilles", "tolliver"], []],
                    [["stewart", "ackerley"], []],
                    [["granger"], []]  # Removed "mrs" per the expected output
                ]
            }
        })
    ]
)
def test_task1(sentences_fixture, names_fixture, expected_output, request, remove_words):
    """
    Test Task 1 using pytest fixtures to ensure fresh, independent data for each test.
    
    Args:
        sentences_fixture (str): Fixture name for sentence data.
        names_fixture (str): Fixture name for names data.
        expected_output (dict): Expected JSON output for assertion.
        request (pytest.FixtureRequest): Provides access to fixture values.
        remove_words (pd.DataFrame): Fixture for remove words dataset.
    """
    # Retrieve fresh data from fixtures
    sentences = request.getfixturevalue(sentences_fixture)
    names = request.getfixturevalue(names_fixture)

    # Run Task 1
    result = task1(sentences, names, remove_words)

    # Debugging info if assertion fails
    if result != expected_output:
        print("\n==== DEBUG INFO ====")
        print(f"Sentences Input:\n{sentences.to_dict()}")
        print(f"Names Input:\n{names.to_dict()}")
        print(f"\nExpected Output:\n{expected_output}")
        print(f"\nActual Output:\n{result}")
        print("====================\n")

    # Assert correctness
    assert result == expected_output, f"Mismatch for Task 1 using {sentences_fixture}, {names_fixture}"

@pytest.mark.parametrize("sentences_fixture, max_k, expected_output", [
    ("sentences3", 3, {  # Test with Sentences 3 and max_k=3
        "Question 2": {
            "3-Seq Counts": [
                ["1_seq", [["candlelight", 1], ["dark", 1], ["dim", 1], ["eyes", 1], ["firmly", 1], 
                           ["glittering", 1], ["harry", 1], ["insist", 1], ["professor", 1], 
                           ["snape", 1], ["sneered", 1]]],
                ["2_seq", [["dark eyes", 1], ["dim candlelight", 1], ["eyes glittering", 1], 
                           ["glittering dim", 1], ["harry firmly", 1], ["insist harry", 1], 
                           ["professor insist", 1], ["snape sneered", 1], ["sneered dark", 1]]],
                ["3_seq", [["dark eyes glittering", 1], ["eyes glittering dim", 1], 
                           ["glittering dim candlelight", 1], ["insist harry firmly", 1], 
                           ["professor insist harry", 1], ["snape sneered dark", 1], 
                           ["sneered dark eyes", 1]]],
            ]
        }
    }),
    ("sentences4", 4, {  # Test with Sentences 4 and max_k=4
        "Question 2": {
            "4-Seq Counts": [
                ["1_seq", [["crumbling", 1], ["edges", 1], ["fragile", 1], ["old", 1], ["parchment", 1]]],
                ["2_seq", [["crumbling edges", 1], ["fragile crumbling", 1], ["old fragile", 1], ["parchment old", 1]]],
                ["3_seq", [["fragile crumbling edges", 1], ["old fragile crumbling", 1], ["parchment old fragile", 1]]],
                ["4_seq", [["old fragile crumbling edges", 1], ["parchment old fragile crumbling", 1]]],
            ]
        }
    })
])
def test_task2(sentences_fixture, max_k, expected_output, request, remove_words):
    """
    Test Task 2 using pytest fixtures to ensure fresh, independent test data.
    
    Args:
        sentences_fixture (str): Fixture name for sentence data.
        max_k (int): Maximum k-sequence length.
        expected_output (dict): Expected JSON output for assertion.
        request (pytest.FixtureRequest): Provides access to fixture values.
        remove_words (pd.DataFrame): Fixture for remove words dataset.
    """
    # Retrieve fresh sentence data from fixture
    sentences = request.getfixturevalue(sentences_fixture)

    # Execute Task 2 logic
    result = task2(sentences, remove_words, max_k)

    # Debugging info if assertion fails
    if result != expected_output:
        print("\n==== DEBUG INFO ====")
        print(f"Sentences Input:\n{sentences.to_dict()}")
        print(f"\nExpected Output:\n{expected_output}")
        print(f"\nActual Output:\n{result}")
        print("====================\n")

    # Assert correctness
    assert json.dumps(result, sort_keys=True) == json.dumps(expected_output, sort_keys=True), \
        f"Mismatch for Task 2 using {sentences_fixture} with max_k={max_k}"

@pytest.mark.parametrize("sentences_fixture, names_fixture, expected_output", [
    ("sentences1", "names1", {  # Igor Karkaroff mentioned 3 times
        "Question 3": {
            "Name Mentions": [
                ["igor karkaroff", 3]
            ]
        }
    }),
    ("sentences2", "names2", {  # Harry Potter mentioned once
        "Question 3": {
            "Name Mentions": [
                ["harry potter", 1]
            ]
        }
    }),
    ("sentences3", "names3", {  # No mentions found
        "Question 3": {
            "Name Mentions": []
        }
    })
])
def test_task3(sentences_fixture, names_fixture, expected_output, request, remove_words):
    """
    Test Task 3 using pytest fixtures to ensure fresh, independent test data.

    Args:
        sentences_fixture (str): Fixture name for sentence data.
        names_fixture (str): Fixture name for names data.
        expected_output (dict): Expected JSON output for assertion.
        request (pytest.FixtureRequest): Provides access to fixture values.
        remove_words (pd.DataFrame): Fixture for remove words dataset.
    """
    # Retrieve fresh data from fixtures
    sentences = request.getfixturevalue(sentences_fixture)
    names = request.getfixturevalue(names_fixture)

    # Execute Task 3 logic
    result = task3(sentences, names, remove_words)

    # Debugging info if assertion fails
    if result != expected_output:
        print("\n==== DEBUG INFO ====")
        print(f"Sentences Input:\n{sentences.to_dict()}")
        print(f"Names Input:\n{names.to_dict()}")
        print(f"\nExpected Output:\n{expected_output}")
        print(f"\nActual Output:\n{result}")
        print("====================\n")

    # Assert correctness
    assert json.dumps(result, sort_keys=True) == json.dumps(expected_output, sort_keys=True), \
        f"Mismatch for Task 3 using {sentences_fixture}, {names_fixture}"

@pytest.mark.parametrize("sentences_fixture, kseq_fixture, expected_output", [
    ("sentences1", "kseq_1", {  # Test with Sentences 1 and K-seq Query 1
        "Question 4": {
            "K-Seq Matches": [
                [
                    "karkaroff",
                    [
                        ["karkaroff", "hovered", "behind", "snape", "desk", "rest", "double", "period"],
                        ["karkaroff", "looked", "extremely", "worried", "snape", "looked", "angry"],
                        ["karkaroff", "seemed", "intent", "preventing", "snape", "slipping", "away", "class"]
                    ]
                ],
                [
                    "snape looked",
                    [
                        ["karkaroff", "looked", "extremely", "worried", "snape", "looked", "angry"]
                    ]
                ]
            ]
        }
    }),
    ("sentences2", "kseq_2", {  # Test with Sentences 2 and K-seq Query 2 (No Matches)
        "Question 4": {
            "K-Seq Matches": []
        }
    })
])
def test_task4(sentences_fixture, kseq_fixture, expected_output, request, remove_words):
    """
    Test Task 4 using pytest fixtures to ensure fresh, independent test data.

    Args:
        sentences_fixture (str): Fixture name for sentence data.
        kseq_fixture (str): Fixture name for K-seq query data.
        expected_output (dict): Expected JSON output for assertion.
        request (pytest.FixtureRequest): Provides access to fixture values.
        remove_words (pd.DataFrame): Fixture for remove words dataset.
    """
    # Retrieve fresh data from fixtures
    sentences = request.getfixturevalue(sentences_fixture)
    kseq_query = request.getfixturevalue(kseq_fixture)

    # Execute Task 4 logic
    result = task4(sentences, remove_words, kseq_query)

    # Debugging info if assertion fails
    if result != expected_output:
        print("\n==== DEBUG INFO ====")
        print(f"Sentences Input:\n{sentences.to_dict()}")
        print(f"K-seq Query Input:\n{kseq_query}")
        print(f"\nExpected Output:\n{expected_output}")
        print(f"\nActual Output:\n{result}")
        print("====================\n")

    # Assert correctness
    assert json.dumps(result, sort_keys=True) == json.dumps(expected_output, sort_keys=True), \
        f"Mismatch for Task 4 using {sentences_fixture}, {kseq_fixture}"

@pytest.mark.parametrize("sentences_fixture, names_fixture, max_k, expected_output", [
    ("sentences1", "names1", 3, {  # Test with Sentences 1, Names 1, max_k=3
        "Question 5": {
            "Person Contexts and K-Seqs": [
                [
                    "igor karkaroff",
                    [
                        ["angry"], ["away"], ["away", "class"], ["behind"], ["behind", "snape"], 
                        ["behind", "snape", "desk"], ["class"], ["desk"], ["desk", "rest"], ["desk", "rest", "double"], 
                        ["double"], ["double", "period"], ["extremely"], ["extremely", "worried"], ["extremely", "worried", "snape"], 
                        ["hovered"], ["hovered", "behind"], ["hovered", "behind", "snape"], ["intent"], ["intent", "preventing"], 
                        ["intent", "preventing", "snape"], ["karkaroff"], ["karkaroff", "hovered"], ["karkaroff", "hovered", "behind"], 
                        ["karkaroff", "looked"], ["karkaroff", "looked", "extremely"], ["karkaroff", "seemed"], ["karkaroff", "seemed", "intent"], 
                        ["looked"], ["looked", "angry"], ["looked", "extremely"], ["looked", "extremely", "worried"], ["period"], ["preventing"], 
                        ["preventing", "snape"], ["preventing", "snape", "slipping"], ["rest"], ["rest", "double"], ["rest", "double", "period"], 
                        ["seemed"], ["seemed", "intent"], ["seemed", "intent", "preventing"], ["slipping"], ["slipping", "away"], ["slipping", "away", "class"], 
                        ["snape"], ["snape", "desk"], ["snape", "desk", "rest"], ["snape", "looked"], ["snape", "looked", "angry"], ["snape", "slipping"], 
                        ["snape", "slipping", "away"], ["worried"], ["worried", "snape"], ["worried", "snape", "looked"]
                    ]
                ]
            ]
        }
    }),
    ("sentences2", "names2", 4, {  # Test with Sentences 2, Names 2, max_k=4
        "Question 5": {
            "Person Contexts and K-Seqs": [
                [
                    "harry potter",
                    [
                        ["curtly"], ["harry"], ["harry", "curtly"], ["urgent"], 
                        ["urgent", "harry"], ["urgent", "harry", "curtly"]
                    ]
                ]
            ]
        }
    }),
    ("sentences3", "names3", 5, {  # Test with Sentences 3, Names 3, max_k=5 (No Matches)
        "Question 5": {
            "Person Contexts and K-Seqs": []
        }
    })
])
def test_task5(sentences_fixture, names_fixture, max_k, expected_output, request, remove_words):
    """
    Test Task 5 using pytest fixtures to ensure fresh, independent test data.

    Args:
        sentences_fixture (str): Fixture name for sentence data.
        names_fixture (str): Fixture name for names data.
        max_k (int): Maximum length for K-sequences.
        expected_output (dict): Expected JSON output for assertion.
        request (pytest.FixtureRequest): Provides access to fixture values.
        remove_words (pd.DataFrame): Fixture for remove words dataset.
    """
    # Retrieve fresh data from fixtures
    sentences = request.getfixturevalue(sentences_fixture)
    names = request.getfixturevalue(names_fixture)

    # Execute Task 5 logic
    result = task5(sentences, names, remove_words, max_k)

    # Debugging info if assertion fails
    if result != expected_output:
        print("\n==== DEBUG INFO ====")
        print(f"Sentences Input:\n{sentences.to_dict()}")
        print(f"Names Input:\n{names.to_dict()}")
        print(f"Max_k: {max_k}")
        print(f"\nExpected Output:\n{expected_output}")
        print(f"\nActual Output:\n{result}")
        print("====================\n")

    # Assert correctness
    assert json.dumps(result, sort_keys=True) == json.dumps(expected_output, sort_keys=True), \
        f"Mismatch for Task 5 using {sentences_fixture}, {names_fixture}, max_k={max_k}"

@pytest.mark.parametrize("sentences_fixture, names_fixture, windowsize, threshold, expected_output", [
    ("sentences5", "names5", 2, 2, {
        "Question 6": {
            "Pair Matches": [
                [["aberforth", "dumbledore"], ["aurelius", "dumbledore"]],
                [["aberforth", "dumbledore"], ["harry", "potter"]],
                [["aurelius", "dumbledore"], ["harry", "potter"]]
            ]
        }
    }),
("sentences6", "names6", 2, 1, {
        "Question 6": {
            "Pair Matches": [
                [["hermione","granger"],["isobel","mcgonagall"]]
            ]
        }
    })

])
def test_task6(sentences_fixture, names_fixture, windowsize, threshold, expected_output, request):
    """
    Test Task 6 using pytest fixtures to ensure fresh, independent test data.

    Args:
        sentences_fixture (str): Fixture name for sentence data.
        names_fixture (str): Fixture name for names data.
        windowsize (int): The window size for checking co-occurrence.
        threshold (int): Minimum occurrences for a valid pair.
        expected_output (dict): Expected JSON output for assertion.
        request (pytest.FixtureRequest): Provides access to fixture values.
        remove_words (pd.DataFrame): Fixture for remove words dataset.
    """
    # Retrieve fresh data from fixtures
    sentences = request.getfixturevalue(sentences_fixture)
    names = request.getfixturevalue(names_fixture)
    remove_words_df = request.getfixturevalue("remove_words")  # Retrieve remove words fixture

    # Execute Task 6 logic
    result = task6(sentences, names, remove_words_df, windowsize, threshold)

    # Debugging info if assertion fails
    if result != expected_output:
        print("\n==== DEBUG INFO ====")
        print(f"Sentences Input:\n{sentences.to_dict()}")
        print(f"Names Input:\n{names.to_dict()}")
        print(f"Windowsize: {windowsize}, Threshold: {threshold}")
        print(f"\nExpected Output:\n{expected_output}")
        print(f"\nActual Output:\n{result}")
        print("====================\n")

    # Assert correctness
    assert json.dumps(result, sort_keys=True) == json.dumps(expected_output, sort_keys=True), \
        f"Mismatch for Task 6 using {sentences_fixture}, {names_fixture}, windowsize={windowsize}, threshold={threshold}"

@pytest.mark.parametrize("sentences_fixture, names_fixture, pairs_fixture, windowsize, threshold, maximal_distance, expected_output", [
    # First test case: using sentences5, names5, pairs1
    ("sentences5", "names5", "pairs1", 3, 2, 1000, {
        "Question 7": {
            "Pair Matches": [
                ["aurelius dumbledore", "harry potter", True],
                ["draco malfoy", "hermione granger", False],
                ["harry potter", "hermione granger", False]
            ]
        }
    }),

    # Second test case: using sentences6, names6, pairs2
    ("sentences6", "names6", "pairs2", 5, 1, 1000, {
        "Question 7": {
            "Pair Matches": [
                ["aurelius dumbledore", "otto bagman", False],
                ["draco malfoy", "hermione granger", False],
                ["harry potter", "hermione granger", False]
            ]
        }
    })
])
def test_task7(sentences_fixture, names_fixture, pairs_fixture, windowsize, threshold, maximal_distance, expected_output, request, remove_words):
    """
    Test Task 7 using pytest fixtures to ensure fresh, independent test data.

    Args:
        sentences_fixture (str): Fixture name for sentence data.
        names_fixture (str): Fixture name for names data.
        pairs_fixture (str): Fixture name for relationship pairs.
        windowsize (int): Window size for checking co-occurrence.
        threshold (int): Minimum occurrences for a valid pair.
        maximal_distance (int): Maximum allowed distance for relationship connection.
        expected_output (dict): Expected JSON output for assertion.
        request (pytest.FixtureRequest): Provides access to fixture values.
        remove_words (pd.DataFrame): Fixture for remove words dataset.
    """
    # Retrieve fresh test data from fixtures
    sentences = request.getfixturevalue(sentences_fixture)
    names = request.getfixturevalue(names_fixture)
    pairs = request.getfixturevalue(pairs_fixture)

    # Execute Task 7 logic
    result = task7(sentences, names, remove_words, windowsize, threshold, pairs, maximal_distance)

    # Debugging output if the test fails
    if result != expected_output:
        print("\n==== DEBUG INFO ====")
        print(f"Sentences Input:\n{sentences.to_dict()}")
        print(f"Names Input:\n{names.to_dict()}")
        print(f"Pairs Input:\n{pairs}")
        print(f"Windowsize: {windowsize}, Threshold: {threshold}, Maximal Distance: {maximal_distance}")
        print(f"\nExpected Output:\n{expected_output}")
        print(f"\nActual Output:\n{result}")
        print("====================\n")

    # Assert correctness
    assert json.dumps(result, sort_keys=True) == json.dumps(expected_output, sort_keys=True), \
        f"Mismatch for Task 7 using {sentences_fixture}, {names_fixture}, {pairs_fixture} with windowsize={windowsize}, threshold={threshold}, maximal_distance={maximal_distance}"


@pytest.mark.parametrize("sentences_fixture, names_fixture, pairs_fixture, windowsize, threshold, fixed_length, expected_output", [
    # First test case: using sentences5, names5, pairs1
    ("sentences5", "names5", "pairs1", 5, 2, 2, {
        "Question 8": {
            "Pair Matches": [
                ["aurelius dumbledore", "harry potter", True],
                ["draco malfoy", "hermione granger", False],
                ["harry potter", "hermione granger", False]
            ]
        }
    }),

    # Second test case: using sentences6, names6, pairs2
    ("sentences6", "names6", "pairs2", 5, 2, 6, {
        "Question 8": {
            "Pair Matches": [
                ["aurelius dumbledore", "otto bagman", False],
                ["draco malfoy", "hermione granger", False],
                ["harry potter", "hermione granger", False]
            ]
        }
    })
])
def test_task8(sentences_fixture, names_fixture, pairs_fixture, windowsize, threshold, fixed_length, expected_output, request, remove_words):
    """
    Test Task 8 using pytest fixtures to ensure fresh, independent test data.

    Args:
        sentences_fixture (str): Fixture name for sentence data.
        names_fixture (str): Fixture name for names data.
        pairs_fixture (str): Fixture name for relationship pairs.
        windowsize (int): Window size for checking co-occurrence.
        threshold (int): Minimum occurrences for a valid pair.
        fixed_length (int): The length of the output sequence.
        expected_output (dict): Expected JSON output for assertion.
        request (pytest.FixtureRequest): Provides access to fixture values.
        remove_words (pd.DataFrame): Fixture for remove words dataset.
    """
    # Retrieve fresh test data from fixtures
    sentences = request.getfixturevalue(sentences_fixture)
    names = request.getfixturevalue(names_fixture)
    pairs = request.getfixturevalue(pairs_fixture)

    # Execute Task 8 logic
    result = task8(sentences, names, remove_words, windowsize, threshold, pairs, fixed_length)

    # Debugging output if the test fails
    if result != expected_output:
        print("\n==== DEBUG INFO ====")
        print(f"Sentences Input:\n{sentences.to_dict()}")
        print(f"Names Input:\n{names.to_dict()}")
        print(f"Pairs Input:\n{pairs}")
        print(f"Windowsize: {windowsize}, Threshold: {threshold}, Fixed Length: {fixed_length}")
        print(f"\nExpected Output:\n{expected_output}")
        print(f"\nActual Output:\n{result}")
        print("====================\n")

    # Assert correctness
    assert json.dumps(result, sort_keys=True) == json.dumps(expected_output, sort_keys=True), \
        f"Mismatch for Task 8 using {sentences_fixture}, {names_fixture}, {pairs_fixture} with windowsize={windowsize}, threshold={threshold}, fixed_length={fixed_length}"


@pytest.mark.parametrize("sentences_fixture, threshold, expected_output", [
    # First test case: using sentences1 with threshold 1
    ("sentences1", 1, {
        "Question 9": {
            "group Matches": [
                [
                    "Group 1",
                    [
                        ["harry", "deliberately", "knocked", "bottle", "delay", "snape"],
                        ["karkaroff", "hovered", "behind", "snape", "desk", "rest", "double", "period"],
                        ["karkaroff", "looked", "extremely", "worried", "snape", "looked", "angry"],
                        ["karkaroff", "seemed", "intent", "preventing", "snape", "slipping", "away", "class"]
                    ]
                ]
            ]
        }
    }),

    # Second test case: using sentences2 with threshold 3
    ("sentences2", 3, {
        "Question 9": {
            "group Matches": [
                ["Group 1", [["ooooh", "urgent", "gargoyle", "high", "pitched", "voice", "well", "us", "place", "hasn"]]],
                ["Group 2", [["urgent", "harry", "curtly"]]]
            ]
        }
    }),

    # Third test case: using sentences6 with threshold 2 (Updated)
    ("sentences6", 2, {
        "Question 9": {
            "group Matches": [
                ["Group 1", [["exactly", "hermione", "slowly"]]],
                ["Group 2", [["gargoyle", "high", "pitched", "voice"]]],
                ["Group 3", [["given", "another", "detention"]]],
                ["Group 4", [["harry", "heard", "footsteps", "door", "opened", "harry", "harry", "face", "face", "professor", "mcgonagall"]]],
                ["Group 5", [["harry", "knocked"]]],
                ["Group 6", [["mcgonagall", "mcgonagall", "square", "spectacles", "flashing", "alarmingly"]]],
                ["Group 7", [["ooooh", "urgent"]]],
                ["Group 8", [["ron", "indignantly"]]],
                ["Group 9", [["urgent", "harry", "curtly"]]],
                ["Group 10", [["ve", "really", "annoying", "hadn", "explained", "properly"]]],
                ["Group 11", [["well", "clears", "ron"]]],
                ["Group 12", [["well", "us", "place", "hasn"]]],
                ["Group 13", [["wondering"]]],
                ["Group 14", [["aren", "harry", "ron", "looked"], ["harry", "ron", "together"], ["hermione", "looked", "ron", "hermione", "realised", "ron"]]],
                ["Group 15", [["hermione", "group", "idea", "place"], ["suppose", "re", "right"], ["wondering", "hermione", "hermione", "voice", "stronger", "whether", "re", "right", "starting", "defence", "dark", "arts", "group"]]]
            ]
        }
    })
])
def test_task9(sentences_fixture, threshold, expected_output, request, remove_words):
    """
    Test Task 9 using pytest fixtures to ensure fresh, independent test data.

    Args:
        sentences_fixture (str): Fixture name for sentence data.
        threshold (int): Threshold for grouping words.
        expected_output (dict): Expected JSON output for assertion.
        request (pytest.FixtureRequest): Provides access to fixture values.
        remove_words (pd.DataFrame): Fixture for remove words dataset.
    """
    # Retrieve fresh test data from fixtures
    sentences = request.getfixturevalue(sentences_fixture)


    # Execute Task 9 logic
    result = task9(sentences, remove_words, threshold)

    # Debugging output if the test fails
    if result != expected_output:
        print("\n==== DEBUG INFO ====")
        print(f"Sentences Input:\n{sentences.to_dict()}")
        print(f"Threshold: {threshold}")
        print(f"\nExpected Output:\n{expected_output}")
        print(f"\nActual Output:\n{result}")
        print("====================\n")

    # Assert correctness
    assert json.dumps(result, sort_keys=True) == json.dumps(expected_output, sort_keys=True), \
        f"Mismatch for Task 9 using {sentences_fixture} with threshold={threshold}"
