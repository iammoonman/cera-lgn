export type LimitedEvent = {
    id: number;
    tag: 'ptm' | 'omn' | 'dps' | '';
    date: Date;
    title: string;
}

export type Draft = {
    scores: Score[];
    rounds: Round[];
    description?: string;
} & LimitedEvent;

export type Score = {
    id: number;
    points: number;
    gwp: number;
    ogp: number;
    omp: number;
}

export type Round = {
    r_id: number;
    title?: string;
    matches: Match[];
}

export type Match = {
    p_ids: number[];
    games: Map<number, number | 'TIE'>; // Map<game_num, winner_id>
    bye: boolean;
    drops: number[];
}

export type TScore = {
    wins: number;
    losses: number;
    ties: number;
    seed: number;
    rank: number;
} & Score;

export type TMatch = {
    b_id: number;
    r_num: number;
    feeds: Map<number, number>; // Map<placement_number, node_id>
} & Match;

export type Tournament = {
    scores: TScore[];
    matches: TMatch[];
} & LimitedEvent;

type oldtype = {
    draftID: string;
    tag: string;
    date: string;
    title: string;
    rounds: {
        roundNUM: string;
        completed: boolean;
        matches: {
            players: string[];
            scores: number[];
        }[];
    }[];
    players: {
        playerID: string;
        score: number;
        gwp: number;
        ogp: number;
        omp: number;
    }[];
}

export function old_to_new(a: oldtype): Draft {
    const newTag = ['ptm', 'omn', 'dps', ''].includes(a.tag) ? a.tag as 'ptm' | 'omn' | 'dps' | '' : '';
    return { scores: a.players.map((p) => { return { id: parseInt(p.playerID), points: p.score, gwp: p.gwp, ogp: p.ogp, omp: p.omp } }), date: new Date(), id: parseInt(a.draftID), rounds: [], tag: newTag, title: a.title }
}