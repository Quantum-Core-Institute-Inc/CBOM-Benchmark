"""Mixed files: realistic-size source files with several cryptographic uses each.

Every other case in the corpus is a small file built around one or two uses. Real modules are
hundreds of lines with crypto in a few helpers, the same algorithm used twice with different
parameters (AES-128 for sessions, AES-256 for exports), ordinary code in between that has numbers
in it (page sizes, buffer lengths, `bit_length()`), and log messages that mention algorithms the
file doesn't use. That is where file-wide parameter guessing, line-window de-duplication and
"first match wins" shortcuts show up.

Used twice: tools/build_mixed.py writes the published corpus/mixed/ from a fixed public seed, and
tools/holdout.py writes holdout-mixed/ from a private one. Same generator, same spec pools.

Findings here are SITE findings ("site": true): several may share a (file, family) key, and the
scorer matches each reported occurrence to the nearest site (tools/score.py, assign_sites).
"""
from __future__ import annotations

from holdout_common import WORDS, sub

# Families that carry parameters, so two uses in one file can disagree.
PARAM_FAMILIES = ["AES", "RSA", "EC", "HMAC", "PBKDF2", "DH", "3DES"]

# Log and note text naming an algorithm, keyed by the families it names. Only phrases naming
# families the file does NOT use go into a file, so a hit on one is a plain false positive.
DECOYS = [
    ("legacy MD5 fingerprints were removed in v3", {"MD5"}),
    ("SHA-1 fingerprints shown for legacy devices only", {"SHA-1"}),
    ("3DES PIN blocks retired in Q3", {"3DES"}),
    ("DSA signing keys revoked", {"DSA"}),
    ("ChaCha20-Poly1305 preferred on mobile", {"ChaCha20-Poly1305"}),
    ("ML-KEM-768 rollout approved for all tenants", {"ML-KEM"}),
    ("rotate RSA-2048 signing keys before the 2030 cutoff", {"RSA"}),
    ("Ed25519 deploy keys only", {"Ed25519"}),
    ("PBKDF2 iterations raised", {"PBKDF2"}),
    ("DH group 14 disabled on the bastion", {"DH"}),
    ("ECDSA P-256 certificates expire in March", {"EC"}),
    ("SHA3-256 checksums in the export manifest", {"SHA3-256"}),
    ("HmacSHA256 webhook check moved to the gateway", {"HMAC", "SHA-256"}),
    ("quantum-safe: ML-DSA-65 signatures (FIPS 204)", {"ML-DSA"}),
    ("AES-256-GCM is the default for new tenants", {"AES"}),
]

