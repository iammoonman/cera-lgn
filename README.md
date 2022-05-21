# cera

## Blurb
The packcreator project recreates Magic: The Gathering draft booster pack generation to the highest fidelity possible with current information. It outputs these packs through Discord to a format usable by Tabletop Simulator.</br>
The drafthandler project is an event manager, using Discord to handle pairings for Magic: The Gathering draft events. The data is output to a somewhat human-readable JSON format intended to be usable by other projects.</br>

## Credits
Thanks to the [lethe.xyz](https://www.lethe.xyz/mtg/collation/index.html) collation project for the collation data. This project is not affiliated with them, though. Consider donating to their Patreon.</br>
Thanks to Scryfall for the card data. This project is not affiliated with them either.</br>
Thanks to CubeCobra for hosting cubes and doing what they do. This project is also not affiliated with them.</br>
Thanks to Wizards of the Coast, as this project technically involves their intellectual property. As far as I am aware, I'm not violating any rules or laws with this project, and it is not affiliated with the company. Do not use this project to avoid having a Magic: The Gathering experience in paper, MTGO, or Arena. Frankly, this project is not an exact replica of real booster packs or the tournament rules, and the real thing is worth your money.</br>
Thanks to Discord, and of course this project isn't affiliated with them.

## Additional Notes
Nearly all rare sheets are randomly generated on JSON. These cannot realistically be reverse engineered.</br>
Some sets' information is currently unavailable. It is possible to reverse engineer more sets' contents, but it takes a lot of work and patience.</br>
The Discord bots use discord.py and pycord as API wrappers.

## V2 Set File Structure
```
{
    "set_code": "abc"          <--- // Three character set code.
                                    // Used for every card in the pack,
                                    // except those pulled from the extras_sheets_odds.
    "distributions_odds": [
        [ {"c": 10}, 0.8 ],    <--- // This pack outline has an 80% chance of occurring.
                                    // The pack will contain 10 commons and nothing else.
        [{
            "c": 9,            <--- // For commons and uncommons, this number helps
                                    // identify what should be in the drops section.
                                    // The key determines what sheets are in the pack.
            "f": 1,            <--- // Foils, rares, and the extra slot do
                                    // care about the number.
            "drops": {"c": 1}  <--- // One random sheet from the ABCD_commons will
                                    // have the number of cards it adds to the pack reduced
                                    // by one to make room for the additional foil.
        }, 0.2],
    ],
    "ABCD_commons_odds":[
        [
            [ {"a": 2}, 1.0 ], <--- // This selection of commons will take
                                    // two cards from the commons' A sheet.
            [ {"b": 2}, 1.0 ]       // It has an equal chance of being chosen
                                    // against the other ABCD.
        ]
    ]
    "ABCD_common_sheets": {
        "a": [ "1", "2" ],     <--- // The A common sheet, in order.
        "b": [ "3", "4" ]
    },
    "ABCD_uncommon_odds": [ ... ],  // Identical to the ABCD_commons_odds.
    "ABCD_uncommon_sheets": { ... },// Identical to the ABCD_commons_sheets.
    "rare_slot_odds": [ ... ],      // Identical to the ABCD_commons_odds.
    "rare_slot_sheets": { ... },    // Identical to the ABCD_commons_sheets.
    "foil_sheets_odds": [
        [ ["5", "6"], 1.0 ]    <--- // This list of foils has a 100% chance of
                                    // having a card taken from it,
                                    // if there is an "f" in the distribution.
    ],
    "extras_sheets_odds": {
        "special": [           <--- // Put "special" or any namespace other
                                    // than c, u, r, or f to identify this slot.
            [ ["7"], ["8"] ],       // Then identify the sheets and
            [  1.0 ,  1.0  ],       // their odds of being chosen,
            "def"                   // along with their set code.
        ]
    }
}
```

## V3 Set File Structure

```
{
    "default_set": "abc",                       <---    // Default set code,
                                                        // listed to save space.
    "distros": [
        {
            "slots": { "c": 9, "u": 3, "r": 1, "f": 1 },// Identifies which slots and
                                                        // how many cards from that slot
                                                        // will be taken.
            "drops": [
                { "slot": "c", "key": "b", "count": 1 } // Identifies the slot and sheet key
                                                        // for cards dropped to make room
                                                        // for other slots.
            ],
            "freq": 1.0                         <---    // The odds that this outline will
                                                        // be chosen for the pack.
        },
        { ... }
    ],
    "slots": {
        "c": {
            "flags": [],                                // Identifies control options for
                                                        // the slot, if any.
            "options": [
                {
                    "struct": {"a": 1, "b": 2},         // This layout takes one card from
                                                        // the slot's "a" sheet and two
                                                        // from the "b" sheet.
                    "freq"  : 0.9
                },
                { ... }
            ],
            "sheets": {
                "a": [                          <---    // Contains the "a" sheet, in order.
                    [ "1", "def" ],             <---    // The first is collector number,
                                                        // the second is the set code.
                                                        // These two combined identify any
                                                        // unique Magic card.
                      "2"                       <---    // A lone string will use the
                                                        // default set code above.
                ],
                "b": [ ... ]
            }
        },
        "u": { ... },
        "r": { ... },
        "f": { "flags": [ "foil" ], ... }       <---    // All of the cards will be foiled.
    },
    "flag_data": {
        "duplicate_control": { ... },                   // Consult the wiki page
        "sequenced"        : { ... }                    // for future flag options.
    }
}
```
