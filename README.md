# cera

## Information
This project recreates Magic: The Gathering draft booster pack generation to the highest fidelity possible with current information. It also outputs these packs through Discord to a format usable by Tabletop Simulator.</br>
The project is also an event manager, using Discord to handle pairings for draft events. The data is output to a human-readable JSON format usable by other projects.  

Thanks to the [lethe.xyz](https://www.lethe.xyz/mtg/collation/index.html) collation project for the collation data. This project is not affiliated with them, though. Consider donating to their Patreon.</br>
Thanks to Scryfall for the card data. This project is not affiliated with them either.</br>
Thanks to Wizards of the Coast, as this project technically deals with their intellectual property. As far as I am aware, I'm not violating any rules or laws with this project. Do not use this project to avoid having a Magic: The Gathering experience in paper, MTGO, or Arena. The real thing is worth your money.  

#### Pickled files you might need:
- packcreator/token.pickle
- packcreator/pointer.pickle
- packcreator/counter.pickle
- packcreator/prevrares.pickle
- packcreator/sections.pickle
- drafthandler/token.pickle

#### Other required files:
- packcreator/packs.json

#### Missing info:
- Nearly all rare sheets are randomly generated on JSON. These cannot realistically be reverse engineered.
- Some sets' information is currently unavailable. We can reverse engineer more sets' contents, but it takes a lot of work and patience.
