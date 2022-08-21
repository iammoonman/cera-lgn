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
    return {
        scores: a.players.map((p) => {
            return { id: parseInt(p.playerID), points: p.score, gwp: p.gwp, ogp: p.ogp, omp: p.omp }
        }),
        date: new Date(),
        id: parseInt(a.draftID),
        rounds: a.rounds.map((r, i) => {
            return {
                r_id: i,
                title: r.roundNUM,
                matches: r.matches.map((m) => {
                    return { p_ids: m.players.map(x => parseInt(x)), games: new Map(m.players.map((p, i) => [parseInt(p), m.scores[i]])), bye: m.players.find(x => x === "0")?.length == 0 ?? false, drops: [] }
                })
            }
        }),
        tag: newTag,
        title: a.title
    }
}

export function new_to_json(a: Draft) {
    return {
        ...a,
        date: a.date.toISOString(),
        rounds: a.rounds.map(r => {
            return {
                ...r, matches: r.matches.map(m => {
                    return { ...m, games: Object.fromEntries([...m.games]) }
                })
            }
        })
    }
}

export function json_to_new(a: {
    date: string;
    rounds: {
        matches: {
            games: {
                [k: string]: number | "TIE";
            };
            p_ids: number[];
            bye: boolean;
            drops: number[];
        }[];
        r_id: number;
        title?: string | undefined;
    }[];
    scores: Score[];
    description?: string | undefined;
    id: number;
    tag: "" | 'ptm' | 'omn' | 'dps';
    title: string;
}): Draft {
    return {
        ...a,
        date: new Date(),
        rounds: a.rounds.map(r => {
            return {
                ...r, matches: r.matches.map(m => {
                    return { ...m, games: new Map(Object.entries(m.games).map(([a, b]) => [parseInt(a), b])) }
                })
            }
        })
    }
}