import typing
import urllib.parse
import aiohttp

from .platform import Platform

_english_pronouns: dict[str, list[str]] = {
    "unspecified": [],
    "hh": ["he", "him"],
    "hi": ["he", "it"],
    "hs": ["he", "she"],
    "ht": ["he", "they"],
    "ih": ["it", "he"],
    "ii": ["it", "its"],
    "is": ["it", "she"],
    "it": ["it", "they"],
    "shh": ["she", "he"],
    "sh": ["she", "her"],
    "si": ["she", "it"],
    "st": ["she", "they"],
    "th": ["they", "he"],
    "ti": ["they", "it"],
    "ts": ["they", "she"],
    "tt": ["they", "them"],
    "any": ["any"],
    "other": ["other"],
    "ask": ["ask"],
    "avoid": ["use name"],
}


async def lookup(platform: Platform, identifiers: typing.Union[str, int, list[str], list[int]]) -> typing.Union[dict[str, list[str]], dict[int, list[str]]]:
    """
    Sends a request to the PronounDB API to get the pronouns of one or multiple users.

    :param platform: One of the supported platforms (see the Platform enum)
    :param identifiers: Account IDs on the platform (max 50)
    :return: The pronouns of the users as a list of all the pronouns the users use
    """

    if isinstance(identifiers, list) and len(identifiers) == 1:
        identifiers = identifiers[0]

    if isinstance(identifiers, list):
        return await _lookup_bulk(platform, identifiers)
    else:
        return await _lookup_single(platform, identifiers)


async def _lookup_single(platform: Platform, identifier: typing.Union[str, int]) -> typing.Union[dict[str, list[str]], dict[int, list[str]]]:
    """
    Sends a request to the PronounDB API to get the pronouns of a user.

    :param platform: One of the supported platforms (see the Platform enum)
    :param identifier: Account ID on the platform
    :return: The pronouns of the user as specified in the PronounDB docs
    """

    async with aiohttp.ClientSession() as session:
        async with session.get("https://pronoundb.org/api/v1/lookup?platform={0}&id={1}".format(
                platform.value,
                urllib.parse.quote_plus(str(identifier))
        )) as resp:
            data = await resp.json()

            if "error" in data:
                raise ValueError(f'{data["error"]}: {data["message"]}')

            return {identifier: _english_pronouns[data["pronouns"]]}


async def _lookup_bulk(platform: Platform, identifiers: typing.Union[list[str], list[int]]) -> typing.Union[dict[str, list[str]], dict[int, list[str]]]:
    """
    Sends a request to the PronounDB API to get the pronouns of multiple users, 50 max.

    :param platform: One of the supported platforms (see the Platform enum)
    :param identifiers: A list of account IDs on the platform
    :return: A dict with the account IDs as keys and the pronouns as values
    """

    if len(identifiers) > 50:
        raise ValueError("You can only lookup 50 users at once.")

    async with aiohttp.ClientSession() as session:
        async with session.get("https://pronoundb.org/api/v1/lookup-bulk?platform={0}&ids={1}".format(
                platform.value,
                urllib.parse.quote_plus(','.join(map(str, identifiers)))
        )) as resp:
            data = await resp.json()

            if "error" in data:
                raise ValueError(f'{data["error"]}: {data["message"]}')

            return {identifier: _english_pronouns[data[str(identifier)]] for identifier in identifiers}
