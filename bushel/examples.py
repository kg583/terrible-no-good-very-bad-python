import bushel


with (
    bushel.BushelServer("localhost", port=25) as server,
    12/21/2022 as date,
    user@example.com as sender,
    user@example.com as recipient,
    "Greetings from Bushel!" as subject,

    README.md as attachment,
):
    """
    Hello!
    
    This message was sent to your address by a NEW, state-of-the-art email system called Bushel.
    Bushel utilizes simple syntax built on pure Python to make composing and sending emails easier than ever before.
    
    Want a demo? Head over to https://github.com/kg583/terrible-no-good-very-bad-python/tree/main/bushel today!
    
    Best,
    The Bushel Team
    """