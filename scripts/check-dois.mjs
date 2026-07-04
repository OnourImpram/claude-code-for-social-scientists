// DOI liveness checker.
//
// Walks the repository for cited DOIs and resolves each against the doi.org
// handle system. A registered DOI answers with a 3xx redirect to its landing
// page; an unregistered or withdrawn DOI answers 404/410. We use a manual
// (non-followed) redirect so we test DOI *registration*, not whether a given
// publisher happens to block automated clients on its landing page.
//
// This is network-dependent and therefore runs as a scheduled, non-blocking
// workflow, never as a required pull-request gate. It operationalizes the
// citation discipline the guide itself preaches: every DOI it prints must
// resolve, or the scheduled run turns red and a human investigates.

import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");

const DOI_PATTERN = /10\.\d{4,9}\/[^\s)\]"'<>*`]+/gu;
const TIMEOUT_MS = 20000;
const CONCURRENCY = 6;
const USER_AGENT =
  "sbcc-doi-liveness/1.0 (+https://github.com/OnourImpram/claude-code-for-social-scientists)";

function walk(dir, files = []) {
  if (!fs.existsSync(dir)) return files;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    if (entry.name === ".git" || entry.name === "node_modules") continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, files);
    else files.push(full);
  }
  return files;
}

function normalizeDoi(rawDoi) {
  // Drop polite-pool query strings and fragments, then trailing punctuation or
  // markdown delimiters (a DOI abutting **bold** or `code` must not absorb them).
  const base = rawDoi.split(/[?#]/u)[0];
  return base.replace(/[.,;:*_`]+$/u, "");
}

function collectDois() {
  // Check DOIs where citation correctness is load-bearing: the booklet
  // bibliographies and the machine-readable CITATION.cff record. Narrative docs
  // (CHANGELOG, README prose) are excluded on purpose, since they may quote
  // superseded or deliberately non-resolving identifiers as historical record.
  const sources = walk(path.join(root, "booklets")).filter((file) =>
    file.endsWith(".md"),
  );
  const citation = path.join(root, "CITATION.cff");
  if (fs.existsSync(citation)) sources.push(citation);

  const map = new Map(); // normalized doi -> Set of source files
  for (const file of sources) {
    const relative = path.relative(root, file).replaceAll(path.sep, "/");
    const text = fs.readFileSync(file, "utf8");
    for (const match of text.match(DOI_PATTERN) || []) {
      const doi = normalizeDoi(match);
      if (/x{4,}/iu.test(doi)) continue; // skip placeholder DOIs such as 10.XXXXX
      if (!map.has(doi)) map.set(doi, new Set());
      map.get(doi).add(relative);
    }
  }
  return map;
}

async function probe(url, method) {
  return fetch(url, {
    method,
    redirect: "manual",
    signal: AbortSignal.timeout(TIMEOUT_MS),
    headers: { "user-agent": USER_AGENT },
  });
}

function classify(status) {
  if (status === 404 || status === 410) return "dead";
  // status 0 / opaqueredirect (browser-style) or any 2xx/3xx means the handle
  // resolved, i.e. the DOI is registered.
  if (status === 0 || (status >= 200 && status < 400)) return "alive";
  return "retry";
}

async function resolveDoi(doi) {
  const url = `https://doi.org/${doi}`;
  try {
    const head = await probe(url, "HEAD");
    const headVerdict = classify(head.status);
    if (headVerdict !== "retry") return { state: headVerdict, status: head.status };

    const get = await probe(url, "GET");
    const getVerdict = classify(get.status);
    if (getVerdict === "retry") return { state: "transient", status: get.status };
    return { state: getVerdict, status: get.status };
  } catch (error) {
    return { state: "transient", status: error?.name ?? String(error) };
  }
}

async function mapLimit(items, limit, fn) {
  const results = [];
  let cursor = 0;
  const workers = Array.from(
    { length: Math.min(limit, items.length) },
    async () => {
      while (cursor < items.length) {
        const current = cursor;
        cursor += 1;
        results[current] = await fn(items[current]);
      }
    },
  );
  await Promise.all(workers);
  return results;
}

const doiMap = collectDois();
const dois = [...doiMap.keys()].sort();

if (dois.length === 0) {
  console.log("No DOIs found to check.");
  process.exit(0);
}

console.log(`Resolving ${dois.length} unique DOIs via https://doi.org ...`);

const outcomes = await mapLimit(dois, CONCURRENCY, async (doi) => ({
  doi,
  ...(await resolveDoi(doi)),
}));

const alive = outcomes.filter((outcome) => outcome.state === "alive");
const transient = outcomes.filter((outcome) => outcome.state === "transient");
const dead = outcomes.filter((outcome) => outcome.state === "dead");

const sources = (doi) => [...doiMap.get(doi)].join(", ");
for (const outcome of alive) {
  console.log(`  ok    ${outcome.status}  ${outcome.doi}`);
}
for (const outcome of transient) {
  console.log(`  warn  ${outcome.status}  ${outcome.doi}  [${sources(outcome.doi)}]`);
}
for (const outcome of dead) {
  console.log(`  DEAD  ${outcome.status}  ${outcome.doi}  [${sources(outcome.doi)}]`);
}

console.log(
  `\n${alive.length} alive, ${transient.length} transient/unverified, ${dead.length} dead.`,
);

if (dead.length > 0) {
  console.error("DOI liveness check failed: the DOIs marked DEAD did not resolve.");
  process.exit(1);
}

console.log("DOI liveness check passed (no dead DOIs).");
