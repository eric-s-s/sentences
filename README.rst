sentences
=========

This is a module for randomly generating sentences with random errors about tenses, nouns and punctuation.

It relies on Word, Noun and BasicVerb. They can call the methods return the class, and they all have the property
`value` that returns a str.  Noun and BasicVerb have other methods.

**Be careful with capitalize!** It returns the same type of object, but if it is not the last method called, it can
give odd results.
:code:`BasicVerb('eat', 'ate').capitalize().past_tense() != BasicVerb('eat', 'ate').past_tense().capitalize()`

**Be more careful with Word.bold()!** It currently only ever returns a Word. It is only intended to be used as a last
step.

It is in its very early stages and this README will be updated if there's anything happening.