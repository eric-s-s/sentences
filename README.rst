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

note to self on cx_freeze.  see this stack_overflow thing.

https://stackoverflow.com/questions/24195311/how-to-set-shortcut-working-directory-in-cx-freeze-msi-bundle

TODOS
=====

remove : generate_text, text_to_pdf, gui.go

change: setup.py, setup_cx_freeze.py

make: guimain, commandline simple tool