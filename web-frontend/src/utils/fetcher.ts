type FetchRequestArgs = {
    url: string;
    token: string;
}

export default function fetcher(args: FetchRequestArgs) {
    const { url, token } = args;
    return fetch(url, {
        headers: { 'Authorization': `Bearer ${token}` },
    }).then((r) => r.json());
}