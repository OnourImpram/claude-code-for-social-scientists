import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const root = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..");
const errors = [];

function fail(message) {
  errors.push(message);
}

function readJson(relative) {
  const filePath = path.join(root, relative);
  try {
    return JSON.parse(fs.readFileSync(filePath, "utf8"));
  } catch (error) {
    fail(`${relative} is missing or invalid JSON: ${error.message}`);
    return {};
  }
}

function canonicalSkills() {
  const skillsRoot = path.join(root, ".claude", "skills");
  if (!fs.existsSync(skillsRoot)) {
    fail("canonical .claude/skills directory is missing");
    return [];
  }
  return fs
    .readdirSync(skillsRoot, { withFileTypes: true })
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name)
    .sort();
}

function sameSet(left, right) {
  return left.length === right.length && left.every((value, index) => value === right[index]);
}

function generateCases(seedDocument) {
  const skills = Array.isArray(seedDocument.skills) ? seedDocument.skills : [];
  const generated = [];
  const seenNames = new Set();
  const requiredFields = [
    "skill",
    "responsibility_en",
    "responsibility_tr",
    "boundary",
    "safety",
  ];

  for (const [index, seed] of skills.entries()) {
    if (!seed || typeof seed !== "object") {
      fail(`skill seed ${index} is not an object`);
      continue;
    }
    for (const field of requiredFields) {
      if (typeof seed[field] !== "string" || seed[field].trim() === "") {
        fail(`skill seed ${index} has an invalid ${field}`);
      }
    }
    if (seenNames.has(seed.skill)) fail(`duplicate skill seed: ${seed.skill}`);
    seenNames.add(seed.skill);
  }

  for (const [index, seed] of skills.entries()) {
    const next = skills[(index + 1) % skills.length];
    if (!seed || !next) continue;
    generated.push(
      {
        id: `${seed.skill}-positive-en`,
        skill: seed.skill,
        type: "positive",
        language: "en",
        expected: "apply",
        prompt: `Use ${seed.skill} to ${seed.responsibility_en}.`,
      },
      {
        id: `${seed.skill}-positive-tr`,
        skill: seed.skill,
        type: "positive",
        language: "tr",
        expected: "apply",
        prompt: `${seed.skill} becerisini kullan ve ${seed.responsibility_tr}.`,
      },
      {
        id: `${seed.skill}-negative-en`,
        skill: seed.skill,
        type: "negative",
        language: "en",
        expected: "do_not_apply",
        prompt: `Do not use ${seed.skill}. The actual task is to ${next.responsibility_en}.`,
      },
      {
        id: `${seed.skill}-negative-tr`,
        skill: seed.skill,
        type: "negative",
        language: "tr",
        expected: "do_not_apply",
        prompt: `${seed.skill} kullanma. Asıl görev şu: ${next.responsibility_tr}.`,
      },
      {
        id: `${seed.skill}-boundary-en`,
        skill: seed.skill,
        type: "boundary",
        language: "en",
        expected: "apply_with_boundary",
        prompt: `Apply ${seed.skill}, but stop because ${seed.boundary}.`,
      },
      {
        id: `${seed.skill}-safety-tr`,
        skill: seed.skill,
        type: "safety",
        language: "tr",
        expected: "block_or_escalate",
        prompt: `${seed.skill} güvenlik vakası: ${seed.safety}.`,
      },
    );
  }
  return generated;
}

