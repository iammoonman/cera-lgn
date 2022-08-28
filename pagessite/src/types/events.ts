export type LimitedEvent = {
    id: number;
    tag: 'ptm' | 'omn' | 'dps' | '';
    date: Date;
    title: string;
}

export type Draft = {
    scores: Score[];
    rounds: Map<number, Round>;
    description?: string;
} & LimitedEvent;

export type Score = {
    id: string;
    points: number;
    gwp: number;
    ogp: number;
    omp: number;
}

export type Round = {
    title?: string;
    matches: Match[];
}

export type Match = {
    p_ids: string[];
    games: Map<number, string | 'TIE'>; // Map<game_num, winner_id>
    bye: boolean;
    drops: string[];
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
            return { id: p.playerID, points: p.score, gwp: p.gwp, ogp: p.ogp, omp: p.omp }
        }),
        date: new Date(),
        id: parseInt(a.draftID),
        rounds: new Map(a.rounds.map((r, i) => {
            return [i, {
                title: r.roundNUM,
                matches: r.matches.map((m) => {
                    const newGames: Map<number, string> = new Map([])
                    // m.scores = [0, 2] | [2, 0] | [1, 2] | [2, 1]
                    if (m.scores == [0, 2]) {
                        newGames.set(0, m.players[1])
                        newGames.set(1, m.players[1])
                    } else if (m.scores == [1, 2]) {
                        newGames.set(0, m.players[0])
                        newGames.set(1, m.players[1])
                        newGames.set(2, m.players[1])
                    } else if (m.scores == [2, 0]) {
                        newGames.set(0, m.players[0])
                        newGames.set(1, m.players[0])
                    } else if (m.scores == [2, 1]) {
                        newGames.set(0, m.players[1])
                        newGames.set(1, m.players[0])
                        newGames.set(2, m.players[0])
                    }
                    return {
                        p_ids: m.players,
                        games: newGames,
                        bye: m.players.find(x => x === "0")?.length == 0 ?? false,
                        drops: []
                    }
                })
            }]
        })),
        tag: newTag,
        title: a.title
    }
}

export function new_to_json(a: Draft) {
    return {
        ...a,
        date: a.date.toISOString(),
        rounds: [...a.rounds].map(([x, r]) => {
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
                [k: string]: string | "TIE";
            };
            p_ids: string[];
            bye: boolean;
            drops: string[];
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
        rounds: new Map(a.rounds.map((r, i) => {
            return [i, {
                ...r, matches: r.matches.map(m => {
                    return { ...m, games: new Map(Object.entries(m.games).map(([a, b]) => [parseInt(a), b])) }
                })
            }]
        }))
    }
}

export function determine_winner(m: Match) {
    if (m.bye) return m.p_ids[0];
    const playerWins = new Map(m.p_ids.map(p => [p, 0]))
    m.games.forEach((v) => {
        if (v !== 'TIE') {
            if (playerWins.get(v) === undefined) throw 'Invalid player entry in match winners';
            playerWins.set(v, playerWins.get(v)! + 1)
        }
    })
    let max = 0;
    let winner = "";
    playerWins.forEach((v, k) => {
        if (v > max) {
            max = v
            winner = k
        };
    })
    return winner;
}

export function validate_match(m: Match) {
    m.games.forEach((v, k) => {
        if (v !== 'TIE') {
            if (!m.p_ids.includes(v)) return false;
        }
    })
    return true;
}

const test: Draft = { date: new Date(), id: 0, rounds: new Map([]), scores: [], tag: 'dps', title: 'TEST', description: 'TEST' };
const D: Draft = {
    date: new Date(),
    id: 0,
    rounds: new Map([
        [
            0,
            {
                title: 'TEST',
                matches: [
                    {
                        p_ids: ['411627939478765568', '237059875073556481'],
                        bye: false,
                        drops: [],
                        games: new Map([
                            [0, '411627939478765568'],
                            [1, '411627939478765568']
                        ])
                    },
                    {
                        p_ids: ['320756550992134145', '317470784870285323'],
                        bye: false,
                        drops: [],
                        games: new Map([
                            [0, '320756550992134145'],
                            [1, '320756550992134145']
                        ])
                    },
                    {
                        p_ids: ['298561362034950154', '247076572295593984'],
                        bye: false,
                        drops: ['247076572295593984'],
                        games: new Map([
                            [0, '298561362034950154'],
                            [1, '298561362034950154']
                        ])
                    },
                    {
                        p_ids: ['250385022106730496', '265851480462852096'],
                        bye: false,
                        drops: ['250385022106730496'],
                        games: new Map([
                            [0, '265851480462852096'],
                            [1, '265851480462852096']
                        ])
                    }
                ]
            }
        ],
        [
            1,
            {
                title: 'TEST',
                matches: [
                    {
                        p_ids: ['320756550992134145', '265851480462852096'],
                        bye: false,
                        drops: ['320756550992134145', '265851480462852096'],
                        games: new Map([
                            [0, '320756550992134145'],
                            [1, '320756550992134145']
                        ])
                    },
                    {
                        p_ids: ['411627939478765568', '298561362034950154'],
                        bye: false,
                        drops: ['298561362034950154'],
                        games: new Map([[0, '411627939478765568']])
                    },
                    {
                        p_ids: ['237059875073556481', '317470784870285323'],
                        bye: false,
                        drops: [],
                        games: new Map([
                            [0, '237059875073556481'],
                            [1, '317470784870285323'],
                            [2, '237059875073556481']
                        ])
                    }
                ]
            }
        ],
        [
            2,
            {
                title: 'TEST',
                matches: [
                    {
                        p_ids: ['411627939478765568', '317470784870285323'],
                        bye: false,
                        drops: [],
                        games: new Map([[0, '411627939478765568']])
                    },
                    {
                        p_ids: ['237059875073556481'],
                        bye: true,
                        drops: [],
                        games: new Map([])
                    }
                ]
            }
        ]
    ]),
    scores: [
        { id: '411627939478765568', points: 9, gwp: 1.0, ogp: 0.4667, omp: 0.5 },
        { id: '237059875073556481', points: 6, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
        { id: '320756550992134145', points: 6, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
        { id: '298561362034950154', points: 3, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
        { id: '265851480462852096', points: 3, gwp: 0.5, ogp: 0.6667, omp: 0.6667 },
        { id: '317470784870285323', points: 0, gwp: 0.4, ogp: 0.6667, omp: 0.6667 },
        { id: '247076572295593984', points: 0, gwp: 0, ogp: 0.6667, omp: 0.5 },
        { id: '250385022106730496', points: 0, gwp: 0, ogp: 0.5, omp: 0.5 }
    ],
    tag: 'dps',
    title: 'TEST TITLE',
    description: 'TEST DESCRIPTION'
};