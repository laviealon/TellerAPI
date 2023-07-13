import pytest


def test_decrypt_account_number():
    from teller_api import decrypt_account_number
    exp_key = decrypt_account_number(cipher_data='J5ZCafuSAb6Q3xtd:nNYZsAzpb/g4XdrnIJB75/4K2Oa7MBan0wEiINZunEY=:6impTEbrlHUr4+5HzWBNVA==', enc_key='ewogICJjaXBoZXIiOiAiQUVBRC0yNTYtR0NNKHVzZXJuYW1lKSIsCiAgImZvcm1hdCI6ICJjdDppdjp0IiwKICAia2V5IjogImZvdXFaMzJYTG9RakJSOTErQUFtUDZWNGdKcGdXUnZHTUcvZG5QeUxmL0U9Igp9')
    act_key = 'fouqZ32XLoQjBR91+AAmP6V4gJpgWRvGMG/dnPyLf/E='
    assert exp_key == act_key




