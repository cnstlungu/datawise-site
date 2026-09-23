import { type Post, seriesInfo, tagName } from './posts';

// "Related posts" by text similarity: TF-IDF over each post's title, description, tags, series
// and body, compared with cosine similarity. Cheap enough to run over every post at build time,
// and it finds genuinely related posts (COALESCE vs IFNULL next to the NULL posts) where shared
// series alone would just list the neighbours.

const STOPWORDS = new Set(
  `a about above after again all also am an and any are as at be because been before being below between both but by
  can could did do does doing down during each few for from further had has have having here how i if in into is it
  its itself just let lets like me more most my no nor not now of off on once only or other our out over own same she
  should so some such than that the their them then there these they this those through to too under until up us use
  used using very was we were what when where which while who whom why will with would you your yours get got one two
  way want see make made need new first well much many may might must shall today post quick look`.split(/\s+/),
);

function tokens(text: string): string[] {
  return (
    text
      .toLowerCase()
      // Drop URLs and image paths: slugs and domains would make every post "related" to its links.
      .replace(/\]\([^)]*\)/g, '] ')
      .replace(/https?:\/\/\S+/g, ' ')
      .match(/[a-z][a-z0-9_]+/g) ?? []
  ).filter((t) => !STOPWORDS.has(t));
}

function weightedTerms(post: Post): Map<string, number> {
  const d = post.data;
  const parts: [string, number][] = [
    [d.title, 3],
    [d.seoDescription, 2],
    [d.tags.map(tagName).join(' '), 2],
    [d.series ? seriesInfo(d.series)?.name ?? '' : '', 1],
    [post.body ?? '', 1],
  ];
  const tf = new Map<string, number>();
  for (const [text, weight] of parts) {
    for (const t of tokens(text)) tf.set(t, (tf.get(t) ?? 0) + weight);
  }
  return tf;
}

/** Map of post id -> up to `limit` related posts, most similar first. */
export function relatedPosts(posts: Post[], limit = 4): Map<string, Post[]> {
  // Only posts that live here: skip delisted ones and ones whose canonical copy is elsewhere.
  const candidates = posts.filter((p) => !p.data.delisted && !p.data.canonical);
  const terms = new Map(posts.map((p) => [p.id, weightedTerms(p)]));

  const df = new Map<string, number>();
  for (const p of candidates) for (const t of terms.get(p.id)!.keys()) df.set(t, (df.get(t) ?? 0) + 1);
  const idf = (t: string) => Math.log((candidates.length + 1) / ((df.get(t) ?? 0) + 1));

  const vectors = new Map<string, Map<string, number>>();
  for (const p of posts) {
    const v = new Map<string, number>();
    let norm = 0;
    for (const [t, n] of terms.get(p.id)!) {
      const w = (1 + Math.log(n)) * idf(t);
      if (w > 0) {
        v.set(t, w);
        norm += w * w;
      }
    }
    norm = Math.sqrt(norm) || 1;
    for (const [t, w] of v) v.set(t, w / norm);
    vectors.set(p.id, v);
  }

  const cosine = (a: Map<string, number>, b: Map<string, number>) => {
    const [small, big] = a.size < b.size ? [a, b] : [b, a];
    let sum = 0;
    for (const [t, w] of small) sum += w * (big.get(t) ?? 0);
    return sum;
  };

  const result = new Map<string, Post[]>();
  for (const p of posts) {
    const v = vectors.get(p.id)!;
    result.set(
      p.id,
      candidates
        .filter((c) => c.id !== p.id)
        .map((c) => ({ c, score: cosine(v, vectors.get(c.id)!) }))
        .sort((x, y) => y.score - x.score)
        .slice(0, limit)
        .map(({ c }) => c),
    );
  }
  return result;
}
