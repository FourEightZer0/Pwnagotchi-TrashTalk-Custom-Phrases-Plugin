![Screenshot](Screenshot.png)
![Screenshot](Screenshot2.png)

This plugin is designed to work with jayofelony Pwnagotchi 2.9.5.4

# Nomagotchi

A Pwnagotchi plugin that Allows you to easily customize your Pwnagotchi's phrases

## Install

1. Copy `trashtalk.py` to your Pwnagotchi custom plugins directory:

   - Typical path: `/usr/local/share/pwnagotchi/custom-plugins/trashtalk.py`

2. Add the following to your `config.toml`:

```toml
main.custom_plugins = "/etc/pwnagotchi/custom-plugins"
main.plugins.trashtalk.enabled = true

main.plugins.trashtalk.phrases.on_starting = [
  "Tiny gremlin online.",
  "Boot sequence complete.",
  "Ready to sniff trouble."
]

main.plugins.trashtalk.phrases.on_assoc = [
  "Yo {what}, let me in.",
  "Associating with {what}.",
  "Knocking on {what}."
]

main.plugins.trashtalk.phrases.on_deauth = [
  "Bye {mac}.",
  "Removing Wi-Fi privileges for {mac}.",
  "Disconnecting {mac}."
]

main.plugins.trashtalk.phrases.on_handshakes = [
  "Nice, got {num} handshake{plural}.",
  "Captured {num} fresh handshake{plural}.",
  "That worked: {num} handshake{plural}."
]

main.plugins.trashtalk.phrases.on_waiting = [
  "Lurking for {secs}s ...",
  "Being suspicious for {secs}s ..."
]

main.plugins.trashtalk.phrases.on_uploading = [
  "Sending loot to {to} ...",
  "Uploading goodies to {to} ..."
]

```

3. Restart Pwnagotchi.
