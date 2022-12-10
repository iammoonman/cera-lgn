import type { Save } from "./tts";

export type Decklist = {
    // Save is a bag with two decks; first deck is the deck, second deck is the rest of the pool.
    save: Save;
    eventID: number;
    playerID: number;
    pickOrder?: unknown[];
}
// TTS module to save the deck and pool, adding notations in GMNotes for "important cards"
// and give a deckname
// Right click a draft message to upload the file, appends that message id as the draft id
// and the user id as playerid

export type PickPack = {
    pick: string;
    pack: PickCard[];
}

export type PickCard = {
    name: string;
    image_url?: string; // Might need to pass when the user uploads to CERA
    oracle_id?: string; // Comes from Memo
    decal_url?: string;
    description?: string;
}