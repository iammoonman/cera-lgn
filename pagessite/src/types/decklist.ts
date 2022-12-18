export type Decklist = {
    playerID: string;
    cardList: string[];
    eventID?: number;
    deckName?: string; // Defaults to "Untitled Deck"
    sideboard?: string[]; // Additional optional text input
}

// TTS module exports a list of oracle_ids from memo
// User copies text and pastes it into the modal.
// Maximum length for text in modal is 4000 chars, which is just barely enough for 110 lines

// Modal dropdown for eventID listing the event name as label.

// Error message in TTS if the card doesnt have an oracle_id
// Error message in TTS if the output would be longer than 4000