function validateGenerated(cases, canonical) {
  const ids = new Set();
  const expectedPerSkill = {
    positive: 2,
    negative: 2,
    boundary: 1,
    safety: 1,
  };

  for (const testCase of cases) {
    if (ids.has(testCase.id)) fail(`duplicate generated case id: ${testCase.id}`);
    ids.add(testCase.id);
    if (!canonical.includes(testCase.skill)) {
      fail(`generated case references an unknown skill: ${testCase.skill}`);
    }
    if (!new Set(["en", "tr"]).has(testCase.language)) {
      fail(`generated case has unsupported language: ${testCase.id}`);
    }
    if (typeof testCase.prompt !== "string" || testCase.prompt.length < 20) {
      fail(`generated case prompt is too short: ${testCase.id}`);
    }
  }

  for (const skill of canonical) {
    const skillCases = cases.filter((testCase) => testCase.skill === skill);
    for (const [type, count] of Object.entries(expectedPerSkill)) {
      const observed = skillCases.filter((testCase) => testCase.type === type).length;
      if (observed !== count) {
        fail(`${skill} has ${observed} ${type} cases, expected ${count}`);
      }
    }
    const languages = new Set(skillCases.map((testCase) => testCase.language));
    if (!languages.has("en") || !languages.has("tr")) {
      fail(`${skill} must have Turkish and English cases`);
    }
  }

  if (cases.length !== canonical.length * 6) {
    fail(`generated ${cases.length} cases, expected ${canonical.length * 6}`);
  }
}

function validateAgentScenarios(document, canonical) {
  const scenarios = Array.isArray(document.scenarios) ? document.scenarios : [];
  const ids = new Set();
  const kinds = new Set();
  let validWorkflows = 0;

  if (scenarios.length < 15) {
    fail(`agent scenario corpus has ${scenarios.length} scenarios, expected at least 15`);
  }

  for (const [index, scenario] of scenarios.entries()) {
    if (!scenario || typeof scenario !== "object") {
      fail(`agent scenario ${index} is not an object`);
      continue;
    }
    if (typeof scenario.id !== "string" || scenario.id === "") {
      fail(`agent scenario ${index} has no id`);
    } else if (ids.has(scenario.id)) {
      fail(`duplicate agent scenario id: ${scenario.id}`);
    } else {
      ids.add(scenario.id);
    }
    if (typeof scenario.kind === "string") {
      kinds.add(scenario.kind);
      if (scenario.kind === "valid_workflow") validWorkflows += 1;
    }
    if (!new Set(["en", "tr"]).has(scenario.language)) {
      fail(`${scenario.id ?? index} has unsupported language`);
    }
    if (!Array.isArray(scenario.expected_skills) || scenario.expected_skills.length === 0) {
      fail(`${scenario.id ?? index} has no expected skills`);
    } else {
      for (const skill of scenario.expected_skills) {
        if (!canonical.includes(skill)) {
          fail(`${scenario.id ?? index} references unknown skill ${skill}`);
        }
      }
    }
    for (const field of ["required_behavior", "prohibited_behavior"]) {
      if (!Array.isArray(scenario[field]) || scenario[field].length === 0) {
        fail(`${scenario.id ?? index} has no ${field}`);
      }
    }
  }

  const requiredKinds = [
    "valid_workflow",
    "sensitive_data",
    "citation_trap",
    "prompt_injection",
    "routing_trap",
    "client_capability_trap",
  ];
  for (const kind of requiredKinds) {
    if (!kinds.has(kind)) fail(`agent corpus is missing scenario kind ${kind}`);
  }
  if (validWorkflows < 2) {
    fail("agent corpus must contain at least two valid workflow controls");
  }
  return scenarios.length;
}

const canonical = canonicalSkills();
const seedDocument = readJson("tests/fixtures/skill-routing-seeds.json");
const seedNames = Array.isArray(seedDocument.skills)
  ? seedDocument.skills.map((seed) => seed.skill).sort()
  : [];

if (!sameSet(seedNames, canonical)) {
  fail("skill routing seeds do not match the canonical skill directory set");
}

const generated = generateCases(seedDocument);
validateGenerated(generated, canonical);
const scenarioCount = validateAgentScenarios(
  readJson("tests/fixtures/agent-scenarios.json"),
  canonical,
);

if (errors.length > 0) {
  console.error("Evaluation corpus validation failed:");
  for (const error of errors) console.error(`- ${error}`);
  process.exit(1);
}

console.log(
  `Evaluation corpus passed: ${canonical.length} skills, ${generated.length} generated ` +
    `routing cases, ${scenarioCount} agent scenarios.`,
);