# ---------------------------------------------------------------------------------------------
# Ordinary code. <<f>> <<g>> function names, <<C>> a type name, <<w>> a word, <<n>> <<m>> small
# numbers, <<pg>> a page size, <<sz>> a buffer length, <<note>> a decoy phrase. Every template runs
# or compiles under the same flags as the corpus (-Wall -Werror for C, go vet-clean for Go).
# ---------------------------------------------------------------------------------------------
PY = [  # (imports, lines)
    ((), ['def <<f>>(raw):', '    """Split one <<w>> export line into fields, trimming quotes."""', '    fields = []',
          '    for part in raw.split(","):', '        part = part.strip()',
          '        if len(part) >= 2 and part[0] == part[-1] == \'"\':', '            part = part[1:-1]',
          '        fields.append(part)', '    return fields']),
    ((), ['def <<f>>(items, page=1, page_size=<<pg>>):', '    if page < 1:', '        raise ValueError("page must be positive")',
          '    start = (page - 1) * page_size', '    chunk = items[start:start + page_size]',
          '    return {"page": page, "size": page_size, "items": chunk, "more": start + page_size < len(items)}']),
    ((), ['def <<f>>(attempt, base=0.5, cap=<<n>>.0):', '    """Exponential backoff for the <<w>> client, capped."""',
          '    delay = min(cap, base * (2 ** attempt))', '    return round(delay, 3)']),
    ((), ['class <<C>>:', '    def __init__(self, ref, amount, currency="USD"):', '        self.ref = ref',
          '        self.amount = amount', '        self.currency = currency', '',
          '    def total_cents(self):', '        return int(round(self.amount * 100))', '',
          '    def __repr__(self):', '        return f"<<C>>({self.ref!r}, {self.amount}, {self.currency})"']),
    ((), ['def <<f>>(cents, currency="USD"):', '    sign = "-" if cents < 0 else ""', '    cents = abs(cents)',
          '    return f"{sign}{currency} {cents // 100:,}.{cents % 100:02d}"']),
    (("import re",), ['_<<W>>_EMAIL = re.compile(r"^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$", re.I)', '', '',
                      'def <<f>>(address):', '    address = (address or "").strip()',
                      '    return bool(_<<W>>_EMAIL.match(address)) and len(address) <= <<sz>>']),
    (("import random",), ['def <<f>>():', '    """Request id for log correlation, not a secret."""',
                          '    return format(random.getrandbits(128), "032x")']),
    ((), ['def <<f>>(base, override):', '    out = dict(base)', '    for key, value in override.items():',
          '        if isinstance(value, dict) and isinstance(out.get(key), dict):', '            out[key] = <<f>>(out[key], value)',
          '        else:', '            out[key] = value', '    return out']),
    (("from collections import defaultdict",), ['def <<f>>(rows, key="<<w>>"):', '    groups = defaultdict(list)',
                                                '    for row in rows:', '        groups[row.get(key)].append(row)',
                                                '    return dict(groups)']),
    (("import datetime",), ['def <<f>>(days=<<n>>):', '    end = datetime.datetime.now(datetime.timezone.utc)',
                            '    start = end - datetime.timedelta(days=days)', '    return start.isoformat(), end.isoformat()']),
    ((), ['def <<f>>(flags):', '    """Count enabled feature bits and the width needed to store them."""',
          '    return bin(flags).count("1"), flags.bit_length()']),
    ((), ['def <<f>>(data, size=<<sz>>):', '    buf = bytearray(size)', '    n = min(len(data), size)',
          '    buf[:n] = data[:n]', '    return bytes(buf[:n])']),
    (("import logging",), ['_<<W>>_LOG = logging.getLogger("<<w>>")', '', '',
                           'def <<f>>(count):', '    if count > <<m>>:',
                           '        _<<W>>_LOG.warning("<<note>> (%d pending)", count)', '    return count']),
    ((), ['<<W>>_NOTES = {', '    "summary": "<<note>>",', '    "owner": "<<w>>-team",', '}']),
    ((), ['def <<f>>(text, width=<<m>>):', '    words, line, out = text.split(), "", []', '    for word in words:',
          '        if len(line) + len(word) + 1 > width:', '            out.append(line)', '            line = word',
          '        else:', '            line = (line + " " + word).strip()', '    if line:', '        out.append(line)',
          '    return out']),
]

