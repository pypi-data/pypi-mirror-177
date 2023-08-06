# PronounDB Python API

Python API for the PronounDB API.

## Installation

```bash
pip install pronoundb
```

## Examples

lookup someones pronouns by their discord id:

```py
from pronoundb import lookup, Platform

lookup(Platform.DISCORD, 123456789012345678)
# -> {123456789012345678: ["he", "him"]}
```

lookup someones pronouns by their minecraft (java) uuid:

```py
from pronoundb import lookup, Platform

lookup(Platform.MINECRAFT, "12345678-1234-1234-1234-123456789012")
# -> {"12345678-1234-1234-1234-123456789012": ["they", "them"]}
```

lookup multiple users pronouns by their discord id:

```py
from pronoundb import lookup, Platform

lookup(Platform.DISCORD, [123456789012345678, 987654321098765432])
# -> {123456789012345678: ["he", "him"], 987654321098765432: ["she", "her"]}
```

## Supported Platforms

- Discord
- Facebook
- GitHub
- Minecraft (Java)
- Twitch
- Twitter

## Contributing

Contributions to this library are always welcome and highly encouraged.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
