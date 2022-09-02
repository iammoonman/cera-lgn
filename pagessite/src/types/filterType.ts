import type { CardDisplayType } from "./displaycard";
import type { Draft } from "./events";

export type FilterObject = {
    label: string;
    active: boolean;
    condition: (x: (CardDisplayType | Draft)) => boolean;
}