JAVA = [  # (lines) inside the class; fully qualified names, so no imports
    ['    static java.util.List<String> <<f>>(String raw) {', '        java.util.List<String> fields = new java.util.ArrayList<>();',
     '        for (String part : raw.split(",")) {', '            part = part.trim();',
     '            if (part.length() >= 2 && part.startsWith("\\"") && part.endsWith("\\"")) part = part.substring(1, part.length() - 1);',
     '            fields.add(part);', '        }', '        return fields;', '    }'],
    ['    static <T> java.util.List<T> <<f>>(java.util.List<T> items, int page) {', '        int pageSize = <<pg>>;',
     '        int from = Math.min(items.size(), Math.max(0, (page - 1) * pageSize));',
     '        return items.subList(from, Math.min(items.size(), from + pageSize));', '    }'],
    ['    static long <<f>>(int attempt) {', '        long delay = 500L << Math.min(attempt, 10);', '        return Math.min(delay, <<n>>000L);', '    }'],
    ['    record <<C>>(String ref, long cents, String currency) {',
     '        String label() { return ref + " " + currency + " " + String.format("%,d.%02d", cents / 100, cents % 100); }', '    }'],
    ['    private static final java.util.regex.Pattern <<W>>_EMAIL = java.util.regex.Pattern.compile("^[^@\\\\s]+@[^@\\\\s]+\\\\.[a-z]{2,}$");', '',
     '    static boolean <<f>>(String address) {', '        return address != null && address.length() <= <<sz>> && <<W>>_EMAIL.matcher(address.trim()).matches();', '    }'],
    ['    static String <<f>>() {',
     '        return Long.toHexString(java.util.concurrent.ThreadLocalRandom.current().nextLong());', '    }'],
    ['    static java.util.Map<String, java.util.List<String>> <<f>>(java.util.List<String> rows) {',
     '        java.util.Map<String, java.util.List<String>> out = new java.util.TreeMap<>();',
     '        for (String row : rows) out.computeIfAbsent(row.isEmpty() ? "" : row.substring(0, 1), k -> new java.util.ArrayList<>()).add(row);',
     '        return out;', '    }'],
    ['    static byte[] <<f>>(byte[] data) {', '        java.nio.ByteBuffer buf = java.nio.ByteBuffer.allocate(<<sz>>);',
     '        buf.put(data, 0, Math.min(data.length, buf.capacity()));', '        return java.util.Arrays.copyOf(buf.array(), buf.position());', '    }'],
    ['    private static final System.Logger <<W>>_LOG = System.getLogger("<<w>>");', '',
     '    static int <<f>>(int pending) {', '        if (pending > <<m>>) <<W>>_LOG.log(System.Logger.Level.WARNING, "<<note>> ({0} pending)", pending);',
     '        return pending;', '    }'],
    ['    private static final java.util.Map<String, String> <<W>>_NOTES = java.util.Map.of(',
     '        "summary", "<<note>>",', '        "owner", "<<w>>-team");'],
    ['    static int[] <<f>>(int flags) {', '        return new int[] {Integer.bitCount(flags), 32 - Integer.numberOfLeadingZeros(flags)};', '    }'],
    ['    static String <<f>>(java.time.Duration window) {', '        java.time.Instant end = java.time.Instant.now();',
     '        return end.minus(window).toString() + ".." + end;', '    }'],
]

GO = [  # (imports, lines)
    (("strings",), ['func <<f>>(raw string) []string {', '\tvar fields []string', '\tfor _, part := range strings.Split(raw, ",") {',
                    '\t\tpart = strings.TrimSpace(part)', '\t\tfields = append(fields, strings.Trim(part, `"`))', '\t}', '\treturn fields', '}']),
    ((), ['func <<f>>(items []string, page int) []string {', '\tconst pageSize = <<pg>>', '\tfrom := (page - 1) * pageSize',
          '\tif from < 0 || from >= len(items) {', '\t\treturn nil', '\t}', '\tto := from + pageSize', '\tif to > len(items) {',
          '\t\tto = len(items)', '\t}', '\treturn items[from:to]', '}']),
    (("time",), ['func <<f>>(attempt int) time.Duration {', '\td := 500 * time.Millisecond << uint(attempt)',
                 '\tif limit := <<n>> * time.Second; d > limit {', '\t\treturn limit', '\t}', '\treturn d', '}']),
    ((), ['type <<C>> struct {', '\tRef      string', '\tCents    int64', '\tCurrency string', '}', '',
          'func (x <<C>>) Label() string {', '\treturn fmt.Sprintf("%s %s %d.%02d", x.Ref, x.Currency, x.Cents/100, x.Cents%100)', '}']),
    (("strconv",), ['func <<f>>(s string) (int, error) {', '\tn, err := strconv.Atoi(s)', '\tif err != nil {', '\t\treturn 0, err',
                    '\t}', '\tif n > <<sz>> {', '\t\tn = <<sz>>', '\t}', '\treturn n, nil', '}']),
    (("sort",), ['func <<f>>(rows map[string]int) []string {', '\tkeys := make([]string, 0, len(rows))', '\tfor k := range rows {',
                 '\t\tkeys = append(keys, k)', '\t}', '\tsort.Strings(keys)', '\treturn keys', '}']),
    ((), ['func <<f>>(data []byte) []byte {', '\tbuf := make([]byte, <<sz>>)', '\tn := copy(buf, data)', '\treturn buf[:n]', '}']),
    (("log",), ['func <<f>>(pending int) int {', '\tif pending > <<m>> {', '\t\tlog.Printf("<<note>> (%d pending)", pending)', '\t}',
                '\treturn pending', '}']),
    ((), ['var <<g>> = map[string]string{', '\t"summary": "<<note>>",', '\t"owner":   "<<w>>-team",', '}']),
    (("math/bits",), ['func <<f>>(flags uint32) (int, int) {', '\treturn bits.OnesCount32(flags), bits.Len32(flags)', '}']),
]

