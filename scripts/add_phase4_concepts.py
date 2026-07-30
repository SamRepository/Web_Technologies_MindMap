#!/usr/bin/env python3
"""ONE-TIME: add the Phase 4 modernization concepts.

Kept for auditability alongside ``extract_readme.py``. Writes new concept YAML
files; it does not touch existing ones. Safe to re-run (it overwrites only the
files it owns), but there is no reason to.

Ordering: new siblings get ``order`` values from 1000 up. Sibling sequence is
decided by ``order`` within a parent, so a high value simply appends after the
existing children without disturbing any of them. The Web3 disambiguation is the
one exception -- it gets ``order: 0`` so it appears *first* in the Web 3.0
subsection, before the material whose ambiguity it resolves.
"""

from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent

W = "wikipedia"
O = "official"
S = "spec"
M = "mdn"
R = "reference"


def L(type_: str, label: str, url: str) -> dict:
    return {"type": type_, "label": label, "url": url}


WIKI = lambda slug: L(W, "Wikipedia", f"https://en.wikipedia.org/wiki/{slug}")  # noqa: E731
MDN = lambda label, path: L(M, label, f"https://developer.mozilla.org/en-US/docs/{path}")  # noqa: E731

# (id, label, section, subsection, parent, order, status, definition, links, see_also)
CONCEPTS: list[dict] = [
    # ---------------------------------------------------------------- protocols
    dict(id="http-2", label="HTTP/2", section="01-introduction",
         subsection="internet-basics", parent="http-https", order=1001,
         definition="A major revision of HTTP that keeps the same semantics but changes how "
                    "messages travel: requests are multiplexed over a single connection and "
                    "headers are compressed, removing the need for the workarounds sites used "
                    "to hide HTTP/1.1's one-request-at-a-time behaviour.",
         links=[L(S, "RFC 9113", "https://httpwg.org/specs/rfc9113.html"), WIKI("HTTP/2")]),
    dict(id="http-3", label="HTTP/3", section="01-introduction",
         subsection="internet-basics", parent="http-https", order=1002,
         definition="The current major version of HTTP, carried over QUIC instead of TCP. Because "
                    "each stream is independent, a single lost packet no longer stalls every other "
                    "request on the connection, which matters most on mobile and lossy networks.",
         links=[L(S, "RFC 9114", "https://httpwg.org/specs/rfc9114.html"), WIKI("HTTP/3")]),
    dict(id="quic", label="QUIC", section="01-introduction",
         subsection="internet-basics", parent="http-3", order=1003,
         definition="A transport protocol built on UDP that provides the reliability, congestion "
                    "control and encryption that TCP plus TLS provide, but with a faster handshake "
                    "and independent streams. It is the transport underneath HTTP/3.",
         links=[L(S, "RFC 9000", "https://datatracker.ietf.org/doc/html/rfc9000"), WIKI("QUIC")]),

    # ------------------------------------------------- Web3 vs Web 3.0 (author to review)
    dict(id="web3-disambiguation", label="Web3 vs Web 3.0 — a note on terminology",
         section="02-evolution", subsection="web-3-0-semantic-web", parent=None, order=0,
         definition="These two terms are routinely confused, and they do not mean the same thing. "
                    "In this mind map, and in academic usage, **Web 3.0** means the *Semantic Web*: "
                    "the W3C programme of making data machine-readable through RDF, ontologies and "
                    "linked data, so that software can reason over meaning rather than parse layout. "
                    "**Web3** is a separate, later coinage from the cryptocurrency industry, "
                    "describing blockchain-based decentralised applications and token ownership. "
                    "The two agendas share the ambition of decentralisation but almost nothing else: "
                    "different standards bodies, different technologies, different research "
                    "communities. When you read \"Web 3.0\" in a tutorial, check which one is meant.",
         links=[WIKI("Semantic_Web"), WIKI("Web3")],
         see_also=["linked-data", "blockchain-and-decentralization", "knowledge-graphs"]),

    # ------------------------------------------------------------------ CSS / UI
    dict(id="tailwind-css", label="Tailwind CSS", section="03-web-development",
         subsection="front-end-development", parent="css3", order=1023,
         definition="A utility-first CSS framework: instead of writing custom stylesheets, you "
                    "compose small single-purpose classes directly in the markup. It takes the "
                    "opposite approach to component frameworks like Bootstrap, trading readable "
                    "HTML for the removal of the naming and dead-CSS problems that grow with a "
                    "hand-written stylesheet.",
         links=[L(O, "Official Website", "https://tailwindcss.com/"), WIKI("Tailwind_CSS")],
         see_also=["bootstrap"]),
    dict(id="css-grid", label="CSS Grid Layout", section="03-web-development",
         subsection="front-end-development", parent="css3", order=1024,
         definition="A two-dimensional layout system that positions elements in rows and columns "
                    "declared on the container. It replaced the float- and table-based hacks that "
                    "page layout previously required, and complements Flexbox, which handles "
                    "one dimension at a time.",
         links=[L(S, "CSS Grid Layout Module", "https://www.w3.org/TR/css-grid-1/"),
                MDN("MDN Web Docs", "Web/CSS/CSS_grid_layout")]),
    dict(id="container-queries", label="Container Queries", section="03-web-development",
         subsection="front-end-development", parent="css3", order=1025, status="emerging",
         definition="Styling rules that respond to the size of a component's own container rather "
                    "than the size of the viewport. This is what media queries could never express: "
                    "a genuinely reusable component that adapts wherever it is placed, without "
                    "knowing anything about the page around it.",
         links=[L(S, "CSS Containment Module Level 3", "https://www.w3.org/TR/css-contain-3/"),
                MDN("MDN Web Docs", "Web/CSS/CSS_containment/Container_queries")]),

    # --------------------------------------------------------------- JS language
    dict(id="typescript", label="TypeScript", section="03-web-development",
         subsection="front-end-development", parent="javascript", order=1020,
         definition="A typed superset of JavaScript that compiles to plain JavaScript. Types are "
                    "checked before the code runs and then erased, so TypeScript catches a whole "
                    "class of errors at build time while shipping ordinary JavaScript to the "
                    "browser. It is now the default choice for large front-end and Node codebases.",
         links=[L(O, "Official Website", "https://www.typescriptlang.org/"), WIKI("TypeScript")]),
    dict(id="esm", label="ES Modules (ESM)", section="03-web-development",
         subsection="front-end-development", parent="javascript", order=1021,
         definition="JavaScript's standard module system, using `import` and `export`. Browsers "
                    "and Node both support it natively, which ended the long split between "
                    "competing module formats such as CommonJS and AMD.",
         links=[MDN("MDN Web Docs", "Web/JavaScript/Guide/Modules"),
                L(S, "ECMAScript Modules", "https://tc39.es/ecma262/#sec-modules")],
         see_also=["es6-features"]),
    dict(id="import-maps", label="Import Maps", section="03-web-development",
         subsection="front-end-development", parent="esm", order=1022, status="emerging",
         definition="A JSON block in the page that tells the browser how to resolve bare module "
                    "names such as `import 'lodash'` to real URLs. It allows a project to use "
                    "named imports directly in the browser without a bundler rewriting them first.",
         links=[MDN("MDN Web Docs", "Web/HTML/Reference/Elements/script/type/importmap"),
                L(S, "HTML Standard — import maps",
                  "https://html.spec.whatwg.org/multipage/webappapis.html#import-maps")]),

    # ------------------------------------------------------- frameworks / meta
    dict(id="svelte", label="Svelte", section="03-web-development",
         subsection="front-end-development", parent="frameworks-and-libraries", order=1030,
         definition="A UI framework that shifts most of its work to build time: components compile "
                    "into direct DOM-updating JavaScript, so no framework runtime or virtual DOM "
                    "ships to the browser.",
         links=[L(O, "Official Website", "https://svelte.dev/"), WIKI("Svelte")]),
    dict(id="meta-frameworks", label="Meta-Frameworks", section="03-web-development",
         subsection="front-end-development", parent="frameworks-and-libraries", order=1031,
         definition="Frameworks built on top of a UI library to supply what an application needs "
                    "beyond rendering components: routing, data loading, server-side rendering, "
                    "build configuration and deployment. They are where most production front-end "
                    "work now starts.",
         links=[WIKI("Web_framework")]),
    dict(id="next-js", label="Next.js", section="03-web-development",
         subsection="front-end-development", parent="meta-frameworks", order=1032,
         definition="The most widely used React meta-framework, providing file-based routing, "
                    "server-side and static rendering, and server components in one toolchain.",
         links=[L(O, "Official Website", "https://nextjs.org/"), WIKI("Next.js")],
         see_also=["react-js"]),
    dict(id="nuxt", label="Nuxt", section="03-web-development",
         subsection="front-end-development", parent="meta-frameworks", order=1033,
         definition="The equivalent meta-framework for Vue, adding routing, rendering modes and a "
                    "module ecosystem on top of Vue's component model.",
         links=[L(O, "Official Website", "https://nuxt.com/")], see_also=["vue-js"]),
    dict(id="sveltekit", label="SvelteKit", section="03-web-development",
         subsection="front-end-development", parent="meta-frameworks", order=1034,
         definition="Svelte's official application framework, handling routing, data loading and "
                    "the choice between server rendering, prerendering and client rendering per "
                    "route.",
         links=[L(O, "Official Documentation", "https://svelte.dev/docs/kit/introduction")],
         see_also=["svelte"]),
    dict(id="remix", label="Remix", section="03-web-development",
         subsection="front-end-development", parent="meta-frameworks", order=1035,
         definition="A React framework built around web platform fundamentals — HTML forms, HTTP "
                    "caching and nested routing — rather than around client-side state management.",
         links=[L(O, "Official Website", "https://remix.run/")], see_also=["react-js"]),
    dict(id="astro", label="Astro", section="03-web-development",
         subsection="front-end-development", parent="meta-frameworks", order=1036,
         definition="A framework aimed at content-heavy sites. It ships zero JavaScript by default "
                    "and hydrates only the components you mark as interactive, and it can mix "
                    "React, Vue and Svelte components in one project.",
         links=[L(O, "Official Website", "https://astro.build/")],
         see_also=["hydration", "jamstack"]),
    dict(id="htmx", label="htmx", section="03-web-development",
         subsection="front-end-development", parent="frameworks-and-libraries", order=1040,
         definition="A small library that lets HTML attributes issue AJAX requests and swap the "
                    "returned HTML into the page. It deliberately inverts the single-page-app "
                    "model: the server keeps rendering HTML, and very little application state "
                    "lives in the browser.",
         links=[L(O, "Official Website", "https://htmx.org/")], see_also=["spas"]),

    # ------------------------------------------------------------ build tooling
    dict(id="build-tooling", label="Build Tooling", section="03-web-development",
         subsection="front-end-development", parent=None, order=1050,
         definition="The programs that turn source files into what the browser actually loads: "
                    "resolving modules, compiling TypeScript and JSX, bundling, minifying, and "
                    "serving a fast development server with hot reloading.",
         links=[WIKI("Build_automation")]),
    dict(id="vite", label="Vite", section="03-web-development",
         subsection="front-end-development", parent="build-tooling", order=1051,
         definition="The de facto standard front-end build tool. In development it serves native "
                    "ES modules so startup stays near-instant regardless of project size, and for "
                    "production it bundles with Rollup.",
         links=[L(O, "Official Website", "https://vite.dev/"), WIKI("Vite_(software)")],
         see_also=["esm"]),
    dict(id="esbuild", label="esbuild", section="03-web-development",
         subsection="front-end-development", parent="build-tooling", order=1052,
         definition="A JavaScript and TypeScript bundler written in Go, one to two orders of "
                    "magnitude faster than the earlier JavaScript-based bundlers. Several other "
                    "tools use it internally rather than reimplementing the work.",
         links=[L(O, "Official Website", "https://esbuild.github.io/")]),

    # --------------------------------------------------------------- JS runtimes
    dict(id="deno", label="Deno", section="03-web-development",
         subsection="back-end-development", parent="server-side-programming", order=1060,
         definition="A JavaScript and TypeScript runtime from Node's original creator, addressing "
                    "design regrets in Node: TypeScript runs without a build step, and file, "
                    "network and environment access are denied unless explicitly granted.",
         links=[L(O, "Official Website", "https://deno.com/"), WIKI("Deno_(software)")],
         see_also=["node-js", "typescript"]),
    dict(id="bun", label="Bun", section="03-web-development",
         subsection="back-end-development", parent="server-side-programming", order=1061,
         definition="A JavaScript runtime built on JavaScriptCore that also bundles a package "
                    "manager, test runner and bundler into one binary, competing with Node "
                    "primarily on startup and install speed.",
         links=[L(O, "Official Website", "https://bun.sh/"), WIKI("Bun_(software)")],
         see_also=["node-js"]),

    # -------------------------------------------------------------- defences
    dict(id="defenses", label="Defenses", section="03-web-development",
         subsection="web-security", parent=None, order=1070,
         definition="The mechanisms that protect against the threats above. Security on the web is "
                    "layered: transport encryption, strong authentication, and browser-enforced "
                    "policies that limit what a page is permitted to load or reach.",
         links=[MDN("MDN Web Security", "Web/Security")], see_also=["threats"]),
    dict(id="tls-https", label="TLS / HTTPS", section="03-web-development",
         subsection="web-security", parent="defenses", order=1071,
         definition="Transport Layer Security encrypts and authenticates the connection between "
                    "browser and server, so traffic cannot be read or altered in transit. HTTPS is "
                    "HTTP carried over TLS, and is now a prerequisite for most browser features.",
         links=[L(S, "RFC 8446 (TLS 1.3)", "https://datatracker.ietf.org/doc/html/rfc8446"),
                WIKI("Transport_Layer_Security")], see_also=["http-https"]),
    dict(id="webauthn-passkeys", label="WebAuthn and Passkeys", section="03-web-development",
         subsection="web-security", parent="defenses", order=1072,
         definition="A standard for signing in with public-key cryptography instead of a shared "
                    "secret. The private key never leaves the user's device, so there is no "
                    "password for a site to leak or an attacker to phish. Passkeys are "
                    "WebAuthn credentials synchronised across a user's devices.",
         links=[L(S, "Web Authentication Level 2", "https://www.w3.org/TR/webauthn-2/"),
                L(R, "passkeys.dev", "https://passkeys.dev/"), WIKI("WebAuthn")],
         see_also=["phishing"]),
    dict(id="content-security-policy", label="CSP (Content Security Policy)",
         section="03-web-development", subsection="web-security", parent="defenses", order=1073,
         definition="An HTTP header by which a page declares which sources it may load scripts, "
                    "styles and other resources from. The browser enforces it, which turns most "
                    "cross-site scripting from a full compromise into a blocked request.",
         links=[L(S, "CSP Level 3", "https://www.w3.org/TR/CSP3/"),
                MDN("MDN Web Docs", "Web/HTTP/Guides/CSP")], see_also=["xss"]),
    dict(id="cors", label="CORS (Cross-Origin Resource Sharing)", section="03-web-development",
         subsection="web-security", parent="defenses", order=1074,
         definition="The mechanism by which a server opts in to being read by pages from other "
                    "origins. It relaxes the same-origin policy in a controlled way; it is a "
                    "permission system, not a restriction imposed on the server.",
         links=[MDN("MDN Web Docs", "Web/HTTP/Guides/CORS"), WIKI("Cross-origin_resource_sharing")]),

    # ------------------------------------------------------ Core Web Vitals
    dict(id="core-web-vitals", label="Core Web Vitals", section="04-additional-topics",
         subsection="performance-optimization", parent=None, order=1080,
         definition="Google's set of field metrics for user-perceived performance, measured on real "
                    "visits rather than in a lab. They give the vaguer goal of \"make it fast\" "
                    "three specific numbers to move, and they feed into search ranking.",
         links=[L(O, "web.dev — Web Vitals", "https://web.dev/articles/vitals")],
         see_also=["seo", "caching"]),
    dict(id="lcp", label="LCP (Largest Contentful Paint)", section="04-additional-topics",
         subsection="performance-optimization", parent="core-web-vitals", order=1081,
         definition="How long until the largest element in the viewport has rendered — a proxy for "
                    "when the page looks loaded to the person waiting.",
         links=[L(O, "web.dev — LCP", "https://web.dev/articles/lcp")]),
    dict(id="inp", label="INP (Interaction to Next Paint)", section="04-additional-topics",
         subsection="performance-optimization", parent="core-web-vitals", order=1082,
         definition="How long the page takes to visibly respond to user input, across the whole "
                    "visit. It replaced First Input Delay, which only measured the first "
                    "interaction and so missed most of the problem.",
         links=[L(O, "web.dev — INP", "https://web.dev/articles/inp")]),
    dict(id="cls", label="CLS (Cumulative Layout Shift)", section="04-additional-topics",
         subsection="performance-optimization", parent="core-web-vitals", order=1083,
         definition="How much visible content moves around unexpectedly while loading — the "
                    "metric for the page that shifts just as you go to tap something.",
         links=[L(O, "web.dev — CLS", "https://web.dev/articles/cls")]),

    # --------------------------------------------------- emerging / platform
    dict(id="webgpu", label="WebGPU", section="04-additional-topics",
         subsection="emerging-technologies", parent=None, order=1090, status="emerging",
         definition="A browser API exposing modern GPU capability for both rendering and general "
                    "computation, succeeding WebGL. It makes serious graphics work and in-browser "
                    "machine-learning inference practical on the web platform.",
         links=[L(S, "WebGPU", "https://www.w3.org/TR/webgpu/"),
                MDN("MDN Web Docs", "Web/API/WebGPU_API"), WIKI("WebGPU")]),
    dict(id="webrtc", label="WebRTC", section="04-additional-topics",
         subsection="emerging-technologies", parent=None, order=1091,
         definition="A set of APIs for real-time audio, video and data directly between browsers, "
                    "without a plugin and, once connected, often without relaying through a "
                    "server. It underpins most browser-based calling and conferencing.",
         links=[L(O, "Official Website", "https://webrtc.org/"),
                L(S, "WebRTC", "https://www.w3.org/TR/webrtc/"), WIKI("WebRTC")],
         see_also=["websockets"]),
    dict(id="service-workers", label="Service Workers", section="04-additional-topics",
         subsection="advanced-web-technologies", parent="progressive-web-apps", order=1100,
         definition="A script the browser runs separately from the page, able to intercept its "
                    "network requests. This is the machinery that lets a web app serve cached "
                    "content offline and receive push notifications.",
         links=[L(S, "Service Workers", "https://www.w3.org/TR/service-workers/"),
                MDN("MDN Web Docs", "Web/API/Service_Worker_API")],
         see_also=["caching", "progressive-web-apps"]),

    # ------------------------------------------------------------- AI-era web
    dict(id="llm", label="LLMs (Large Language Models)", section="04-additional-topics",
         subsection="ai-era-web", parent=None, order=1110,
         definition="Models trained on very large text corpora that predict continuations of a "
                    "prompt, and in doing so perform tasks they were not explicitly programmed "
                    "for. Accessed over HTTP APIs, they have become an ordinary component of web "
                    "applications rather than a specialist research tool.",
         links=[WIKI("Large_language_model")], see_also=["nlp", "deep-learning"]),
    dict(id="prompt-engineering", label="Prompt Engineering", section="04-additional-topics",
         subsection="ai-era-web", parent=None, order=1111,
         definition="Structuring the input to a language model — instructions, context, examples "
                    "and output format — to get reliable results. It matters because the same "
                    "underlying model can succeed or fail on a task depending on how the request "
                    "is framed.",
         links=[WIKI("Prompt_engineering")]),
    dict(id="embeddings", label="Embeddings", section="04-additional-topics",
         subsection="ai-era-web", parent=None, order=1112,
         definition="Numeric vectors representing text, images or other data such that items close "
                    "in meaning are close in the vector space. They are what makes search by "
                    "meaning rather than by keyword possible.",
         links=[WIKI("Word_embedding")], see_also=["vector-databases"]),
    dict(id="rag", label="RAG (Retrieval-Augmented Generation)", section="04-additional-topics",
         subsection="ai-era-web", parent=None, order=1113,
         definition="Retrieving relevant documents and supplying them to a language model as "
                    "context before it answers. It grounds answers in a specific corpus, which "
                    "reduces fabrication and lets a model use information it was never trained on "
                    "without retraining.",
         links=[WIKI("Retrieval-augmented_generation"),
                L(R, "Original paper (arXiv 2005.11401)", "https://arxiv.org/abs/2005.11401")],
         see_also=["embeddings", "vector-databases", "knowledge-graphs"]),
    dict(id="mcp", label="MCP (Model Context Protocol)", section="04-additional-topics",
         subsection="ai-era-web", parent=None, order=1114, status="emerging",
         definition="An open protocol for connecting language models to external tools and data "
                    "sources through a common interface, so an integration written once works "
                    "across different clients instead of being rebuilt per application.",
         links=[L(O, "Official Website", "https://modelcontextprotocol.io/")],
         see_also=["restful-apis", "ai-agents"]),
    dict(id="streaming-responses", label="Streaming Responses", section="04-additional-topics",
         subsection="ai-era-web", parent=None, order=1115,
         definition="Delivering a response incrementally as it is produced rather than waiting for "
                    "it to complete, usually over Server-Sent Events or a readable stream. It is "
                    "what makes a model's answer appear token by token instead of after a long "
                    "pause.",
         links=[MDN("Server-Sent Events", "Web/API/Server-sent_events"),
                MDN("Streams API", "Web/API/Streams_API")],
         see_also=["websockets"]),
    dict(id="ai-agents", label="AI Agents", section="04-additional-topics",
         subsection="ai-era-web", parent=None, order=1116, status="emerging",
         definition="Systems in which a language model plans and carries out multi-step tasks by "
                    "calling tools and reacting to the results, rather than only producing text. "
                    "This is the classical notion of a software agent, with a model supplying the "
                    "decision-making.",
         links=[WIKI("Intelligent_agent")], see_also=["agents", "mcp", "autonomous-systems"]),
]


def main() -> int:
    written, skipped = 0, 0
    for c in CONCEPTS:
        d = ROOT / "concepts" / c["section"]
        d.mkdir(parents=True, exist_ok=True)
        path = d / f"{c['id']}.yml"

        doc: dict = {
            "id": c["id"],
            "label": c["label"],
            "section": c["section"],
        }
        if c.get("subsection"):
            doc["subsection"] = c["subsection"]
        doc["parent"] = c.get("parent")
        doc["order"] = c["order"]
        doc["level"] = c.get("level")
        doc["status"] = c.get("status", "current")
        if c.get("see_also"):
            doc["see_also"] = c["see_also"]
        doc["definition"] = " ".join(c["definition"].split())
        doc["links"] = c["links"]

        path.write_text(
            yaml.safe_dump(doc, sort_keys=False, allow_unicode=True, width=100),
            encoding="utf-8",
        )
        written += 1
        print(f"  {c['section']}/{c['id']}.yml")

    print(f"\n{written} concept files written, {skipped} skipped")
    print("Remember: concepts/_taxonomy.yml needs the ai-era-web subsection.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
