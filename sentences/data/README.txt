sentences v2.1
==============

This module creates randomly generated paragraphs and then assigns specific
kinds of errors to those paragraphs. It outputs this text to a pdf file.

GUI options details
-------------------

- MAIN OPTIONS
    - "Save current settings": Saves the current setting to the config file.
                               They will be set at startup.
    - "Reset to saved settings": Reloads the config file.
    - "Update from word files": If you altered the CSV files containing your
                                pool of countable nouns, uncountable nouns
                                and verbs, this will reload those files into
                                the app.
    - "New default word files": Moves "nouns.csv", "verbs.csv" and
                                "uncountable.csv" to new locations (such as
                                "nouns_old_01.csv") and then copies the default
                                word files.
    - "Factory Reset": overwrites the config file and default word files
                       without saving them.
    - "Make me some PDFs": Creates an error file and an answer file in your
                           save_folder.

- FILE MANAGEMENT OPTIONS: Set where to save files, and where
                           the word lists are located.
    - Customising word lists: You can customize your word lists. Use the defaults
                              as templates, or simply edit the default. Then use
                              "New default word files" to move your changed files and make new defaults.
    - Each "SET" button allows you to choose the location of the file.

- ERROR OPTIONS: Choose the frequency of errors and what kinds of errors occur.
    - "% chance for error": The chance that any one word or punctuation will
                            get a grammatical error.
    - "noun errors": Errors such as: "a water", "the rices", "cat"
                     (no article or plural ending), "a cats"
    - "verb errors": Mixing up third-person an non-third-person endings.
                     Swapping tenses.
    - "is do errors": Changing "subj VERB" to "subj. BE-VERB infinitive"
                     (He plays. -> He is play.)
    - "transpose preposition errors": Putting the prepositional phrase between
                                      subject and verb ("He with a cat plays.")
    - "period errors": Changing period and capital letter to
                       comma and lower-case letter (without a conjunction)

- PARAGRAPH TYPE OPTIONS: Choose size of paragraph, how many
                          paragraph and how subjects are selected.
    - "choose a paragraph type": Determines the algorithm
                                 for selecting subjects.
        - "pool": Creates a pool of subjects of size: "subject pool size".
                  Each sentence randomly selects a subject from the pool.
        - "chain": The object of the previous sentence becomes
                   the subject of the current sentence.
    - "number of paragraphs": How many paragraphs are in the PDFs.
    - "sentences per paragraph": How many sentences in each paragraph.
    - "subject pool size": The size of the subject pool. If "chain"
                           is selected, this is ignored.

- PARAGRAPH GRAMMAR OPTIONS:
    - "choose a tense": Determines if your paragraphs are in simple
                        present tense or simple past tense.
    - "% chance of plural noun": The probability that any countable noun
                                 will be assigned as plural.
    - "% chance of negative verb": The probability that any verb will be
                                   assigned as negative (go -> don't go).
    - "% chance of pronoun": The probability that any subject or object
                             will be a randomly selected pronoun.
