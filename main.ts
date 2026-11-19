// 19 November 2026 — World News in One Image (Node 22, standard library only).
// The bundled entry.png.b64 contains the 1024x1024 infographic rendered from
// the supplied 19 November 2026 stories in news.json by build_image.py.
// No network, randomness or timestamps: each run writes identical PNG bytes.
// Local run: MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const png = Buffer.from(
  readFileSync(new URL('./entry.png.b64', import.meta.url), 'utf8').trim(),
  'base64',
);
if (png.subarray(0, 8).toString('hex') !== '89504e470d0a1a0a') {
  throw new Error('entry.png.b64 did not decode to a PNG');
}
mkdirSync(outDir, { recursive: true });
writeFileSync(join(outDir, 'entry.png'), png);
