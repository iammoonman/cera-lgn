export type Save = {
    ObjectStates: (TTSBag | TTSDeck | TTSCard)[];
}

export type TTSBag = {
    Name: "Bag";
    Transform: Transform;
    Nickname: string;
    ColorDiffuse: ColorDiffuse;
    Bag: { Order: 0 }
    ContainedObjects: (TTSDeck | TTSCard)[];
}
export type TTSDeck = {
    Name: "Deck";
    Transform: Transform;
    Nickname: string;
    ColorDiffuse: ColorDiffuse;
    DeckIDs: number[];
    CustomDeck: Record<string, CustomDeckObject>;
    ContainedObjects: TTSCard[];
}
export type TTSCard = {
    Name: "Card";
    Transform: Transform;
    Nickname: string;
    ColorDiffuse: ColorDiffuse;
    Memo: string;
    Description: string;
    CardID?: number;
    CustomDeck: Record<string, CustomDeckObject>;
    States: Record<number, TTSCard>;
    AttachedDecals?: Decal[];
    GMNotes?: string;
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
    Transform: Transform;
}

type Transform = { posX: number; posY: number; posZ: number; rotX: number; rotY: number; rotZ: number; scaleX: number; scaleY: number; scaleZ: number; }
type ColorDiffuse = { r: number; g: number; b: number }

export type CardWrapper = {
    id: string;
    card: TTSCard;
    highlighted: boolean;
};