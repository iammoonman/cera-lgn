export type CardDisplayType = {
    id: number;
    title: string;
    description?: string;
    set: string;
    cn: string;
    uri?: string;
    p_id: string; // The card's owner.
}