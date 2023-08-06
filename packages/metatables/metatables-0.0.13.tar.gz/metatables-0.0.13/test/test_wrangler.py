from metatables import Student


def test_Student():
    assert Student(
        fname='Joe', lname='Martinez', semester=7
    ).return_greeting() == "Welcome Joe Martinez to the 7. semester!"