JS = [
    ['function <<f>>(raw) {', '  return raw.split(",").map((part) => part.trim().replace(/^"|"$/g, ""));', '}'],
    ['function <<f>>(items, page = 1, pageSize = <<pg>>) {', '  const start = (page - 1) * pageSize;',
     '  return { page, size: pageSize, items: items.slice(start, start + pageSize), more: start + pageSize < items.length };', '}'],
    ['function <<f>>(attempt) {', '  return Math.min(<<n>>000, 500 * 2 ** attempt);', '}'],
    ['class <<C>> {', '  constructor(ref, cents, currency = "USD") {', '    this.ref = ref;', '    this.cents = cents;',
     '    this.currency = currency;', '  }', '  label() {',
     '    return `${this.ref} ${this.currency} ${(this.cents / 100).toFixed(2)}`;', '  }', '}'],
    ['const <<W>>_EMAIL = /^[^@\\s]+@[^@\\s]+\\.[a-z]{2,}$/i;', '', 'function <<f>>(address) {',
     '  return typeof address === "string" && address.length <= <<sz>> && <<W>>_EMAIL.test(address.trim());', '}'],
    ['function <<f>>(rows, key = "<<w>>") {', '  return rows.reduce((acc, row) => {', '    (acc[row[key]] ||= []).push(row);',
     '    return acc;', '  }, {});', '}'],
    ['function <<f>>(data) {', '  const buf = Buffer.alloc(<<sz>>);', '  const n = Buffer.from(data).copy(buf);', '  return buf.subarray(0, n);', '}'],
    ['function <<f>>(pending) {', '  if (pending > <<m>>) console.warn(`<<note>> (${pending} pending)`);', '  return pending;', '}'],
    ['const <<W>>_NOTES = {', '  summary: "<<note>>",', '  owner: "<<w>>-team",', '};'],
    ['function <<f>>(cents, currency = "USD") {', '  return new Intl.NumberFormat("en-US", { style: "currency", currency }).format(cents / 100);', '}'],
    ['function <<f>>(base, override) {', '  const out = { ...base };', '  for (const [k, v] of Object.entries(override)) {',
     '    out[k] = v && typeof v === "object" && !Array.isArray(v) && typeof out[k] === "object" ? <<f>>(out[k], v) : v;',
     '  }', '  return out;', '}'],
]

C = [  # (includes, lines); external linkage so unused helpers don't trip -Wunused-function
    ((), ['int <<f>>(int v, int lo, int hi) {', '    return v < lo ? lo : (v > hi ? hi : v);', '}']),
    (("stdlib.h",), ['long <<f>>(const char *s) {', '    char *end = NULL;', '    long n = strtol(s, &end, 10);',
                     '    if (end == s || n < 0) return -1;', '    return n > <<sz>> ? <<sz>> : n;', '}']),
    (("ctype.h", "string.h"), ['char *<<f>>(char *s) {', '    size_t n = strlen(s);', '    while (n > 0 && isspace((unsigned char)s[n - 1])) s[--n] = 0;',
                               '    while (*s && isspace((unsigned char)*s)) s++;', '    return s;', '}']),
    ((), ['struct <<g>> {', '    const char *ref;', '    long cents;', '    int page_size;', '};', '',
          'long <<f>>(const struct <<g>> *x) {', '    return x->cents / 100 + x->page_size * 0;', '}']),
    (("string.h",), ['size_t <<f>>(const unsigned char *data, size_t len, unsigned char *out) {', '    unsigned char buf[<<sz>>];',
                     '    size_t n = len < sizeof buf ? len : sizeof buf;', '    memcpy(buf, data, n);', '    memcpy(out, buf, n);',
                     '    return n;', '}']),
    ((), ['unsigned <<f>>(unsigned flags) {', '    unsigned count = 0;', '    while (flags) {', '        count += flags & 1u;',
          '        flags >>= 1;', '    }', '    return count;', '}']),
    ((), ['int <<f>>(int page, int total) {', '    const int page_size = <<pg>>;', '    int pages = (total + page_size - 1) / page_size;',
          '    return page > pages ? pages : page;', '}']),
    ((), ['const char *<<g>> = "<<note>>";']),
    ((), ['long <<f>>(int attempt) {', '    long d = 500L << (attempt > 10 ? 10 : attempt);', '    return d > <<n>>000L ? <<n>>000L : d;', '}']),
]


