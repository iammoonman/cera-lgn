export type Save = {
    ObjectStates: (TTSBag | TTSDeck | TTSCard)[];
}

export type TTSBag = {
    Name: "Bag";
    Transform: string;
    Nickname: string;
    ColorDiffuse: { r: number, g: number, b: number };
    Bag: { Order: 0 }
    ContainedObjects: (TTSDeck | TTSCard)[];
}
export type TTSDeck = {
    Name: "Deck";
    Transform: string;
    Nickname: string;
    ColorDiffuse: { r: number, g: number, b: number };
    DeckIDs: number[];
    CustomDeck: Record<number, CustomDeckObject>;
    ContainedObjects: TTSCard[];
}
export type TTSCard = {
    Name: "Card";
    Transform: string;
    Nickname: string;
    ColorDiffuse: { r: number, g: number, b: number };
    Memo: string;
    Description: string;
    CardID: number;
    CustomDeck: Record<number, CustomDeckObject>;
    States: Record<number, TTSCard>;
    AttachedDecals?: Decal[];
}

export type CustomDeckObject = {
    FaceURL: string;
    BackURL: string;
    NumWidth: number;
    NumHeight: number;
    BackIsHidden: boolean;
    UniqueBack: boolean;
}

export type Decal = {
    CustomDecal: { Name: string; ImageURL: string; Size: number };
    Transform: { posX: number; posY: number; posZ: number; rotX: number; rotY: number; rotZ: number }
}