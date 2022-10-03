import fs from 'fs/promises';
import type { CardDisplayType } from 'src/types/displaycard';
import { json_to_new, type Draft } from '../types/events';
import { DIS_TOKEN } from '$env/static/private';
import { Client, type User } from 'discord.js'
import type { LoadEvent } from '@sveltejs/kit';
export const prerender = true;
export async function load(event: LoadEvent) {
    let CDs: Promise<(Draft | CardDisplayType)>[] = [];
    await fs.readdir('./src/data').then(async (fnames) => {
        CDs = await fnames.map((fname) => {
            return fs.readFile('./src/data/' + fname, 'utf-8').then((content) => {
                return json_to_new(JSON.parse(content));
            })
        });
    })
    let newList = await Promise.allSettled(CDs).then(v => { return v.map(y => { if (y.status === 'fulfilled') return y.value }) })
    let listUsers: Promise<User>[] = []
    const client = new Client({ intents: ['GuildMembers'] });
    client.login(DIS_TOKEN)
    newList.forEach((x) => {
        if (x === undefined) return null;
        if ('date' in x) {
            x.scores.forEach((v, i) => {
                listUsers.push(client.users.fetch(`${v.id}`))
            })
        }
    })
    let newUsers = await Promise.allSettled(listUsers).then(v => {
        const newthing: Record<string, unknown> = {}
        v.forEach(y => { if (y.status === 'fulfilled') { return newthing[y.value.id] = y.value.toJSON() } })
        return newthing
    })
    return { cds: newList, users: newUsers }
}