def _fill(lines, rng, names, notes, style="snake"):
    w = rng.choice(WORDS)
    m = {"f": names.snake() if style == "snake" else names.camel() if style == "camel" else names.var(),
         "g": names.camel() if style != "snake" else names.snake(), "C": names.cap(), "w": w, "W": f"{w.upper()}_{rng.randint(10, 99)}",
         "n": str(rng.randint(5, 60)), "m": str(rng.randint(10, 500)), "pg": str(rng.choice([25, 50, 128, 256, 512])),
         "sz": str(rng.choice([16, 32, 64, 256, 1024, 4096])), "note": rng.choice(notes) if notes else "nightly sync finished"}
    return [sub(t, m) for t in lines]


def _decoy_notes(rng, used: set[str]) -> list[str]:
    return [p for p, fams in DECOYS if not fams & used]


def pick_specs(fns, rng, draw, n_sites: int, allowed: set[str] | None = None) -> list[dict]:
    """n_sites specs from a spec pool; when the pool allows it, one family twice with different
    parameters, which is the case file-wide guessing gets wrong. allowed: limit to these families
    (the holdout mirrors the families the published mixed files use)."""
    chosen = []
    pairable = [f for f in PARAM_FAMILIES if (allowed is None or f in allowed) and any(_makes(fn, f, rng) for fn in fns)]
    if pairable:
        fam = rng.choice(pairable)
        a = draw(fns, fam, rng, False)
        for _ in range(60):
            b = draw(fns, fam, rng, False)
            if a and b and b["params"] != a["params"]:
                chosen += [a, b]
                break
    for _ in range(200):
        if len(chosen) >= n_sites:
            break
        sp = rng.choice(fns)(rng, False)
        if allowed is not None and sp["family"] not in allowed:
            continue
        n = sum(1 for c in chosen if c["family"] == sp["family"])
        if n == 0 or (n == 1 and sp["family"] in ("SHA-256", "MD5") and rng.random() < 0.3):
            chosen.append(sp)
    rng.shuffle(chosen)
    return chosen


def _makes(fn, family, rng) -> bool:
    import random as _r
    probe = _r.Random(rng.random())
    return any(fn(probe, False)["family"] == family for _ in range(12))


def add_filler(lang, builder, rng, names, used_families: set[str], target_lines: int, current_lines) -> None:
    """Append ordinary code to a builder until the rendered file would reach target_lines."""
    notes = _decoy_notes(rng, used_families)
    for _ in range(400):
        if current_lines() >= target_lines:
            return
        if lang == "python":
            imps, tpl = rng.choice(PY)
            builder.imports.update(imps)
            builder.funcs.append([(t, None) for t in _fill(tpl, rng, names, notes)] + [("", None), ("", None)])
        elif lang == "java":
            builder.funcs.append([(t, None) for t in _fill(rng.choice(JAVA), rng, names, notes, "camel")] + [("", None)])
        elif lang == "go":
            imps, tpl = rng.choice(GO)
            for i in imps:
                builder.imports.setdefault(i, "")
            builder.funcs.append([(t, None) for t in _fill(tpl, rng, names, notes, "camel")] + [("", None)])
        elif lang in ("javascript", "typescript"):
            builder.funcs.append([(t, None) for t in _fill(rng.choice(JS), rng, names, notes, "camel")] + [("", None)])
        else:
            incs, tpl = rng.choice(C)
            builder.includes.update(incs)
            builder.funcs.append([(t, None) for t in _fill(tpl, rng, names, notes, "var")] + [("", None)])


def funcs_lines(builder) -> int:
    return sum(len(f) for f in builder.funcs) + len(getattr(builder, "top", [])) + len(builder.mains) + 15
